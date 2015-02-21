# -*- coding: utf-8 -*-
import sqlite3
import cookielib
import Cookie
import urllib2
import json

import re
import os

from httpLib      import *
from helper       import *
from worker       import *
from init         import *
from login        import *
from simpleFilter import *
from epubBuilder.epubBuilder import * 

class ZhihuHelp(object):
    def __init__(self):
        u"""
        配置文件使用$符区隔，同一行内的配置文件归并至一本电子书内
        """
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
            self.maxThread = 5
        else:
            self.maxThread = int(self.maxThread)

        if self.picQuality == '':
            self.picQuality = 1
        else:
            self.picQuality = int(self.picQuality)


        login = Login(self.conn)
        if self.rememberAccount == '':
            login.login()
            self.maxThread  = int(self.setting.guideOfMaxThread())
            self.picQuality = int(self.setting.guideOfPicQuality())
        else:
            login.setCookie()

        #储存设置
        self.setting = Setting()
        settingDict = {
                'maxThread'  : self.maxThread,
                'picQuality' : self.picQuality,
                }
        self.setting.setSetting(settingDict)
        
        #主程序开始运行
        readList = open('./ReadList.txt', 'r')
        for line in readList:
            #一行内容代表一本电子书
            for rawUrl in line.split('$'):
                urlInfo = self.getUrlInfo(rawUrl)
                if urlInfo == {}:
                    continue
                self.manager(urlInfo)
                self.addEpubContent(urlInfo['filter'].getResult())
                self.epubInfoList.append(urlInfo['filter'].getInfoDict())
            Zhihu2Epub(self.epubContent, self.epubInfoList)
            self.epubContent  = {}
            self.epubInfoList = []
            self.resetDir()
            print u'test over'
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

    def mkdir(self, path):
        try:
            os.mkdir(path)
        except OSError:
            print u'指定目录已存在'
        return 
    
    def chdir(self, path):
        try:
            os.chdir(path)
        except OSError:
            print u'指定目录不存在，自动创建之'
            mkdir(path)
            os.chdir(path)
        return

    def resetDir(self):
        chdir(self.baseDir)
        return
