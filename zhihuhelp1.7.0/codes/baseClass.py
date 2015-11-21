# -*- coding: utf-8 -*-
import os
import sys
import threading
import traceback
import uuid  # 生成线程唯一ID，用于控制线程数
import logging
import logging.handlers


class BaseClass(object):
    u'''
    用于存放常用函数
    '''
    handler = logging.StreamHandler()  # 实例化handler
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler.setFormatter(formatter)  # 为handler添加formatter

    logger = logging.getLogger('main')  # 获取名为main的logger
    logger.addHandler(handler)  # 为logger添加handler
    #logger.setLevel(logging.INFO)  # 发布时关闭log输出
    logger.setLevel(logging.DEBUG)  # debug模式
    # 辅助函数
    @staticmethod
    def printInOneLine(text=''):  # Pass
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
            sys.stdout.write("\r" + " " * 60 + '\r')
            sys.stdout.flush()
            sys.stdout.write(text)
            sys.stdout.flush()
        except:
            pass
        return

    @staticmethod
    def printDict(data={}, key='', prefix=''):
        try:
            if isinstance(data, dict):
                for key in data.keys():
                    BaseClass.printDict(data[key], key, prefix + '   ')
            else:
                if isinstance(data, basestring):
                    print prefix + unicode(key) + ' => ' + data
                else:
                    print prefix + unicode(key) + ' => ' + unicode(data)
        except UnicodeEncodeError as error:
            BaseClass.logger.info(u'printDict中编码异常')
            BaseClass.logger.info(u'系统默认编码为：' + sys.getdefaultencoding())
            raise error
        return

    @staticmethod
    def printCurrentDir():
        print os.path.realpath('.')

    @staticmethod
    def mkdir(path):
        try:
            os.mkdir(path)
        except OSError:
            print u'指定目录已存在'
        return

    @staticmethod
    def chdir(path):
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
    dataBaseFileName = u'./zhihuDB_172.db'

    UPDATETIME = '2015-11-21'  # 更新日期

    ACCOUNT = 'mengqingxue2014@qq.com'  # 默认账号密码
    PASSWORD = '131724qingxue'  #
    REMEMBERACCOUNT = False  # 是否使用已有密码
    MAXTHREAD = 10  # 最大线程数
    PICQUALITY = 1  # 图片质量（0/1/2，无图/标清/原图）
    MAXQUESTION = 100  # 每本电子书中最多可以放多少个问题
    MAXTRY = 5  # 最大尝试次数
    ANSWERORDERBY = 'agree'  # 答案排序原则
    QUESTIONORDERBY = 'agreeCount'  # 问题排序原则
    THREADMODE = False  # 线程模式：为False时所有任务均在主线程上执行，用于调试错误
    PRIVATE = True
    WAITFOR_PIC = 10
    WAITFOR_HTML = 5


class TestClass(object):
    u"""
    用于存放测试用变量
    """
    # 测试变量
    test_chekcUpdate_flag = False
    test_catchAnswerData_flag = False
    test_buffer_flag = False
    # test_chekcUpdate_flag = False
    # test_chekcUpdate_flag = False


class ThreadClass(object):
    u"""
    用于添加常用的线程控制函数
    """
    # 线程相关
    # 线程ID池(用于控制线程数)
    threadIDPool = set()

    mutex = threading.Lock()
    threadRegisterLock = threading.Lock()

    @staticmethod
    def getUUID():
        u'''
        获取由python官方库生成的，永不重复的128位int型ID
        '''
        return uuid.uuid1().__int__()

    @staticmethod
    def getThreadCount():
        return len(ThreadClass.threadIDPool)

    @staticmethod
    def acquireThreadPoolPassport(threadID):
        ThreadClass.mutex.acquire()
        # 每次只允许向队列中添加一个线程ID，以此来控制当前运行线程数
        if ThreadClass.getThreadCount() < SettingClass.MAXTHREAD:
            ThreadClass.threadIDPool.add(threadID)
            ThreadClass.mutex.release()
            ThreadClass.registerThreadCompleted()
            return True
        else:
            ThreadClass.mutex.release()
            return False

    @staticmethod
    def startRegisterThread():
        BaseClass.logger.debug(u"开始注册新线程")
        BaseClass.logger.debug(u'当前已注册线程数:' + str(ThreadClass.getThreadCount()))
        return ThreadClass.threadRegisterLock.acquire()

    @staticmethod
    def registerThreadCompleted():
        BaseClass.logger.debug(u"新线程注册完毕")
        BaseClass.logger.debug(u'当前活跃线程数:' + str(ThreadClass.getThreadCount()))
        try:
            ThreadClass.threadRegisterLock.release()
        except threading.ThreadError as error:
            if SettingClass.THREADMODE:
                BaseClass.logger.debug(u"错误：释放了一个未被锁定的线程锁")
                BaseClass.logger.debug(u"ThreadClass.threadRegisterLock出现问题，请及时修复")
                raise error
            else:
                pass
        return

    @staticmethod
    def releaseThreadPoolPassport(threadID):
        ThreadClass.mutex.acquire()
        ThreadClass.threadIDPool.discard(threadID)
        ThreadClass.mutex.release()

    @staticmethod
    def threadWorker(function):
        u"""
        实现线程池功能，传入待工作的函数，自动完成线程数量控制
        """
        return

    @staticmethod
    def waitForSecond(second):
        u"休眠n秒"
        time.sleep(second)
        return

    @staticmethod
    def waitForThreadRunningCompleted(maxThread=-1):
        # 等待所有线程执行完毕, 用于启动线程时控制线程数量
        threadLockCount = maxThread
        if threadLockCount == -1:
            threadLockCount = SettingClass.MAXTHREAD
        BaseClass.logger.debug(u'进入waitForThreadRunningCompleted，等待所有线程运行完毕\n' + u'当前运行线程数 : ' + str(
            ThreadClass.getThreadCount()) + u'\t允许的最大线程数:' + str(threadLockCount) + '\n' + u'开始检测线程数是否符合要求')
        while ThreadClass.getThreadCount() > threadLockCount:
            time.sleep(0.1)
        BaseClass.logger.debug(
            u'线程数已符合允许的最大线程数的要求，允许的最大线程数为：' + str(threadLockCount) + u' 当前运行的线程数为：' + str(ThreadClass.getThreadCount()))
        return


class SqlClass(object):
    u'''
    用于存放常用的sql代码
    '''

    @staticmethod
    def save2DB(cursor, data={}, table_name=''):
        sql = "replace into {table_name} ({columns}) values ({items})".format(table_name=table_name,
                                                                              columns=','.join(data.keys()),
                                                                              items=(',?' * len(data.keys()))[1:])
        BaseClass.logger.debug(sql)
        cursor.execute(sql, tuple(data.values()))
        return


import urllib2
import socket  # 用于捕获超时错误
import zlib


class HttpBaseClass(object):
    u'''
    用于存放常用Http函数
    '''

    def getHttpContent(self, url='', extraHeader={}, data=None, timeout=5):
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
        request = urllib2.Request(url=url, data=data)
        for headerKey in extraHeader.keys():
            request.add_header(headerKey, extraHeader[headerKey])

        try:
            response = urllib2.urlopen(request, timeout=timeout)
        except urllib2.HTTPError as error:
            BaseClass.logger.info(u'网页打开失败')
            BaseClass.logger.info(u'错误页面:{}'.format(url))
            BaseClass.logger.info(u'失败代码:{}'.format(error.code))
            BaseClass.logger.info(u'错误原因:{}'.format(error.reason))
        except urllib2.URLError as error:
            BaseClass.logger.info(u'网络连接异常')
            BaseClass.logger.info(u'错误页面:{}'.format(url))
            BaseClass.logger.info(u'错误原因:{}'.format(error.reason))
        except socket.timeout as error:
            BaseClass.logger.info(u'打开网页超时')
            BaseClass.logger.info(u'超时页面:{}'.format(url))
        except:
            BaseClass.logger.info(u'未知错误')
            BaseClass.logger.info(u'错误页面:{}'.format(url))
            BaseClass.logger.info(u'错误堆栈信息:{}'.format(traceback.format_exc()))
        return self.unpack_response(response)

    def unpack_response(self, response):
        try:
            content = response.read()
        except socket.timeout as error:
            BaseClass.logger.info(u'打开网页超时')
            BaseClass.logger.info(u'超时页面:{}'.format())
            return ''

        decode = response.info().get(u"Content-Encoding")
        if u"gzip" in decode:
            content = HttpBaseClass.ungzip(content)
        return content

    @staticmethod
    def ungzip(content):
        try:
            content = zlib.decompress(content, 16 + zlib.MAX_WBITS)
        except zlib.error as error:
            BaseClass.logger.info(u'解压出错')
            BaseClass.logger.info(u'错误信息:{}'.format(error))
            return ''
        return content

import cookielib
import time


class BaseCookie(object):
    u'''
    本类负责处理与cookie相关事宜
    '''

    @staticmethod
    def makeCookie(name, value, domain):
        cookie = cookielib.Cookie(version=0, name=name, value=value, port=None, port_specified=False, domain=domain,
                                  domain_specified=True, domain_initial_dot=False, path="/", path_specified=True,
                                  secure=False, expires=time.time() + 300000000, discard=False, comment=None,
                                  comment_url=None, rest={})
        return cookie
