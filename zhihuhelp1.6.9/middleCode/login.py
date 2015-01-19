# -*- coding: utf-8 -*-
import cookielib
import Cookie
import urllib2
import urllib#编码请求字串，用于处理验证码
import socket#用于捕获超时错误
import zlib
import json

import time
import datetime

import re
import os
import pickle
import StringIO#使用字符串模拟一个文件

from httpLib import *
from helper import *
from setting import *
 
class Login(object):
    def __init__(self, conn):
        self.setting           = Setting()
        self.conn              = conn
        self.cursor            = conn.cursor()
        self.cookieJarInMemory = cookielib.LWPCookieJar()
        self.opener            = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJarInMemory))
        urllib2.install_opener(self.opener)

    def sendMessage(self, account, password, captcha = ''):
        xsrf = getXsrf(self.getHttpContent('http://www.zhihu.com/login'))
        if xsrf == '':
            print  u'知乎网页打开失败'
            print  u'请敲击回车重新发送登陆请求'
            return False
        _xsrf = xsrf.split('=')[1]
        #add xsrf as cookie into cookieJar,
        xsrfCookie = makeCookie(name = '_xsrf', value = _xsrf, domain='www.zhihu.com')
        self.cookieJarInMemory.set_cookie(xsrfCookie)
        if captcha == '':
            loginData = '{0}&email={1}&password={2}'.format(xsrf, account, password, ) + '&rememberme=y'
        else:
            loginData = '{0}&email={1}&password={2}&captcha={3}'.format(xsrf, account, password, captcha) + '&rememberme=y'
        loginData = urllib.quote(loginData, safe = '=&')
        header = {
                   'Accept'          : '*/*',
                   'Accept-Encoding' : 'gzip,deflate', #主要属性，只要有此项知乎即认为来源非脚本
                   'Accept-Language' : 'zh,zh-CN;q=0.8,en-GB;q=0.6,en;q=0.4',
                   'Connection'      : 'keep-alive',
                   'Host'            : 'www.zhihu.com',
                   'Content-Type'    : 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent'      : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/34.0.1847.116 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest',
                 }
        header['Origin']  = 'http://www.zhihu.com'
        header['Referer'] = 'http://www.zhihu.com/'
        
        #登陆时需要手工写urlopen，否则无法获取返回的信息
        request = urllib2.Request(url = 'http://www.zhihu.com/login', data = loginData)
        
        for headerKey in header.keys():
            request.add_header(headerKey, header[headerKey])
        
        try:
            result   = urllib2.urlopen(request)
            jsonData = zlib.decompress(result.read(), 16 + zlib.MAX_WBITS) 
            result   = json.loads(jsonData)
        except Exception as error:
            print error
            return False
        
        if result['r'] == 0:
            print u'登陆成功！'
            print u'登陆账号:', account
            print u'请问是否需要记住帐号密码？输入yes记住，输入其它任意字符跳过，回车确认'
            if raw_input() == 'yes':
                setting = {
                        'account' : account,
                        'password' : password
                        }
                self.setting.setSetting(setting)
                print u'帐号密码已保存,可通过修改setting.ini进行修改密码等操作'
            else:
                print u'跳过保存环节，进入下一流程'
            cookieJar2String = self.saveCookieJar()
            data = {}
            data['account']    = account
            data['password']   = password
            data['recordDate'] = datetime.date.today().isoformat()
            data['cookieStr']  = cookieJar2String
            save2DB(cursor = self.cursor, data = data, primaryKey = 'account', tableName = 'LoginRecord')
            self.conn.commit()
            return True
        else:
            print u'登陆失败'
            printDict(result)
            return False 
    
    def getCaptcha(self):
        buf = urllib2.urlopen(u'http://www.zhihu.com/captcha.gif')#开始拉取验证码
        f   = open(u'我是登陆知乎时的验证码.gif', 'wb')
        f.write(buf.read())
        f.close()
        print u'请输入您所看到的验证码，验证码文件在助手所处的文件夹内,\n双击打开『我是登陆知乎时的验证码.gif』即可\n如果不需要输入验证码可以直接敲击回车跳过该步'
        captcha = raw_input()
        return captcha
    
    def login(self):
        self.setting.guide()
        account, password = self.setting.guideOfAccountAndPassword()
        captcha = ''
        while not self.sendMessage(account, password, captcha):
            print u'请按照提示重新登陆'
            print u'输入『yes』后按回车可以更换账号密码，点击回车直接重新发送登录请求'
            confirm = raw_input()
            if confirm == 'yes':
                account,password = self.guideOfAccountAndPassword()
            captcha = self.getCaptcha()
        return

    def saveCookieJar(self):
        fileName = u'./theFileNameIsSoLongThatYouWontKnowWhatIsThat.txt' 
        f = open(fileName, 'w')
        f.close()
        self.cookieJarInMemory.save(fileName)
        f = open(fileName, 'r')
        content = f.read()
        f.close
        os.remove(fileName)
        return content
    
    def loadCookJar(self, content = ''):
        fileName = u'./theFileNameIsSoLongThatYouWontKnowWhatIsThat.txt' 
        f = open(fileName, 'w')
        f.write(content)
        f.close()
        self.cookieJarInMemory.load(fileName)
        os.remove(fileName)
        return 

    #这个函数暂时没有用到
    def setCookie(self, account = ''):
        if account == '':
            rowcount = self.cursor.execute('select count(cookieStr) from LoginRecord').fetchone()[0]    
            if rowcount != 0:
                Var  = self.cursor.execute("select cookieStr, recordDate from LoginRecord order by recordDate desc").fetchone()
                cookieStr  = Var[0]
                recordDate = Var[1]
                recordDate = datetime.datetime.strptime(recordDate,'%Y-%m-%d').date()#日期函数可以进一步修改
                today      = datetime.date.today()
                diff       = 20 - (today - recordDate).days
                if diff > 0:
                    print u'使用储存于' + str(recordDate) + u'的记录进行登陆。'
                    self.loadCookJar(cookieStr)
                    return True
        else:
            rowcount = self.cursor.execute('select count(cookieStr) from LoginRecord where account = `{}`'.format(account)).fetchone()[0]    
            if rowcount != 0:
                Var  = self.cursor.execute("select cookieStr, recordDate from LoginRecord order by recordDate desc where account = `{}`".format(account)).fetchone()
                cookieStr  = Var[0]
                recordDate = Var[1]
                recordDate = datetime.datetime.strptime(recordDate,'%Y-%m-%d').date()#日期函数可以进一步修改
                today      = datetime.date.today()
                diff       = 20 - (today - recordDate).days
                if diff > 0:
                    print u'使用储存于' + str(recordDate) + u'的记录进行登陆。'
                    self.loadCookJar(cookieStr)
                    return True
        return False

    def getCookieHeader(self):
        cookieStr = ''
        for cookie in self.cookieJarInMemory:
            cookieStr += cookie.name + '=' + cookie.value + ';'
        return {'Cookie': cookieStr}

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
            return decodeGZip(rawPageData)
        return ''
