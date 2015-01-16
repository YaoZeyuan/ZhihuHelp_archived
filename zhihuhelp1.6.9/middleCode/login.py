# -*- coding: utf-8 -*-
import cookielib
import Cookie
import urllib2
import json

import time
import datetime

import re
import os
import pickle

from httpLib import *
from helper import *
from setting import *
 
class Login(object):
    def __init__(self, conn):
        self.setting           = Setting()
        self.conn              = conn
        self.cursor            = conn.cursor()
        self.cookieJarInMemory = cookielib.CookieJar()
        self.opener            = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJarInMemory))
        urllib2.install_opener(self.opener)

    def sendMessage(self, account, password, captcha = ''):
        xsrf = getXsrf(getHttpContent('http://www.zhihu.com/login'))
        if xsrf == '':
            print  u'知乎网页打开失败'
            print  u'请敲击回车重新发送登陆请求'
            return False
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
            for cookie in self.cookieJarInMemory:
                if  cookie.name == 'q_c1':
                    qc_1 = 'q_c1=' + cookie.value
                if  cookie.name == 'q_c0':
                    qc_0 = 'q_c0=' + cookie.value
            cookies = '{0};{1};l_c=1;{2}'.format(qc_1, xsrf, qc_0)#生成cookie
            print u'登陆成功！'
            print u'登陆账号:', account
            print u'请问是否需要记住帐号密码？输入yes记住，输入其它任意字符跳过，回车确认'
            if raw_input() == 'yes':
                setting = {
                        'account' : account,
                        'password' : password
                        }
                setSetting(setting)
                print u'帐号密码已保存,可通过修改setting.ini进行修改密码等操作'
            else:
                print u'跳过保存环节，进入下一流程'
            newHeader = (str(datetime.date.fromtimestamp(time.time()).strftime('%Y-%m-%d')), cookies)#time和datetime模块需要导入        
            data = {}
            data['Var']    = 'PostHeader'
            data['Pickle'] = pickle.dumps(newHeader)
            save2DB(cursor = self.cursor, data = data, primaryKey = 'Var', tableName = 'VarPickle')
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
        print u'请问是否要记住密码？'
        print u'输入yes记住账号密码，输入其他任意字符跳过，回车确认'
        confirm = raw_input()
        if confirm == 'yes':
            setDict = {
                    'account'  : account, 
                    'password' : password
                    }
            self.setSetting(setDict)
        return

    
    #这个函数暂时没有用到
    def setCookie(self):
        rowcount = self.cursor.execute('select count(Pickle) from VarPickle where Var = "PostHeader"').fetchone()[0]    
        if rowcount != 0:
            varList    = pickle.loads(self.cursor.execute("select Pickle from VarPickle where Var='PostHeader'").fetchone()[0])
            recordtime = datetime.datetime.strptime(varList[0],'%Y-%m-%d').date()#日期函数可以进一步修改
            today      = datetime.date.today()
            diff       = 20 - (today - recordtime).days
            if diff > 0:
                print u'使用储存于' + varList[0] + u'的记录进行登陆。'
                self.cookieJarInMemory.set_cookie(Cookie.SimpleCookie().load(varList[1]))#载入cookie
                return True
        return False

