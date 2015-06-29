# -*- coding: utf-8 -*-
from baseClass import *

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
import json#用于JsonWorker
import datetime#用于格式化专栏文章的发布时间

from contentParse import *


class PageWorker(BaseClass, HttpBaseClass, SqlClass):
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
        u"""
        获取私人收藏夹时需要携cookie登陆
        但专栏不需要，所以专栏处又重载了一回
        """
        self.workSchedule = {}
        detectUrl = self.url + self.suffix + str(self.maxPage)
        content      = self.getHttpContent(url = detectUrl, extraHeader = self.extraHeader)
        self.maxPage = self.getMaxPage(content)
        for i in range(self.maxPage):
            self.workSchedule[i] = self.url + self.suffix + str(i + 1)

    def addProperty(self):
        return
 
    def commitSuccess(self):
        print u'答案录入数据库成功'
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
                # 'Accept-Encoding':    'gzip, deflate', 貌似没用
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJarInMemory))
        urllib2.install_opener(self.opener)
        return 

class QuestionQueenWorker(PageWorker):
    u"""
    对问题队列进行处理
    对于页面跳转问题，可以以这个问题作为测试用例
    http://www.zhihu.com/question/21230473?sort=created&nr=1&page=2
    """
    def __init__(self, conn = None, taskQueen = []):
        self.conn         = conn
        self.cursor       = conn.cursor()
        self.taskQueen    = taskQueen
        self.suffix       = ''  # 由addProperty负责重载
        self.addProperty()
        self.setCookie()
        self.setWorkSchedule()

    def setWorkSchedule(self):
        u"""
        需要携cookie读取网页内容
        初始化待收集页面列表
        """
        self.workSchedule = {}
        workerNo = 0
        completeFlag = False
        while not completeFlag:
            completeFlag = True #放置于前，避免taskQueen为空
            for urlInfo in self.taskQueen:
                if 'maxPage' in urlInfo:
                    continue
                else:
                    completeFlag = False
                    t = threading.Thread(target = self.detectMaxPage, kwargs = {'urlInfo' : urlInfo})
                    t.start()
                    ThreadClass.waitForThreadRunningCompleted()

        for urlInfo in self.taskQueen:
            for i in range(urlInfo['maxPage']):
                self.workSchedule[workerNo] = urlInfo['baseUrl'] + self.suffix + str(i + 1)
                workerNo += 1

    def detectMaxPage(self, urlInfo):
        # 通过全球唯一的uuid来实现对线程数的控制
        threadID = ThreadClass.getUUID()
        while not ThreadClass.acquireThreadPoolPassport(threadID):
            time.sleep(0.1)
        detectUrl = urlInfo['baseUrl'] + self.suffix + str(self.maxPage)# 检测问题的最大页数, 使用maxPage, 为扩展留出空间
        content   = self.getHttpContent(url = detectUrl, extraHeader = self.extraHeader)
        if len(content) != 0:
            urlInfo['maxPage'] = self.getMaxPage(content)
        else:
            urlInfo['tryCount'] = urlInfo.get('tryCount', 0) + 1
            if urlInfo['tryCount'] >= ThreadClass.MAXTRY:
                urlInfo['maxPage'] = 1
        ThreadClass.releaseThreadPoolPassport(threadID)
        return

    def start(self):
        self.complete = set()
        maxTry = SettingClass.MAXTRY
        while maxTry > 0 and len(self.workSchedule) > len(self.complete):
            #只要完成数等于workSchedule即可宣告完成
            self.leader()
            maxTry -= 1
        return 
    
    def leader(self):
        self.questionInfoDictList = []
        self.answerDictList       = []
        index = 0
        workScheduleLength = len(self.workSchedule)
        for key in self.workSchedule:
            index += 1
            t = threading.Thread(target = self.worker, kwargs = {'workNo' : key})
            t.start()
            BaseClass.printInOneLine(u'正在读取答案页面，还有{}/{}张页面等待读取'.format(workScheduleLength - index, workScheduleLength))
            ThreadClass.waitForThreadRunningCompleted()
        for questionInfoDict in self.questionInfoDictList:
            self.save2DB(self.cursor, questionInfoDict, 'questionIDinQuestionDesc', 'QuestionInfo')
        for answerDict in self.answerDictList:
            self.save2DB(self.cursor, answerDict, 'answerHref', 'AnswerContent')
        self.conn.commit()
        self.commitSuccess()
        return

    def worker(self, workNo = 0):
        u"""
        完成线程控制工作，实际工作由realWork完成
        """
        if workNo in self.complete:
            return
        threadID = ThreadClass.getUUID()
        while not ThreadClass.acquireThreadPoolPassport(threadID):
            time.sleep(0.1)
        result = self.realWorker(workNo)
        if result :
            self.complete.add(workNo)
        ThreadClass.releaseThreadPoolPassport()
        return

    def realWorker(self, workNo = 0):
        u"""
        worker只执行一次，待全部worker执行完毕后由调用函数决定哪些worker需要再次运行
        重复的次数由self.maxTry指定
        这样可以给知乎服务器留出生成页面缓存的时间
        """
        content = self.getHttpContent(url = self.workSchedule[workNo], extraHeader = self.extraHeader, timeout = self.waitFor)
        if content == '':
            return False
        parse = ParseQuestion(content)
        questionInfoDictList, answerDictList = parse.getInfoDict()
        for questionInfoDict in questionInfoDictList:
            self.questionInfoDictList.append(questionInfoDict)
        for answerDict in answerDictList:
            self.answerDictList.append(answerDict)
        return True

    def addProperty(self):
        self.maxPage = 1
        self.suffix  = '?nr=1&sort=created&page='  # 按时间对答案排序，同时屏蔽跳转
        self.maxTry  = 5
        self.waitFor = 5
        return

class AnswerQueenWorker(QuestionQueenWorker):
    def addProperty(self):
        self.maxPage        = ''
        self.suffix         = ''
        self.answerDictList = []
        return

    def setWorkSchedule(self):
        u"""
        需要携cookie读取网页内容
        初始化待收集页面列表
        """
        self.workSchedule = {}
        workerNo = 0
        for urlInfo in self.taskQueen:
            self.workSchedule[workerNo] = urlInfo['baseUrl']
            workerNo += 1

    def realWorker(self, workNo = 0):
        content = self.getHttpContent(url = self.url, extraHeader = self.extraHeader)
        if content == '':
            return False
        parse = ParseAnswer(content)
        questionInfoDictList, answerDictList = parse.getInfoDict()
        for questionInfoDict in questionInfoDictList:
            self.questionInfoDictList.append(questionInfoDict)
        for answerDict in answerDictList:
            self.answerDictList.append(answerDict)
        return True

class AuthorWorker(PageWorker):
    def start(self):
        self.complete = set()
        maxTry = SettingClass.MAXTRY
        while maxTry > 0 and len(self.workSchedule) > len(self.complete):
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
        #self.clearIndex()

        self.catchFrontInfo()
        self.questionInfoDictList = []
        self.answerDictList       = []
        for key in self.workSchedule:
            t = threading.Thread(target = self.worker, kwargs = {'workNo' : key})
            t.start()
            ThreadClass.waitForThreadRunningCompleted()
            BaseClass.printInOneLine(u'正在读取答案页面，还有{}/{}张页面等待读取'.format(len(self.workSchedule) - len(self.complete), len(self.workSchedule)))
        for questionInfoDict in self.questionInfoDictList:
            self.save2DB(self.cursor, questionInfoDict, 'questionIDinQuestionDesc', 'QuestionInfo')
        for answerDict in self.answerDictList:
            self.save2DB(self.cursor, answerDict, 'answerHref', 'AnswerContent')
            self.addIndex(answerDict['answerHref'])
        self.conn.commit()
        self.commitSuccess()
        return
    
    def catchFrontInfo(self):
        content = self.getHttpContent(url = self.urlInfo['infoUrl'], extraHeader = self.extraHeader, timeout = self.waitFor)
        if content == '':
            return
        parse    = AuthorInfoParse(content)
        infoDict = parse.getInfoDict()
        self.save2DB(self.cursor, infoDict, 'authorID', 'AuthorInfo')
        return 

    def worker(self, workNo = 0):
        u"""
        完成线程控制工作，实际工作由realWorker完成
        """
        if workNo in self.complete:
            return
        threadID = 0  # 初始化threadID值
        try:
            threadID = ThreadClass.getUUID()
            while not ThreadClass.acquireThreadPoolPassport(threadID):
                time.sleep(0.1)
            result = self.realWorker(workNo)
            if result:
                self.complete.add(workNo)
        except Exception as e:
            print e #  输出异常信息
        finally:
            #无论发生什么，都必须执行该函数
            ThreadClass.releaseThreadPoolPassport(threadID)
        return

    def realWorker(self, workNo = 0):
        u"""
        realWorker只执行一次，待全部worker执行完毕后由调用函数决定哪些worker需要再次运行
        重复的次数由self.maxTry指定
        这样可以给知乎服务器留出生成页面缓存的时间
        """
        content = self.getHttpContent(url = self.workSchedule[workNo], extraHeader = self.extraHeader, timeout = self.waitFor)
        if content == '':
            return False
        parse = ParseAuthor(content)
        questionInfoDictList, answerDictList = parse.getInfoDict()
        for questionInfoDict in questionInfoDictList:
            self.questionInfoDictList.append(questionInfoDict)
        for answerDict in answerDictList:
            self.answerDictList.append(answerDict)
        return True

    def addProperty(self):
        self.maxPage = 1
        self.suffix  = '/answers?order_by=vote_num&page='
        self.maxTry  = SettingClass.MAXTRY
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
        content = self.getHttpContent(url = self.urlInfo['infoUrl'], extraHeader = self.extraHeader)
        if content == '':
            return
        parse    = TopicInfoParse(content)
        infoDict = parse.getInfoDict()
        self.save2DB(self.cursor, infoDict, 'topicID', 'TopicInfo')
        return 

    def realWorker(self, workNo = 0):
        content = self.getHttpContent(url = self.workSchedule[workNo], extraHeader = self.extraHeader)
        if content == '':
            return False
        parse = ParseTopic(content)
        questionInfoDictList, answerDictList = parse.getInfoDict()
        for questionInfoDict in questionInfoDictList:
            self.questionInfoDictList.append(questionInfoDict)
        for answerDict in answerDictList:
            self.answerDictList.append(answerDict)
        return True

    def addProperty(self):
        self.maxPage = 1
        self.suffix  = '/top-answers?page='
        self.maxTry  = 5
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
        self.save2DB(self.cursor, infoDict, 'collectionID', 'CollectionInfo')
        return 

    def realWorker(self, workNo = 0):
        content = self.getHttpContent(url = self.workSchedule[workNo], extraHeader = self.extraHeader, timeout = self.waitFor)
        if content == '':
            return False
        parse = ParseCollection(content)
        questionInfoDictList, answerDictList = parse.getInfoDict()
        for questionInfoDict in questionInfoDictList:
            self.questionInfoDictList.append(questionInfoDict)
        for answerDict in answerDictList:
            self.answerDictList.append(answerDict)
        return 

    def addProperty(self):
        self.maxPage = 1
        self.suffix  = '?page='
        self.maxTry  = 5
        self.waitFor = 5
        return

class JsonWorker(PageWorker):
    u'''
    用于获取返回值为Json格式的网页内容
    '''
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
        return
    
    def getJsonContent(self, url = '', extraHeader = {} , data = None, timeout = 5):
        u'''
        对获取json内容进行的封装，打开成功时返回解析后的字典，打开失败则返回空字典
        '''
        content = self.getHttpContent(url = url, extraHeader = extraHeader, data = data, timeout = timeout)
        if content == '':
            return {}
        else:
            return json.loads(content)

class ColumnWorker(JsonWorker):
    def setCookie(self):
        u'''
        专栏不需要登陆
        '''
        self.extraHeader = {}
        return
    def commitSuccess(self):
        print u'专栏文章录入数据库成功'
        return

    def addProperty(self):
        self.maxPage    = 1
        self.suffix     = ''
        self.maxTry     = 5
        self.waitFor    = 5

        self.columnInfo = {}
        return

    def getColumnInfo(self):
        rawInfo = self.getJsonContent(url = 'http://zhuanlan.zhihu.com/api/columns/' + self.urlInfo['columnID'])
        if not rawInfo:
            return False

        self.columnInfo['creatorID']   = rawInfo['creator']['slug']
        self.columnInfo['creatorHash'] = rawInfo['creator']['hash']
        self.columnInfo['creatorSign'] = rawInfo['creator']['bio']
        self.columnInfo['creatorName'] = rawInfo['creator']['name']
        self.columnInfo['creatorLogo'] = rawInfo['creator']['avatar']['template'].replace('{id}', rawInfo['creator']['avatar']['id']).replace('_{size}', '_r')

        self.columnInfo['columnID']       = rawInfo['slug']
        self.columnInfo['columnName']     = rawInfo['name']
        self.columnInfo['columnLogo']     = rawInfo['creator']['avatar']['template'].replace('{id}', rawInfo['avatar']['id']).replace('_{size}', '_r')
        self.columnInfo['articleCount']   = rawInfo['postsCount']
        self.columnInfo['followerCount']  = rawInfo['followersCount'] 
        self.columnInfo['description']    = rawInfo['description']
        return True

    def setWorkSchedule(self):
        print u'开始获取专栏信息'
        maxTry = self.maxTry
        while maxTry > 0 and not self.getColumnInfo():
            maxTry -= 1
            print u'第{}次尝试获取专栏信息失败'.format(self.maxTry - maxTry)
        if not self.columnInfo:
            print u'获取专栏信息失败，请检查专栏地址是否正确后重试。打开失败的专栏地址为:{}'.format(self.url)
            return
        else:
            print u'获取专栏信息成功'
        self.workSchedule = {}
        detectUrl = 'http://zhuanlan.zhihu.com/api/columns/{}/posts?limit=10&offset='.format(self.urlInfo['columnID'])
        for i in range(self.columnInfo['articleCount']/10 + 1):
            self.workSchedule[i] = detectUrl + str(i * 10)
        #将专栏信息储存至数据库中
        self.save2DB(self.cursor, self.columnInfo, 'columnID', 'ColumnInfo')
        self.conn.commit()
        return

    def start(self):
        self.complete = set()
        if not self.columnInfo:
            return
        maxTry = self.maxTry
        while maxTry > 0 and len(self.workSchedule) > len(self.complete):
            self.leader()
            maxTry -= 1
        return 
    
    def leader(self):
        threadPool = []
        self.articleList = []
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
                print u'正在读取专栏页面，还有{}/{}张页面等待读取'.format(len(self.workSchedule) - len(self.complete), len(self.workSchedule))
                time.sleep(1)
            threadLiving = threading.activeCount()

        for article in self.articleList:
            self.save2DB(self.cursor, article, 'articleHref', 'ArticleContent')
        self.conn.commit()
        self.commitSuccess()
        return

    def worker(self, workNo = 0):
        u"""
        worker只执行一次，待全部worker执行完毕后由调用函数决定哪些worker需要再次运行
        重复的次数由self.maxTry指定
        这样可以给知乎服务器留出生成页面缓存的时间
        """
        if workNo in self.complete:
            return

        content = self.getJsonContent(url = self.workSchedule[workNo], extraHeader = self.extraHeader, timeout = self.waitFor)

        if not content:
            return
        self.formatJsonArticleData(content)
        self.complete.add(workNo)
        return 
    
    def formatJsonArticleData(self, rawArticleList = []):
        for rawArticle in rawArticleList: 
            article = {}
            article['authorID']       = rawArticle['author']['slug']  
            article['authorHash']     = rawArticle['author']['hash']
            article['authorSign']     = rawArticle['author']['bio']
            article['authorName']     = rawArticle['author']['name']
            article['authorLogo']     = rawArticle['author']['avatar']['template'].replace('{id}', rawArticle['author']['avatar']['id']).replace('_{size}', '_r')

            article['columnID']       = rawArticle['column']['slug']
            article['columnName']     = rawArticle['column']['name']
            article['articleID']      = rawArticle['slug']
            article['articleHref']    = u'http://zhuanlan.zhihu.com/{columnID}/{articleID}'.format(**article)
            article['title']          = rawArticle['title']
            article['titleImage']     = rawArticle['titleImage']
            article['articleContent'] = rawArticle['content']    
            article['commentCount']   = rawArticle['commentsCount']   
            article['likeCount']      = rawArticle['likesCount']
            article['publishedTime']  = self.formatPublishedTime(rawArticle['publishedTime'])   
            self.articleList.append(article)
        return 

    def formatPublishedTime(self, publishedTime = ''):
        if not publishedTime:
            return datetime.date.today().isoformat()
        else:
            return datetime.datetime.strptime(publishedTime, '%Y-%m-%dT%H:%M:%S+08:00').strftime('%Y-%m-%d')
