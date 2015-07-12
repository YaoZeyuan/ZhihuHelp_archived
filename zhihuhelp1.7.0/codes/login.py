# -*- coding: utf-8 -*-
from baseClass import *

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

from setting import *
 
class Login(BaseClass, HttpBaseClass, SqlClass, CookieBaseClass):
    def __init__(self, conn):
        self.setting           = Setting()
        self.conn              = conn
        self.cursor            = conn.cursor()
        self.cookieJarInMemory = cookielib.LWPCookieJar()
        self.opener            = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJarInMemory))
        urllib2.install_opener(self.opener)

    def sendMessage(self, account, password, captcha = ''):
        xsrf = self.getXsrf(self.getHttpContent('http://www.zhihu.com/'))
        if xsrf == '':
            print  u'知乎网页打开失败'
            print  u'请敲击回车重新发送登陆请求'
            return False
        _xsrf = xsrf.split('=')[1]
        #add xsrf as cookie into cookieJar,
        xsrfCookie = self.makeCookie(name = '_xsrf', value = _xsrf, domain='www.zhihu.com')
        self.cookieJarInMemory.set_cookie(xsrfCookie)
        if captcha == '':
            loginData={'_xsrf':_xsrf,'email':account,'password':password,'remember_me':True}
        else:
            loginData={'_xsrf':_xsrf,'email':account,'password':password,'remember_me':True,'captcha':captcha}

        loginData = urllib.urlencode(loginData) 

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
        request = urllib2.Request(r'http://www.zhihu.com/login/email',loginData)
        
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
                        'password' : password,
                        'rememberAccount' : 'yes',
                        }
                self.setting.setSetting(setting)
                print u'帐号密码已保存,可通过修改setting.ini进行修改密码等操作'
            else:
                setting = {
                        'account' : '',
                        'password' : '',
                        'rememberAccount' : '',
                        }
                self.setting.setSetting(setting)
                print u'跳过保存环节，进入下一流程'
            cookieJar2String = self.saveCookieJar()
            data = {}
            data['account']    = account
            data['password']   = password
            data['recordDate'] = datetime.date.today().isoformat()
            data['cookieStr']  = cookieJar2String
            self.save2DB(cursor = self.cursor, data = data, primaryKey = 'account', tableName = 'LoginRecord')
            self.conn.commit()
            return True
        else:
            print u'登陆失败'
            self.printDict(result)
            return False 
    
    def getCaptcha(self):
        buf = urllib2.urlopen(u'http://www.zhihu.com/captcha.gif')#开始拉取验证码
        f   = open(u'我是登陆知乎时的验证码.gif', 'wb')
        f.write(buf.read())
        f.close()
        print u'请输入您所看到的验证码，验证码文件在助手所处的文件夹中,\n双击打开『我是登陆知乎时的验证码.gif』即可\n如果不需要输入验证码可以直接敲击回车跳过该步'
        captcha = raw_input()
        return captcha
    
    def login(self):
        self.setting.guide()
        account, password = self.setting.guideOfAccountAndPassword()
        captcha = ''
        while not self.sendMessage(account, password, captcha):
            print u'啊哦，登录失败了'
            print u'请问是否需要更换登陆账号？输入『yes』后按回车可以更换账号密码'
            print u'或者猛击回车进入获取验证码的流程'
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
        f.close()
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

    def getXsrf(self, content=''):
        u'''
        提取xsrf信息
        '''
        xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', content)
        if xsrf == None:
            return ''
        else:
            return '_xsrf=' + xsrf.group(0)
