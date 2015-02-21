# -*- coding: utf-8 -*-

import threading
import time
import cookielib
import urllib2
import urllib#编码请求字串，用于处理验证码
import socket#用于捕获超时错误
import zlib
import pickle
import re#获取TpoicID/CollectionID时用
import os

from contentParse import *
from httpLib import *
from helper import *


class PageWorker(object):
    def __init__(self, conn = None, urlInfo = {}):
        self.conn         = conn
        self.cursor       = conn.cursor()
        self.maxPage      = ''
        self.urlInfo      = urlInfo
        self.maxThread    = urlInfo['baseSetting']['maxThread']
        self.url          = urlInfo['baseUrl']
        self.suffix       = ''
        self.addProperty()
        self.setCookie()
        self.setWorkSchedule()
        
    def getMaxPage(self, content):
        u"Don't finding unicode char in normal string"
        try:
            pos      = content.index('">下一页</a></span>')
            rightPos = content.rfind("</a>", 0, pos)
            leftPos  = content.rfind(">", 0, rightPos)
            maxPage  = int(content[leftPos+1:rightPos])
            print u"答案列表共计{}页".format(maxPage)
            return maxPage
        except:
            print u"答案列表共计1页"
            return 1
    
    def setWorkSchedule(self):
        self.workSchedule = {}
        detectUrl = self.url + self.suffix + str(self.maxPage)
        content      = self.getHttpContent(detectUrl)
        self.maxPage = self.getMaxPage(content)
        for i in range(self.maxPage):
            self.workSchedule[i] = self.url + self.suffix + str(i + 1)

    def addProperty(self):
        self.urlInfo      = urlInfo
        return
    
    #set cookieJar
    def loadCookJar(self, content = ''):
        fileName = u'./theFileNameIsSoLongThatYouWontKnowWhatIsThat.txt' 
        f = open(fileName, 'w')
        f.write(content)
        f.close()
        self.cookieJarInMemory.load(fileName)
        os.remove(fileName)
        return 

    def setCookie(self, account = ''):
        self.cookieJarInMemory = cookielib.LWPCookieJar()
        if account == '':
            Var = self.cursor.execute("select cookieStr, recordDate from LoginRecord order by recordDate desc").fetchone()
        else:
            Var = self.cursor.execute("select cookieStr, recordDate from LoginRecord order by recordDate desc where account = `{}`".format(account)).fetchone()

        cookieStr = Var[0]
        self.loadCookJar(cookieStr)
        
        cookieStr = ''
        for cookie in self.cookieJarInMemory:
            cookieStr += cookie.name + '=' + cookie.value + ';'
        self.extraHeader = {
                'User-Agent':    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:34.0) Gecko/20100101 Firefox/34.0',
                'Referer':    'www.zhihu.com/',
                'Host':   'www.zhihu.com',
                'DNT':    '1',
                'Connection': 'keep-alive',
                'Cache-Control':  'max-age=0',
                'Accept-Language':    'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                #'Accept-Encoding':    'gzip, deflate',mao si bu neng yong
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJarInMemory))
        urllib2.install_opener(self.opener)
        return 


    def getHttpContent(self, url='', extraHeader={} , data=None, timeout=5):
        u"""获取网页内容
     
        获取网页内容, 打开网页超过设定的超时时间则报错
        
        参数:
            url         一个字符串,待打开的网址
            extraHeader 一个简单字典,需要添加的http头信息
            data        需传输的数据,默认为空
            timeout     int格式的秒数，打开网页超过这个时间将直接退出，停止等待
        返回:
            pageContent 打开成功时返回页面内容，字符串或二进制数据|失败则返回空字符串
        报错:
            IOError     当解压缩页面失败时报错
        """
        if data == None:
            request = urllib2.Request(url = url)
        else:
            request = urllib2.Request(url = url, data = data)
        #add default extra header
        for headerKey in self.extraHeader.keys():
            request.add_header(headerKey, self.extraHeader[headerKey])
        #add userDefined header
        for headerKey in extraHeader.keys():
            request.add_header(headerKey, extraHeader[headerKey])
        try: 
            rawPageData = urllib2.urlopen(request, timeout = timeout)
        except  urllib2.HTTPError as error:
            print u'网页打开失败'
            print u'错误页面:' + url
            if hasattr(error, 'code'):
                print u'失败代码:' + str(error.code)
            if hasattr(error, 'reason'):
                print u'错误原因:' + error.reason
        except  urllib2.URLError as error:
            print u'网络连接异常'
            print u'错误页面:' + url
            print u'错误原因:'
            print error.reason
        except  socket.timeout as error:
            print u'打开网页超时'
            print u'超时页面' + url
        else:
            return self.decodeGZip(rawPageData)
        return ''

    def decodeGZip(self, rawPageData):
        u"""返回处理后的正常网页内容
     
        判断网页内容是否被压缩，无则直接返回，若被压缩则使用zlip解压后返回
        
        参数:
            rawPageData   urlopen()传回的fileLike object
        返回:
            pageContent   页面内容，字符串或二进制数据|解压缩失败时则返回空字符串
        报错:
            无
        """
        if rawPageData.info().get(u"Content-Encoding") == "gzip":
            try:
                pageContent = zlib.decompress(rawPageData.read(), 16 + zlib.MAX_WBITS)
            except zlib.error as ziperror:
                print u'解压出错'
                print u'出错解压页面:' + rawPageData.geturl()
                print u'错误信息：'
                print zliberror
                return ''
        else:
            pageContent = rawPageData.read()
            return pageContent

class QuestionWorker(PageWorker):
    def start(self):
        self.complete = set()
        maxTry = self.maxTry
        while maxTry > 0 and len(self.workSchedule) > 0:
            self.leader()
            maxTry -= 1
        return 
    
    def leader(self):
        threadPool = []
        self.questionInfoDictList = []
        self.answerDictList       = []
        for key in self.workSchedule:
            threadPool.append(threading.Thread(target = self.worker, kwargs = {'workNo' : key}))
        threadsCount = len(threadPool)
        threadLiving = 2
        while (threadsCount > 0 or threadLiving > 1):
            bufLength = self.maxThread - threadLiving
            if bufLength > 0 and threadsCount > 0:
                while bufLength > 0 and threadsCount > 0:
                    threadPool[threadsCount - 1].start()
                    bufLength -= 1
                    threadsCount -= 1
                    time.sleep(0.1)
            else:
                print u'正在读取答案页面，还有{}/{}张页面等待读取'.format(len(self.workSchedule) - len(self.complete), len(self.workSchedule))
                time.sleep(1)
            threadLiving = threading.activeCount()
        for questionInfoDict in self.questionInfoDictList:
            save2DB(self.cursor, questionInfoDict, 'questionIDinQuestionDesc', 'QuestionInfo')
        for answerDict in self.answerDictList:
            save2DB(self.cursor, answerDict, 'answerHref', 'AnswerContent')
        self.conn.commit()
        print 'commit complete'
        return

    def worker(self, workNo = 0):
        u"""
        worker只执行一次，待全部worker执行完毕后由调用函数决定哪些worker需要再次运行
        重复的次数由self.maxTry指定
        这样可以给知乎服务器留出生成页面缓存的时间
        """
        if workNo in self.complete:
            return
        content = self.getHttpContent(url = self.workSchedule[workNo], extraHeader = self.extraHeader, timeout = self.waitFor)
        if content == '':
            return
        parse = ParseQuestion(content)
        questionInfoDictList, answerDictList = parse.getInfoDict()
        for questionInfoDict in questionInfoDictList:
            self.questionInfoDictList.append(questionInfoDict)
        for answerDict in answerDictList:
            self.answerDictList.append(answerDict)
        self.complete.add(workNo)
        return 

    def addProperty(self):
        self.maxPage = 1
        self.suffix  = '?sort=created&page='
        self.maxTry  = 1
        self.waitFor = 5
        return

class AnswerWorker(PageWorker):
    def addProperty(self):
        self.maxPage        = ''
        self.suffix         = ''
        self.maxTry         = 1
        self.waitFor        = 5
        self.answerDictList = []
        return

    def start(self):
        maxTry = self.maxTry
        while maxTry > 0 and not self.answerDictList:
            self.leader()
            maxTry -= 1
        return 

    def leader(self):
        self.questionInfoDictList = []
        self.answerDictList       = []
        self.worker()
        for questionInfoDict in self.questionInfoDictList:
            save2DB(self.cursor, questionInfoDict, 'questionIDinQuestionDesc', 'QuestionInfo')
        for answerDict in self.answerDictList:
            save2DB(self.cursor, answerDict, 'answerHref', 'AnswerContent')
        self.conn.commit()
        print 'commit complete'
        return

    def worker(self):
        content = self.getHttpContent(url = self.url, extraHeader = self.extraHeader, timeout = self.waitFor)
        if content == '':
            return
        parse = ParseAnswer(content)
        questionInfoDictList, answerDictList = parse.getInfoDict()
        for questionInfoDict in questionInfoDictList:
            self.questionInfoDictList.append(questionInfoDict)
        for answerDict in answerDictList:
            self.answerDictList.append(answerDict)
        return


class AuthorWorker(PageWorker):
    def start(self):
        self.complete = set()
        maxTry = self.maxTry
        while maxTry > 0 and len(self.workSchedule) > 0:
            self.leader()
            maxTry -= 1
        return 
    
    def getIndexID(self):
        u'''
        用于为Topic，collection，userAgree添加Index
        '''
        return 
    
    def clearIndex(self):
        u'''
        用于在插入Index之前先清空Index表
        '''
        return

    def addIndex(self, answerHref):
        u'''
        用于插入Index
        '''
        return

    def leader(self):
        #clear index cache
        self.getIndexID()
        self.clearIndex()

        self.catchFrontInfo()
        threadPool = []
        self.questionInfoDictList = []
        self.answerDictList       = []
        for key in self.workSchedule:
            threadPool.append(threading.Thread(target = self.worker, kwargs = {'workNo' : key}))
        threadsCount = len(threadPool)
        threadLiving = 2
        while (threadsCount > 0 or threadLiving > 1):
            bufLength = self.maxThread - threadLiving
            if bufLength > 0 and threadsCount > 0:
                while bufLength > 0 and threadsCount > 0:
                    threadPool[threadsCount - 1].start()
                    bufLength -= 1
                    threadsCount -= 1
                    time.sleep(0.1)
            else:
                print u'正在读取答案页面，还有{}/{}张页面等待读取'.format(len(self.workSchedule) - len(self.complete), len(self.workSchedule))
                time.sleep(1)
            threadLiving = threading.activeCount()
        for questionInfoDict in self.questionInfoDictList:
            save2DB(self.cursor, questionInfoDict, 'questionIDinQuestionDesc', 'QuestionInfo')
        for answerDict in self.answerDictList:
            save2DB(self.cursor, answerDict, 'answerHref', 'AnswerContent')
            self.addIndex(answerDict['answerHref'])
        self.conn.commit()
        print 'commit complete'
        return
    
    def catchFrontInfo(self):
        content = self.getHttpContent(url = self.urlInfo['infoUrl'], extraHeader = self.extraHeader, timeout = self.waitFor)
        if content == '':
            return
        parse    = AuthorInfoParse(content)
        infoDict = parse.getInfoDict()
        save2DB(self.cursor, infoDict, 'authorID', 'AuthorInfo')
        return 


    def worker(self, workNo = 0):
        u"""
        worker只执行一次，待全部worker执行完毕后由调用函数决定哪些worker需要再次运行
        重复的次数由self.maxTry指定
        这样可以给知乎服务器留出生成页面缓存的时间
        """
        if workNo in self.complete:
            return
        content = self.getHttpContent(url = self.workSchedule[workNo], extraHeader = self.extraHeader, timeout = self.waitFor)
        if content == '':
            return
        parse = ParseAuthor(content)
        questionInfoDictList, answerDictList = parse.getInfoDict()
        for questionInfoDict in questionInfoDictList:
            self.questionInfoDictList.append(questionInfoDict)
        for answerDict in answerDictList:
            self.answerDictList.append(answerDict)
        self.complete.add(workNo)
        return 

    def addProperty(self):
        self.maxPage = 1
        self.suffix  = '/answers?order_by=vote_num&page='
        self.maxTry  = 1
        self.waitFor = 5
        return

class TopicWorker(AuthorWorker):
    def getIndexID(self):
        topicMatch = re.search(r'(?<=www.zhihu.com/topic/)\d{8}', self.url)
        if topicMatch == None:
            print u'抱歉，没能在网址中匹配到话题ID'
            print u'输入的话题网址为：{}'.format(self.url)
            print u'程序无法继续运行，请检查网址是否正确后重试'
            exit()
        self.topicID = topicMatch.group(0)
        return self.topicID
    
    def clearIndex(self):
        self.getIndexID()
        self.cursor.execute('delete from TopicIndex where topicID = ?', [self.topicID,])
        self.conn.commit()
        return

    def addIndex(self, answerHref):
        self.cursor.execute('replace into TopicIndex (answerHref, topicID) values (?, ?)', [answerHref, self.topicID])
        return

    def catchFrontInfo(self):
        content = self.getHttpContent(url = self.urlInfo['infoUrl'], extraHeader = self.extraHeader, timeout = self.waitFor)
        if content == '':
            return
        parse    = TopicInfoParse(content)
        infoDict = parse.getInfoDict()
        save2DB(self.cursor, infoDict, 'topicID', 'TopicInfo')
        return 

    def worker(self, workNo = 0):
        if workNo in self.complete:
            return
        content = self.getHttpContent(url = self.workSchedule[workNo], extraHeader = self.extraHeader, timeout = self.waitFor)
        if content == '':
            return
        parse = ParseTopic(content)
        questionInfoDictList, answerDictList = parse.getInfoDict()
        for questionInfoDict in questionInfoDictList:
            self.questionInfoDictList.append(questionInfoDict)
        for answerDict in answerDictList:
            self.answerDictList.append(answerDict)
        self.complete.add(workNo)
        return 

    def addProperty(self):
        self.maxPage = 1
        self.suffix  = '/top-answers?page='
        self.maxTry  = 1
        self.waitFor = 5
        return

class CollectionWorker(AuthorWorker):
    def getIndexID(self):
        collectionMatch = re.search(r'(?<=www.zhihu.com/collection/)\d{8}', self.url)
        if collectionMatch == None:
            print u'抱歉，没能在网址中匹配到收藏夹ID'
            print u'输入的收藏夹网址为：{}'.format(self.url)
            print u'程序无法继续运行，请检查网址是否正确后重试'
            exit()
        self.collectionID = collectionMatch.group(0)
        return self.collectionID

    def addIndex(self, answerHref):
        self.cursor.execute('replace into CollectionIndex (answerHref, collectionID) values (?, ?)', [answerHref, self.collectionID])
        return

    def catchFrontInfo(self):
        content = self.getHttpContent(url = self.urlInfo['infoUrl'], extraHeader = self.extraHeader, timeout = self.waitFor)
        if content == '':
            return
        parse    = CollectionInfoParse(content)
        infoDict = parse.getInfoDict()
        save2DB(self.cursor, infoDict, 'collectionID', 'CollectionInfo')
        return 

    def worker(self, workNo = 0):
        if workNo in self.complete:
            return
        content = self.getHttpContent(url = self.workSchedule[workNo], extraHeader = self.extraHeader, timeout = self.waitFor)
        if content == '':
            return
        parse = ParseCollection(content)
        questionInfoDictList, answerDictList = parse.getInfoDict()
        for questionInfoDict in questionInfoDictList:
            self.questionInfoDictList.append(questionInfoDict)
        for answerDict in answerDictList:
            self.answerDictList.append(answerDict)
        self.complete.add(workNo)
        return 

    def addProperty(self):
        self.maxPage = 1
        self.suffix  = '?page='
        self.maxTry  = 1
        self.waitFor = 5
        return
"""
class JsonWorker:
"""
