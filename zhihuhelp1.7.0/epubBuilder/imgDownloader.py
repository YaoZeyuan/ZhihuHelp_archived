# -*- coding: utf-8 -*-
import time
import threading
import cookielib
import urllib2
import urllib#编码请求字串，用于处理验证码
import socket#用于捕获超时错误
import zlib

import os

class ImgDownloader():
    u'''
     负责下载图片到指定文件夹内 
    '''
    def __init__(self, targetDir = '', imgSet = set(), maxThread = 20, maxTry = 5):
        self.targetDir  = targetDir
        self.maxThread  = maxThread
        self.waitFor    = 5
        self.maxTry     = maxTry
        self.extraHeader= {}
        self.threadPool = []
        self.imgSet     = imgSet
        self.complete   = set()
        self.getCacheSet()
    
    def leader(self):
        times = 0
        while times < self.maxTry and len(self.imgSet) > 0:
            print u'开始第{}/{}遍图片下载'.format(times, self.maxTry)
            self.downloader()
            times += 1
        print u'所有图片下载完毕'
        return self.complete

    def downloader(self):
        u'''
        返回下载成功的图片列表
        '''
        threadPool = []
        for img in list(self.imgSet):
            fileName = self.getFileName(img)
            if fileName in self.cacheSet:
                self.imgSet.discard(img)
                self.complete.add(fileName)
                continue
            threadPool.append(threading.Thread(target = self.worker, kwargs = {'link' : img}))
        threadsCount = len(threadPool)
        threadLiving = 2
        while (threadsCount > 0 or threadLiving > 1):
            bufLength = self.maxThread - threadLiving
            if bufLength > 0 and threadsCount > 0:
                while bufLength > 0 and threadsCount > 0:
                    threadPool[threadsCount - 1].start()
                    bufLength    -= 1
                    threadsCount -= 1
                    time.sleep(0.1)
            else:
                print u'正在下载图片，还有{}张图片等待下载'.format(len(self.imgSet))
                time.sleep(1)
            threadLiving = threading.activeCount()
        return 

    def worker(self, link = ''):
        u"""
        worker只执行一次，待全部worker执行完毕后由调用函数决定哪些worker需要再次运行
        重复的次数由self.maxTry指定
        这样可以给知乎服务器留出生成页面缓存的时间
        """
        fileName = self.getFileName(link)
        if fileName in self.complete:
            return
        content = self.getHttpContent(url = link, timeout = self.waitFor)
        if content == '':
            return
        imgFile  = open(self.targetDir + fileName, 'wb')
        imgFile.write(content)
        imgFile.close()
        self.imgSet.discard(link)
        self.complete.add(fileName)
        return 

    def getHttpContent(self, url='', extraHeader = {} , data=None, timeout=5):
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

    def getCacheSet(self):
        self.cacheSet = set(os.listdir(self.targetDir))
        return

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

    def getFileName(self, imgHref = ''):
        return imgHref.split('/')[-1]
