# -*- coding: utf-8 -*-
import os
import sys
import threading
import uuid  # 生成线程唯一ID，用于控制线程数


class BaseClass(object):
    u'''
    用于存放常用函数
    '''

    # 辅助函数
    def printInOneLine(text = ''):#Pass
        u"""
            *   功能
                *   反复在一行内输出内容
                *   输出前会先将光标移至行首，输出完毕后不换行
            *   输入
                *   待输出字符
            *   返回
                *  无
         """
        try:
            sys.stdout.write("\r"+" "*60+'\r')
            sys.stdout.flush()
            sys.stdout.write(text)
            sys.stdout.flush()
        except:
            pass
        return

    def printDict(self, data = {}, key = '', prefix = ''):
        if isinstance(data, dict):
            for key in data.keys():
                self.printDict(data[key], key, prefix + '   ')
        else:
            print prefix + str(key) + ' => ' + str(data)
        return

    def printCurrentDir(self):
        print os.path.realpath('.')
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
            BaseClass.mkdir(path)
            os.chdir(path)
        return

class SettingClass(object):
    u"""
    用于储存、获取设置值、全局变量值
    """
    # 全局变量

    # 默认数据库名称
    dataBaseFileName = u'./zhihuDB_171.db'

    MAXTHREAD       = 20           # 最大线程数
    PICQUALITY      = 1            # 图片质量（0/1/2，无图/标清/原图）
    MAXQUESTION     = 100          # 每本电子书中最多可以放多少本书
    MAXTRY          = 5            # 最大尝试次数
    ANSWERORDERBY   = 'agree'      # 答案排序原则
    QUESTIONORDERBY = 'agreeCount' # 问题排序原则

class TestClass(object):
    u"""
    用于存放测试用变量
    """
    # 测试变量
    test_chekcUpdate_flag     = False
    test_catchAnswerData_flag = False
    test_buffer_flag          = False
    #test_chekcUpdate_flag = False
    #test_chekcUpdate_flag = False

class ThreadClass(object):
    u"""
    用于添加常用的线程控制函数
    """
    # 线程相关
    # 线程ID池(用于控制线程数)
    threadIDPool = set()

    mutex = threading.Lock()

    def getUUID(self):
        u'''
        获取由python官方库生成的，永不重复的128位int型ID
        '''
        return uuid.uuid1().__int__()

    def getThreadCount(self):
        return len(ThreadClass.threadIDPool)

    def acquireThreadPoolPassport(self, threadID):
        ThreadClass.mutex.acquire()
        # 每次只允许向队列中添加一个线程ID，以此来控制当前运行线程数
        if ThreadClass.getThreadCount() < ThreadClass.MAXTHREAD:
            ThreadClass.threadIDPool.add(threadID)
            ThreadClass.mutex.release()
            return True
        else:
            ThreadClass.mutex.release()
            return False

    def releaseThreadPoolPassport(self, threadID):
        ThreadClass.mutex.acquire()
        ThreadClass.threadIDPool.discard(threadID)
        ThreadClass.mutex.release()

    def threadWorker(self, function):
        u"""
        实现线程池功能，传入待工作的函数，自动完成线程数量控制
        """
        return

    def waitForThreadRunningCompleted(self):
        # 等待所有线程执行完毕, 用于启动线程时控制线程数量
        while ThreadClass.getThreadCount() > ThreadClass.MAXTHREAD:
            time.sleep(0.1)
        return
    
class SqlClass(object):
    u'''
    用于存放常用的sql代码
    '''
    def save2DB(self, cursor, data={}, primaryKey='', tableName=''):
        u"""
            *   功能
                *   提供一个简单的数据库储存函数，按照data里的设定，将值存入键所对应的数据库中
                *   若数据库中没有对应数据，执行插入操作，否则执行更新操作
                *   表与主键由tableName ，primarykey指定
                *   注意，本函数不进行提交操作
            *   输入
                *   cursor
                    *   数据库游标
                *   data
                    *   需要存入数据库中的键值对
                    *   键为数据库对应表下的列名，值为列值
                *   primarykey
                    *   用于指定主键
                *   tableName
                    *   用于指定表名
            *   返回
                 *   无
         """
        replaceSql   = 'replace into '+ tableName +' ('
        placeholder = ') values ('
        varTuple = []
        for columnKey in data:
            replaceSql  += columnKey + ','
            placeholder += '?,'
            varTuple.append(data[columnKey])
    
        cursor.execute(replaceSql[:-1] + placeholder[:-1] + ')', tuple(varTuple))
        return

import urllib2
import urllib#编码请求字串，用于处理验证码
import socket#用于捕获超时错误
import zlib
import json
        
class HttpBaseClass(object):
    u'''
    用于存放常用Http函数
    '''

    def getHttpContent(self, url = '', extraHeader = {} , data = None, timeout = 5):
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
            try:
                return self.decodeGZip(rawPageData)
            except socket.timeout as error:
                print u'打开网页超时'
                print u'超时页面' + url
                print u'错误信息'
                print error
                return ''
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
            except zlib.error as zlibError:
                print u'解压出错'
                print u'出错解压页面:' + rawPageData.geturl()
                print u'错误信息：'
                print zlibError
                return ''
        else:
            pageContent = rawPageData.read()
        return pageContent

import cookielib
import time

class CookieBaseClass(object):
    u'''
    本类负责处理与cookie相关事宜
    '''
    def makeCookie(self, name, value, domain):
        cookie = cookielib.Cookie(
                version=0,
                name=name,
                value=value,
                port=None,
                port_specified=False,
                domain=domain,
                domain_specified=True,
                domain_initial_dot=False,
                path="/",
                path_specified=True,
                secure=False,
                expires=time.time() + 300000000,
                discard=False,
                comment=None,
                comment_url=None,
                rest={}
                )
        return cookie
    
