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

        self.checkUpdate()
        init = Init()
        self.conn         = init.getConn()
        self.cursor       = self.conn.cursor() 
        self.epubContent  = {}
        self.epubInfoList = []
        self.baseDir      = os.path.realpath('.')
        self.setting      = Setting()
        return 
    
    def helperStart(self):
        #登陆
        settingDict = self.setting.getSetting(['rememberAccount', 'maxThread', 'picQuality'])
        self.rememberAccount = settingDict['rememberAccount']
        self.maxThread       = settingDict['maxThread']
        self.picQuality      = settingDict['picQuality']
        if self.maxThread == '':
            self.maxThread = 20
        else:
            self.maxThread = int(self.maxThread)

        if self.picQuality == '':
            self.picQuality = 1
        else:
            self.picQuality = int(self.picQuality)


        login = Login(self.conn)
        if self.rememberAccount == 'yes':
            print   u'检测到有设置文件，是否直接使用之前的设置？(帐号、密码、图片质量、最大线程数)'
            print   u'直接点按回车使用之前设置，敲入任意字符后点按回车进行重新设置'
            if raw_input() == '':
                login.setCookie()
            else:
                login.login()
                self.maxThread  = int(self.setting.guideOfMaxThread())
                self.picQuality = int(self.setting.guideOfPicQuality())
        else:
            login.login()
            self.maxThread  = int(self.setting.guideOfMaxThread())
            self.picQuality = int(self.setting.guideOfPicQuality())

        #储存设置
        self.setting = Setting()
        settingDict = {
                'maxThread'  : self.maxThread,
                'picQuality' : self.picQuality,
                }
        self.setting.setSetting(settingDict)
        
        #主程序开始运行
        readList  = open('./ReadList.txt', 'r')
        bookCount = 1 
        for line in readList:
            #一行内容代表一本电子书
            chapter = 1
            for rawUrl in line.split('$'):
                print u'正在制作第{}本电子书的第{}节'.format(bookCount, chapter)
                urlInfo = self.getUrlInfo(rawUrl)
                if not 'filter' in urlInfo:
                    continue
                self.manager(urlInfo)
                try:
                    self.addEpubContent(urlInfo['filter'].getResult())
                    self.epubInfoList.append(urlInfo['filter'].getInfoDict())
                except TypeError as error:
                    print u'没有收集到指定问题'
                    print u'错误信息:'
                    print error
                chapter += 1
            if self.epubContent != {}:
                Zhihu2Epub(self.epubContent, self.epubInfoList)
            self.epubContent  = {}
            self.epubInfoList = []
            self.resetDir()
            bookCount += 1
        return

    def addEpubContent(self, result = {}):
        u'''
        将分析到的数据添加至epubContent中去
        '''
        for questionID in result:
            if questionID in self.epubContent:
                self.epubContent[questionID]['questionInfo'] = result[questionID]['questionInfo']
            else:
                self.epubContent[questionID] = {}
                self.epubContent[questionID]['questionInfo']   = result[questionID]['questionInfo']
                self.epubContent[questionID]['answerListDict'] = {}
            for answerID in result[questionID]['answerListDict']:
                answerDict = result[questionID]['answerListDict'][answerID]
                self.epubContent[questionID]['answerListDict'][answerID] = answerDict
        return

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
        def detectUrl(rawUrl):
            targetPattern = {}
            targetPattern['answer']     = r'(?<=zhihu\.com/)question/\d{8}/answer/\d{8}'
            targetPattern['question']   = r'(?<=zhihu\.com/)question/\d{8}'
            targetPattern['author']     = r'(?<=zhihu\.com/)people/[^/#\n\r]*'#使用#作为备注起始标识符，所以在正则中要去掉#
            targetPattern['collection'] = r'(?<=zhihu\.com/)collection/\d*'
            targetPattern['table']      = r'(?<=zhihu\.com/)roundtable/[^/#\n\r]*'
            targetPattern['topic']      = r'(?<=zhihu\.com/)topic/\d*'
            targetPattern['article']    = r'(?<=zhuanlan\.zhihu\.com/)[^/]*/\d{8}'#先检测专栏，再检测文章，文章比专栏网址更长，类似问题与答案的关系，取信息可以用split('/')的方式获取
            targetPattern['column']     = r'(?<=zhuanlan\.zhihu\.com/)[^/#\n\r]*'
            for key in ['answer', 'question', 'author', 'collection', 'table', 'topic', 'article', 'column']:
                urlInfo['url'] = re.search(targetPattern[key], rawUrl)
                if urlInfo['url'] != None:
                    urlInfo['kind'] = key
                    if key != 'article' and key != 'column':
                        urlInfo['baseUrl']  = 'http://www.zhihu.com/' + urlInfo['url'].group(0) 
                    else:
                        urlInfo['baseUrl']  = 'http://zhuanlan.zhihu.com/' + urlInfo['url'].group(0) 
                    return key
            return ''   
        kind = detectUrl(rawUrl)
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
        if kind == 'column':
            urlInfo['columnID']     = re.search(r'(?<=zhuanlan\.zhihu\.com/)[^/]*', urlInfo['baseUrl']).group(0)
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
        if time == "2015-02-26":
            return
        else:
            print u"发现新版本，\n更新说明:{}\n更新日期:{} ，点按回车进入更新页面".format(updateComment, time)
            print u'新版本下载地址:' + url
            raw_input()
            import  webbrowser
            webbrowser.open_new_tab(url)
        return
