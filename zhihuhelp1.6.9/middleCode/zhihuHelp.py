# -*- coding: utf-8 -*-
import sqlite3
import cookielib
import Cookie
import urllib2
import json

import re
import os

from httpLib import *
from helper  import *
from worker  import *
from init    import *
from login   import *

class ZhihuHelp(object):
    def __init__(self):
        u"""
        配置文件使用$符区隔，同一行内的配置文件归并至一本电子书内
        """
        init  = Init()
        self.conn   = init.getConn()
        self.cursor = self.conn.cursor() 
        return 
    
    def helperStart(self):
        login = Login(self.conn)
        login.login()
        self.setting = Setting()
        self.maxThread  = self.guideOfMaxThread()
        self.picQuality = self.guideOfPicQuality()
        readList = open('./ReadList.txt', 'r')
        for line in readList:
            targetList = []
            for rawUrl in line.split('$'):
                urlInfo = self.getUrlInfo(rawUrl)
                if urlInfo == {}:
                    continue
                urlInfo['filter'] = self.manager(urlInfo)
                targetList.append(urlInfo)
            epub = EpubBuilder(targetList)
            epub.makeEpub()
        return

    def getUrlInfo(self, rawUrl):
        u"""
        返回标准格式的网址
        返回查询所需要的内容
        """
        urlInfo = {}
        def detectUrl(rawUrl):
            targetPattern = {}
            targetPattern['answer']     = r'(?<=zhihu\.com/)question/\d{8}/answer/\d{8}'
            targetPattern['question']   = r'(?<=zhihu\.com/)question/\d{8}'
            targetPattern['author']     = r'(?<=zhihu\.com/)people/[^/#]*'#使用#作为备注起始标识符，所以在正则中要去掉#
            targetPattern['collection'] = r'(?<=zhihu\.com/)collection/\d*'
            targetPattern['table']      = r'(?<=zhihu\.com/)roundtable/[^/#]*'
            targetPattern['topic']      = r'(?<=zhihu\.com/)topic/\d*'
            targetPattern['article']    = r'(?<=zhuanlan\.zhihu\.com/)[^/]*/\d{8}'#先检测专栏，再检测文章，文章比专栏网址更长，类似问题与答案的关系，取信息可以用split('/')的方式获取
            targetPattern['column']     = r'(?<=zhuanlan\.zhihu\.com/)[^/#]*'
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
        if kind == 'question':
            urlInfo['questionID']   = re.search(r'(?<=zhihu\.com/question/)\d{8}', urlInfo['baseUrl']).group(0)
        if kind == 'author':
            urlInfo['authorID']     = re.search(r'(?<=zhihu\.com/people/)[^/#]*', urlInfo['baseUrl']).group(0)
        if kind == 'collection':
            urlInfo['collectionID'] = re.search(r'(?<=zhihu\.com/collection/)\d*', urlInfo['baseUrl']).group(0)
        if kind == 'table':
            urlInfo['tableID']      = re.search(r'(?<=zhihu\.com/roundtable/)[^/#]*', urlInfo['baseUrl']).group(0)
        if kind == 'topic':
            urlInfo['topicID']      = re.search(r'(?<=zhihu\.com/topic/)\d*', urlInfo['baseUrl']).group(0)
        if kind == 'article':
            urlInfo['columnID']     = re.search(r'(?<=zhuanlan\.zhihu\.com/)[^/]*', urlInfo['baseUrl']).group(0)
            urlInfo['articleID']    = re.search(r'(?<=zhuanlan\.zhihu\.com/' + urlInfo['columnID'] + '/)' + '\d{8}', urlInfo['baseUrl']).group(0)
        if kind == 'column':
            urlInfo['columnID']     = re.search(r'(?<=zhuanlan\.zhihu\.com/)[^/]*', urlInfo['baseUrl']).group(0)
        return urlInfo

    def manager(self, urlInfo = {}):
        kind = urlInfo['kind']
        questionFilter, authorFilter = self.setFilter()

        if kind == 'answer':
            print u'啊哦，这个功能作者还没写←_←，敬请期待！'
        if kind == 'question':
            worker = QuestionWorker(conn = self.conn, maxThread = self.maxThread, targetUrl=urlInfo['baseUrl'])
            worker.boss()
            return questionFilter 
        if kind == 'author':
            print u'啊哦，这个功能作者还没写←_←，敬请待！'
        if kind == 'collection':
            print u'啊哦，这个功能作者还没写←_←，敬请期待！'
        if kind == 'table':
            print u'啊哦，这个功能作者还没写←_←，敬请期待！'
        if kind == 'topic':
            print u'啊哦，这个功能作者还没写←_←，敬请期待！'
        if kind == 'article':
            print u'啊哦，这个功能作者还没写←_←，敬请期待！'
        if kind == 'column':
            urlInfo['columnID']     = re.search(r'(?<=zhuanlan\.zhihu\.com/)^[/]*', rawUrl).group(0)

    def setFilter(self):
        answerFilter   = {}
        questionFilter = {}
        authorFilter   = {}
        #对答案的筛选
        answerFilter['minAgree']        = 0
        answerFilter['maxAgree']        = 100000
        answerFilter['minLength']       = 100
        answerFilter['maxLength']       = 100000
        answerFilter['minAverageAgree'] = 10#平均每字赞同数
        answerFilter['maxAverageAgree'] = 10#平均每字赞同数
        answerFilter['minDate']         = '2010-10-01'
        answerFilter['maxDate']         = '2099-12-12'
        answerFilter['noRecord']        = '0'
        answerFilter['imgSize']         = 1#图片质量，0:无图，1:普通，2:高清
        #对问题的筛选
        questionFilter['minComment']              = 0 
        questionFilter['maxComment']              = 1000000 
        questionFilter['minFollowCount']          = 0 
        questionFilter['maxFollowCount']          = 1000000 
        questionFilter['minAnswerCount']          = 0 
        questionFilter['maxAnswerCount']          = 1000000 
        questionFilter['minViewCount']            = 0 
        questionFilter['maxViewCount']            = 1000000 
        questionFilter['minCollapsedAnswerCount'] = 0 
        questionFilter['maxCollapsedAnswerCount'] = 1000000 
        #对人的筛选
        authorFilter['minAgree']          = 0
        authorFilter['maxAgree']          = 100000
        authorFilter['minCollect']        = 0
        authorFilter['maxCollect']        = 100000
        authorFilter['minEdit']           = 0
        authorFilter['maxEdit']           = 100000
        authorFilter['minColumn']         = 0
        authorFilter['maxColumn']         = 100000
        authorFilter['minThanks']         = 0
        authorFilter['maxThanks']         = 100000
        authorFilter['minAnswer']         = 0
        authorFilter['maxAnswer']         = 100000
        authorFilter['minQuestion']       = 0
        authorFilter['maxQuestion']       = 100000
        authorFilter['minAnswerCount']    = 0
        authorFilter['maxAnswerCount']    = 100000
        authorFilter['minAverageAgree']   = 0#平均赞同数
        authorFilter['maxAverageAgree']   = 100000
        authorFilter['minAverageCollect'] = 0#平均收藏数
        authorFilter['maxAverageCollect'] = 100000
        return questionFilter, authorFilter 
    
class EpubData(object):
    def __init__(self, cursor = None, urlInfo = {}):
        self.cursor  = cursor
        self.urlInfo = urlInfo

    def createQuestionFilterSQL(self):
        self.answerQuery = "select * from AnswerContent where questionID = %s"
        
        sqlVarList = []
        
        sqlQuestionFilter['minAgree']        = 'answerAgreeCount > %s'
        sqlQuestionFilter['maxAgree']        = 'answerAgreeCount < %s'
        sqlQuestionFilter['minDate']         = 'updateDate > %s'
        sqlQuestionFilter['maxDate']         = 'updateDate < %s'
        sqlQuestionFilter['noRecord']        = 'noRecordFlag == %s'
        
        for key in self.urlInfo['filter']:
            self.answerQuery += ' and ' + sqlQuestionFilter[key]
            sqlVarList.append(self.urlInfo['filter'][key])
        allAnswer = self.cursor.execute(self.answerQuery%sqlVarList).fetchAll()
        
        return 
    
    def formatAnswerDict(self, allAnswer):
        itemList  = ['authorID', 'authorSign', 'authorLogo', 'authorName', 'answerAgreeCount',  'answerContent',  'questionID',  'answerID',  'commitDate',  'updateDate',  'answerCommentCount',  'noRecordFlag',  'answerHref']
        self.answerDict = {}
        for line in range(allAnswer):
            self.answerDict[line] = {}
            for index in range(itemList):
                self.answerDict[line][itemList[index]] = allAnswer[line][index]

    def imgProcess(self):
        return

    def imgDownload(self):
        return
    

