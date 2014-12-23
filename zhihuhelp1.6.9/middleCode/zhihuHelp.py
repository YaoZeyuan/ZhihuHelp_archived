# -*- coding: utf-8 -*-
import sqlite3
import cookielib
import Cookie
import urllib2
import json

import re
import os

from httpLib import *
from helper import *
from worker import PageWorker

class ZhihuHelp:
    u"""
    助手未来肯定是要换设置文件的结构的，
    这个类作为中间文件，
    负责将原始的设置文件转换为未来的标准格式
    """
    def __init__(self):
        u"""
        配置文件使用$符区隔，同一行内的配置文件归并至一本电子书内
        """
        init  = init()
        login = Login(conn)
        login.login()
        self.conn   = init.getConn()
        self.cursor = self.conn.cursor() 
        readList = open('./ReadList.txt')
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
        def detectUrl():
            targetPattern = {}
            targetPattern['answer']     = r'(?<=zhihu\.com/)question/\d{8}/answer/\d{8}'
            targetPattern['question']   = r'(?<=zhihu\.com/)question/\d{8}'
            targetPattern['author']     = r'(?<=zhihu\.com/)people/[^/#]*'#使用#作为备注起始标识符，所以在正则中要去掉#
            targetPattern['collection'] = r'(?<=zhihu\.com/)collection/\d*'
            targetPattern['table']      = r'(?<=zhihu\.com/)roundtable/[^/#]*'
            targetPattern['topic']      = r'(?<=zhihu\.com/)topic/\d*'
            targetPattern['article']    = r'(?<=zhuanlan\.zhihu\.com/)^[/]/\d{8}.*'#先检测专栏，再检测文章，文章比专栏网址更长，类似问题与答案的关系，取信息可以用split('/')的方式获取
            targetPattern['column']     = r'(?<=zhuanlan\.zhihu\.com/)[^/#]*'
            for key in ['answer', 'question', 'athor', 'collection', 'table', 'topic', 'article', 'column']:
                urlInfo['url'] = re.search(targetPattern[key], rawUrl)
                if urlInfo['url']  != None:
                    urlInfo['kind'] = kind
                    if kind != 'article' and kind != 'column':
                        urlInfo['baseUrl']  = 'http://www.zhihu.com/' + urlInfo['url'].group(0) 
                    else:
                        urlInfo['baseUrl']  = 'http://zhuanlan.zhihu.com/' + urlInfo['url'].group(0) 
                    return key
            return ''   
        kind = detectUrl(rawUrl)
        if kind == 'answer':
            urlInfo['questionID']   = re.search(r'(?<=zhihu\.com/question/)\d{8}', rawUrl).group(0)
            urlInfo['answerID']     = re.search(r'(?<=zhihu\.com/question/\d{8}/answer/)\d{8}', rawUrl).group(0)
        if kind == 'question':
            urlInfo['questionID']   = re.search(r'(?<=zhihu\.com/question/)\d{8}', rawUrl).group(0)
        if kind == 'author':
            urlInfo['authorID']     = re.search(r'(?<=zhihu\.com/people/)[^/#]*', rawUrl).group(0)
        if kind == 'collection':
            urlInfo['collectionID'] = re.search(r'(?<=zhihu\.com/collection/)\d*', rawUrl).group(0)
        if kind == 'table':
            urlInfo['tableID']      = re.search(r'(?<=zhihu\.com/roundtable/)[^/#]*', rawUrl).group(0)
        if kind == 'topic':
            urlInfo['topicID']      = re.search(r'(?<=zhihu\.com/topic/)\d*', rawUrl).group(0)
        if kind == 'article':
            urlInfo['columnID']     = re.search(r'(?<=zhuanlan\.zhihu\.com/)^[/]*', rawUrl).group(0)
            urlInfo['articleID']    = re.search(r'(?<=zhuanlan\.zhihu\.com/)'+ urlInfo['columnID'] +'/\d{8}.*', rawUrl).group(0)
        if kind == 'column':
            urlInfo['columnID']     = re.search(r'(?<=zhuanlan\.zhihu\.com/)^[/]*', rawUrl).group(0)
        return urlInfo

    def manager(self, urlInfo = {}):
        kind = urlInfo['kind']
        questionFilter, authorFilter = self.setFilter()

        if kind == 'answer':
            print u'啊哦，这个功能作者还没写←_←，敬请期待！'
        if kind == 'question':
            worker = QuestionWorker(conn = self.conn, maxWorker = self.maxWorker, targetUrl=urlInfo['baseUrl'])
            worker.boss()
            return questionFilter 
        if kind == 'author':
            print u'啊哦，这个功能作者还没写←_←，敬请期！'
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
        questionFilter = {}
        authorFilter   = {}
        #对答案的筛选
        questionFilter['minAgree']        = 0
        questionFilter['maxAgree']        = 100000
        questionFilter['minLength']       = 100
        questionFilter['maxLength']       = 100000
        questionFilter['minAverageAgree'] = 10#平均每字赞同数
        questionFilter['maxAverageAgree'] = 10#平均每字赞同数
        questionFilter['minDate']         = '2010-10-01'
        questionFilter['maxDate']         = '2099-12-12'
        #对人的筛选
        authorFilter['minAgree']          = 0
        authorFilter['maxAgree']          = 100000
        authorFilter['minCollect']        = 0
        authorFilter['maxCollect']        = 100000
        authorFilter['minEdit']           = 100000
        authorFilter['maxEdit']           = 100000
        authorFilter['minColumn']         = 100000
        authorFilter['maxColumn']         = 100000
        authorFilter['minThanks']         = 100000
        authorFilter['maxThanks']         = 100000
        authorFilter['minAnswer']         = 100000
        authorFilter['maxAnswer']         = 100000
        authorFilter['minQuestion']       = 100000
        authorFilter['maxQuestion']       = 100000
        authorFilter['minAnswerCount']    = 100
        authorFilter['maxAnswerCount']    = 100000
        authorFilter['minAverageAgree']   = 10#平均赞同数
        authorFilter['maxAverageAgree']   = 10
        authorFilter['minAverageCollect'] = 10#平均收藏数
        authorFilter['maxAverageCollect'] = 10
        return questionFilter, authorFilter 


