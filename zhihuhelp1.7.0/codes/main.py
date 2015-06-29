# -*- coding: utf-8 -*-
from baseClass import *

import sqlite3
import cookielib
import Cookie
import urllib2
import json

import re
import os

from worker       import *
from init         import *
from login        import *
from simpleFilter import *
from epubBuilder.epubBuilder import * 

class ZhihuHelp(BaseClass):
    def __init__(self):
        u"""
        配置文件使用$符区隔，同一行内的配置文件归并至一本电子书内
        """
        if TestClass.test_catchAnswerData_flag:
            print u'测试期间，移除检查更新模块，测试完成后请删除'
        else:
            self.checkUpdate()
        init = Init()
        self.conn    = init.getConn()
        self.cursor  = self.conn.cursor()
        self.baseDir = os.path.realpath('.')
        self.config  = Setting()

        # 初始化网址检测模板
        self.initBaseResource()
        return

    def initBaseResource(self):
        self.urlKind    = ['answer', 'question', 'author', 'collection', 'table', 'topic', 'article', 'column']

        self.urlPattern = {}
        self.urlPattern['answer']     = r'(?<=zhihu\.com/)question/\d{8}/answer/\d{8}'
        self.urlPattern['question']   = r'(?<=zhihu\.com/)question/\d{8}'

        # 使用#作为备注起始标识符，所以在正则中要去掉#
        self.urlPattern['author']     = r'(?<=zhihu\.com/)people/[^/#\n\r]*'
        self.urlPattern['collection'] = r'(?<=zhihu\.com/)collection/\d*'
        self.urlPattern['table']      = r'(?<=zhihu\.com/)roundtable/[^/#\n\r]*'
        self.urlPattern['topic']      = r'(?<=zhihu\.com/)topic/\d*'

        # 先检测专栏，再检测文章，文章比专栏网址更长，类似问题与答案的关系，取信息可以用split('/')的方式获取
        self.urlPattern['article']    = r'(?<=zhuanlan\.zhihu\.com/)[^/]*/\d{8}'
        self.urlPattern['column']     = r'(?<=zhuanlan\.zhihu\.com/)[^/#\n\r]*'
        return

    def helperStart(self):
        # 登陆
        settingDict = self.config.getSetting(['rememberAccount', 'maxThread', 'picQuality'])
        rememberAccount = settingDict['rememberAccount']



        login = Login(self.conn)
        if rememberAccount == 'yes':
            print   u'检测到有设置文件，是否直接使用之前的设置？(帐号、密码、图片质量、最大线程数)'
            print   u'直接点按回车使用之前设置，敲入任意字符后点按回车进行重新设置'
            if raw_input() == '':
                login.setCookie()
                SettingClass.MAXTHREAD  = settingDict['maxThread']
                SettingClass.PICQUALITY = settingDict['picQuality']
                if SettingClass.MAXTHREAD == '':
                    SettingClass.MAXTHREAD = 20
                else:
                    SettingClass.MAXTHREAD = int(SettingClass.MAXTHREAD)

                if SettingClass.PICQUALITY == '':
                    SettingClass.PICQUALITY = 1
                else:
                    SettingClass.PICQUALITY = int(SettingClass.PICQUALITY)
            else:
                login.login()
                SettingClass.MAXTHREAD  = int(self.config.guideOfMaxThread())
                SettingClass.PICQUALITY = int(self.config.guideOfPicQuality())
        else:
            login.login()
            SettingClass.MAXTHREAD  = int(self.config.guideOfMaxThread())
            SettingClass.PICQUALITY = int(self.config.guideOfPicQuality())

        #储存设置
        self.config = Setting()
        settingDict = {
                'maxThread'  : SettingClass.MAXTHREAD,
                'picQuality' : SettingClass.PICQUALITY,
                }
        self.config.setSetting(settingDict)
        self.config.saveToGlobalClass()
        
        #主程序开始运行
        readList  = open('./ReadList.txt', 'r')
        bookCount = 1 
        for line in readList:
            # 一行内容代表一本电子书
            chapter = 1

            # 先将栏目进行分类，以便并行执行，加快速度
            taskQueen = {}
            taskQueen['questionQueen'] = []
            taskQueen['answerQueen']   = []
            taskQueen['articleQueen']  = [] # 专栏文章队列
            taskQueen['otherQueen']    = [] # 其他队列，主要是用户、收藏夹、话题、专栏等无法并行执行的队列
            # 预处理部分开始
            for rawUrl in line.split('$'):
                urlInfo = self.detectUrl(rawUrl)
                if not 'kind' in urlInfo:
                    continue
                if urlInfo['kind'] == 'question':
                    taskQueen['questionQueen'].append(urlInfo)
                    continue
                if urlInfo['kind'] == 'answer':
                    taskQueen['answerQueen'].append(urlInfo)
                    continue
                if urlInfo['kind'] == 'article':
                    taskQueen['articleQueen'].append(urlInfo)
                    continue
                taskQueen['otherQueen'].append(urlInfo)




            for rawUrl in line.split('$'):
                # todo
                # 可以使用队列对待抓取页面进行分类整理，加快抓取速度
                # 每个种类各一个队列
                # 就算是非线性抓取也没关系，增强报错记录功能就行了，先把速度提上去
                # 主要是对单个问题和单个答案的抓取，暂时不考虑单篇专栏文章的问题
                print u'正在制作第{bookNo}本电子书的第{chapterNo}节'.format(bookNo = bookCount, chapterNo = chapter)
                urlInfo = self.getUrlInfo(rawUrl)
                if not 'filter' in urlInfo:
                    continue

                if TestClass.test_catchAnswerData_flag:
                    print u'测试期间，跳过对网页的抓取'
                else:
                    self.manager(urlInfo)

                try:
                    self.addEpubContent(urlInfo['filter'].getResult())
                except TypeError as error:
                    print u'没有收集到指定问题'
                    print u'错误信息:'
                    print error
                chapter += 1

            try:
                if self.epubContent:
                    Zhihu2Epub(self.epubContent)
                del self.epubContent
            except AttributeError:
                pass

            self.resetDir()
            bookCount += 1
        return

    def addEpubContent(self, result):
        u'''
        分析到的数据为自行制作的Package类型，
        具有一定的内容分析能力
        '''
        try:
            self.epubContent.merge(result)
        except AttributeError:
            self.epubContent = result
        return



    def detectUrl(self, rawUrl):
        u"""
        检测Url类型并返回对应值
        """
        urlInfo = {}
        for key in self.urlKind:
            urlInfo['url'] = re.search(self.urlPattern[key], rawUrl)
            if urlInfo['url'] != None:
                urlInfo['kind'] = key
                if key != 'article' and key != 'column':
                    urlInfo['baseUrl']  = 'http://www.zhihu.com/' + urlInfo['url'].group(0)
                else:
                    urlInfo['baseUrl']  = 'http://zhuanlan.zhihu.com/' + urlInfo['url'].group(0)
                return urlInfo
            return urlInfo

    def getUrlInfo(self, rawUrl):
        u"""
        返回标准格式的网址
        返回查询所需要的内容
        urlInfo 结构
        *   kind
            *   answer
                *   questionID
                *   answerID
            *   question
                *   questionID
            *   author
                *   authorID
            *   collection
                *   colliectionID
            *   table
                *   tableID
            *   topic
                *   topicID
            *   article
                *   columnID
                *   articleID
            *   column
                *   columnID
        *   guide
            *   用于输出引导语，告知用户当前工作的状态
        *   worker
            *   用于生成抓取对象，负责抓取网页内容
        *   filter
            *   用于生成过滤器，负责在数据库中提取答案，并将答案组织成便于生成电子书的结构
        *   urlInfo
            *   用于为Author/Topic/Table获取信息
        *   baseSetting
            *   基础的设置信息，比如图片质量，过滤标准
            *   picQuality
                *   图片质量
            *   maxThread
                *   最大线程数
        """
        urlInfo = {}
        urlInfo['baseSetting'] = {}
        urlInfo['baseSetting']['picQuality'] = self.picQuality
        urlInfo['baseSetting']['maxThread']  = self.maxThread

        kind = self.detectUrl(rawUrl)
        if kind == 'answer':
            urlInfo['questionID']   = re.search(r'(?<=zhihu\.com/question/)\d{8}', urlInfo['baseUrl']).group(0)
            urlInfo['answerID']     = re.search(r'(?<=zhihu\.com/question/\d{8}/answer/)\d{8}', urlInfo['baseUrl']).group(0)
            urlInfo['guide']        = u'成功匹配到答案地址{}，开始执行抓取任务'.format(urlInfo['baseUrl'])
            urlInfo['worker']       = AnswerWorker(conn = self.conn, urlInfo = urlInfo)
            urlInfo['filter']       = AnswerFilter(self.cursor, urlInfo)
            urlInfo['infoUrl']      = ''
        if kind == 'question':
            urlInfo['questionID']   = re.search(r'(?<=zhihu\.com/question/)\d{8}', urlInfo['baseUrl']).group(0)
            urlInfo['guide']        = u'成功匹配到问题地址{}，开始执行抓取任务'.format(urlInfo['baseUrl'])
            urlInfo['worker']       = QuestionWorker(conn = self.conn, urlInfo = urlInfo)
            urlInfo['filter']       = QuestionFilter(self.cursor, urlInfo)
            urlInfo['infoUrl']      = ''
        if kind == 'author':
            urlInfo['authorID']     = re.search(r'(?<=zhihu\.com/people/)[^/#]*', urlInfo['baseUrl']).group(0)
            urlInfo['guide']        = u'成功匹配到用户主页地址{}，开始执行抓取任务'.format(urlInfo['baseUrl'])
            urlInfo['worker']       = AuthorWorker(conn = self.conn, urlInfo = urlInfo)
            urlInfo['filter']       = AuthorFilter(self.cursor, urlInfo)
            urlInfo['infoUrl']      = urlInfo['baseUrl'] + '/about'
        if kind == 'collection':
            urlInfo['collectionID'] = re.search(r'(?<=zhihu\.com/collection/)\d*', urlInfo['baseUrl']).group(0)
            urlInfo['guide']        = u'成功匹配到收藏夹地址{}，开始执行抓取任务'.format(urlInfo['baseUrl'])
            urlInfo['worker']       = CollectionWorker(conn = self.conn, urlInfo = urlInfo)
            urlInfo['filter']       = CollectionFilter(self.cursor, urlInfo)
            urlInfo['infoUrl']      = urlInfo['baseUrl']
        if kind == 'topic':
            urlInfo['topicID']      = re.search(r'(?<=zhihu\.com/topic/)\d*', urlInfo['baseUrl']).group(0)
            urlInfo['guide']        = u'成功匹配到话题地址{}，开始执行抓取任务'.format(urlInfo['baseUrl'])
            urlInfo['worker']       = TopicWorker(conn = self.conn, urlInfo = urlInfo)
            urlInfo['filter']       = TopicFilter(self.cursor, urlInfo)
            urlInfo['infoUrl']      = urlInfo['baseUrl']
        if kind == 'table':
            urlInfo['tableID']      = re.search(r'(?<=zhihu\.com/roundtable/)[^/#]*', urlInfo['baseUrl']).group(0)
        if kind == 'article':
            urlInfo['columnID']     = re.search(r'(?<=zhuanlan\.zhihu\.com/)[^/]*', urlInfo['baseUrl']).group(0)
            urlInfo['articleID']    = re.search(r'(?<=zhuanlan\.zhihu\.com/' + urlInfo['columnID'] + '/)' + '\d{8}', urlInfo['baseUrl']).group(0)
            urlInfo['worker']       = ColumnWorker(conn = self.conn, urlInfo = urlInfo)
            urlInfo['filter']       = ArticleFilter(self.cursor, urlInfo)
            urlInfo['infoUrl']      = urlInfo['baseUrl']
        if kind == 'column':
            #专栏文章的总量并不多，所以获取单篇文章可以和获取全部文章一块完成
            urlInfo['columnID']     = re.search(r'(?<=zhuanlan\.zhihu\.com/)[^/]*', urlInfo['baseUrl']).group(0)
            urlInfo['guide']        = u'成功匹配到专栏地址{}，开始执行抓取任务'.format(urlInfo['baseUrl'])
            urlInfo['worker']       = ColumnWorker(conn = self.conn, urlInfo = urlInfo)
            urlInfo['filter']       = ColumnFilter(self.cursor, urlInfo)
            urlInfo['infoUrl']      = urlInfo['baseUrl']
        return urlInfo

    def manager(self, urlInfo = {}):
        print urlInfo['guide']
        urlInfo['worker'].start()
        return

    def resetDir(self):
        chdir(self.baseDir)
        return
    
    def checkUpdate(self):#强制更新
        u"""
            *   功能
                *   检测更新。
                *   若在服务器端检测到新版本，自动打开浏览器进入新版下载页面
                *   网页请求超时或者版本号正确都将自动跳过
            *   输入
                *   无
            *   返回
                *   无
        """
        print   u"检查更新。。。"
        try:
            updateTime = urllib2.urlopen(u"http://zhihuhelpbyyzy-zhihu.stor.sinaapp.com/ZhihuHelpUpdateTime.txt", timeout = 10)
        except:
            return
        time = updateTime.readline().replace(u'\n','').replace(u'\r','')
        url  = updateTime.readline().replace(u'\n','').replace(u'\r','')
        updateComment = updateTime.read()#可行？
        if time == "2015-06-19":
            return
        else:
            print u"发现新版本，\n更新说明:{}\n更新日期:{} ，点按回车进入更新页面".format(updateComment, time)
            print u'新版本下载地址:' + url
            raw_input()
            import  webbrowser
            webbrowser.open_new_tab(url)
        return
