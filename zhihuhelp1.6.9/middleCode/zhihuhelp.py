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

class ZhihuHelper:
    def __init__(self):
        self.conn, self.cursor = self.getCursor()
        self.cookieJarInMemory = cookielib.CookieJar();
        opener                 = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJarInMemory));
        urllib2.install_opener(opener);
        return    
    
    def getCursor(self):
        if  os.path.isfile('./ZhihuDateBase.db'):
            conn              = sqlite3.connect("./ZhihuDateBase.db")
            conn.text_factory = str
            cursor            = conn.cursor()
        else:
            conn              = sqlite3.connect("./ZhihuDateBase.db")
            conn.text_factory = str
            cursor            = conn.cursor()
            cursor.execute("""create table VarPickle(Var varchar(255), Pickle varchar(50000), primary key (Var))""")
            cursor.execute("""create table AnswerInfoTable( 
                            ID                  varchar(255)    not Null, 
                            Sign                varchar(9000)   not Null,
                            AgreeCount          int(11)         not Null, 
                            QuestionID          varchar(20)     not Null,
                            AnswerID            varchar(20)     not Null,
                            UpdateTime          date            not Null,
                            CommitCount         int(11)         not Null,
                            QuestionTitle       varchar(1000)   not Null,
                            Questionhref        varchar(255)    not Null,
                            UserName            varchar(255)    not Null,
                            UserIDLogoAdress    varchar(255)    not Null,
                            primary key(Questionhref))""")#没有数据库就新建一个
            cursor.execute("""
                            create  table AnswerContentTable (
                            AnswerContent       longtext        not Null ,
                            Questionhref        varchar(255)    not Null ,
                            primary key(Questionhref))""")
            cursor.execute("""
                            create  table   CollectionIndex(
                            CollectionID        varchar(50)     not Null,
                            Questionhref        varchar(255)    not Null,
                            primary key(CollectionID, Questionhref))""")#负责永久保存收藏夹链接，防止丢收藏
            cursor.execute("""
                            CREATE TABLE IDInfo (
                            IDLogoAdress        varchar(255)    default "http://p1.zhimg.com/da/8e/da8e974dc_m.jpg",
                            ID                  varchar(255)    not Null,
                            Sign                varchar(255)    default '',
                            Name                varchar(255)    default '',
                            Ask                 varchar(255)    default '',
                            Answer              int             default 0,
                            Post                int             default 0,
                            Collect             int             default 0,
                            Edit                int             default 0,
                            Agree               int             default 0,
                            Thanks              int             default 0,
                            Followee            int             default 0,
                            Follower            int             default 0,
                            Watched             int             default 0,
                            primary key(ID))""")#负责保存ID信息
            cursor.execute("""
                            create table CollectionInfo(
                            CollectionID        varchar(50)     not Null,
                            Title               varchar(255),
                            Description         varchar(1000),
                            AuthorName          varchar(255),
                            AuthorID            varchar(255),
                            AuthorSign          varchar(255),
                            FollowerCount       int(20)         not Null,
                            primary key(CollectionID))""")#负责保存收藏夹信息
            cursor.execute("""create table TopicInfo (
                            Title               varchar(255),
                            Adress              varchar(255),
                            LogoAddress         varchar(255),
                            Description         varchar(3000),
                            TopicID             varchar(50),
                            primary key (TopicID))""")#负责保存话题信息
            conn.commit()
        return  conn,cursor
    
    def setCookie(self):
        cursor = self.cursor
        conn   = self.conn
        rowcount = cursor.execute('select count(Pickle) from VarPickle where Var = "PostHeader"').fetchone()[0]    
        if  rowcount!=0:
            List = pickle.loads(cursor.execute("select Pickle from VarPickle where Var='PostHeader'").fetchone()[0])
            recordtime = datetime.datetime.strptime(List[0],'%Y-%m-%d').date()
            today      = datetime.date.today()
            diff       = 20 - (today - recordtime).days
            if diff > 0:
                print   u'使用储存于' + List[0] + u'的记录进行登陆。'
                self.cookieJarInMemory.set_cookie(Cookie.SimpleCookie().load(List[1]))#载入cookie
                return True
        return False
    
    def getAccountAndPassword(self):
        print   u'开始登陆流程，请根据下列提示输入您的账号密码'    
        print   u'示例:\n用户名:mengqingxue2014@qq.com\n密码：131724qingxue\n'
        print   u'请输入用户名(知乎注册邮箱),回车确认'
        account = raw_input()
        while re.search(r'\w+@[\w\.]{3,}',account) == None:
            print   u'话说，输入的账号不规范...'
            print   u'账号标准：1.必须是正确格式的邮箱\n2.邮箱用户名只能由数字、字母和下划线_构成\n3.@后面必须要有.而且长度至少为3位'
            print   u'范例：mengqingxue2014@qq.com\n5719asd@sina.cn'
            print   u'请重新输入账号，回车确认'
            account = raw_input()
        print   u'OK,请输入密码，回车确认'
        password = raw_input()
        while len(password) < 6:
            print   u'少侠，密码长度不科学啊，这年头物价飞扬民不聊生的，密码怎么说也要六位往上哇'
            print   u'范例：helloworldvia27149,9527zaizhihu~'
            print   u'请重新输入密码，回车确认'
            password = raw_input()
        print   u'开始发送登陆请求...'
        return  account, password
    
    def getCaptcha(self):
        buf = urllib2.urlopen(u'http://www.zhihu.com/captcha.gif')#开始拉取验证码
        f   = open(u"我是登陆知乎时的验证码.gif","wb")
        f.write(buf.read())
        f.close()
        print   u"请输入您所看到的验证码，验证码文件在助手所处的文件夹内,\n双击打开『我是登陆知乎时的验证码.gif』即可"
        captcha = raw_input()
        return captcha

    def login(self):
        account,password = self.getAccountAndPassword()
        captcha = ''
        while not self.messager(account, password, captcha):
            print u'请按照提示重新登陆'
            print u'请问是否需要重新输入账号密码？直接按回车继续使用原先账号，输入『yes』后按回车更换账号'
            confirm = raw_input()
            if confirm == 'yes':
                account,password = self.getAccountAndPassword()
            captcha = self.getCaptcha()
    
    def messager(self, account, password, captcha = ''):
        xsrf = getXsrf(getHttpContent('http://www.zhihu.com/login'))
        if xsrf == '':
            print  u'知乎网页打开失败'
            return False
        if captcha == '':
            loginData = '{0}&email={1}&password={2}'.format(xsrf, account, password, ) + '&rememberme=y'
        else:
            loginData = '{0}&email={1}&password={2}&captcha={3}'.format(xsrf, account, password, captcha) + '&rememberme=y'
        loginData = urllib.quote(loginData, safe='=&')
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
            for cookie  in  self.cookieJarInMemory:
                  if  cookie.name ==  'q_c1':
                      qc_1    =   'q_c1=' + cookie.value
                  if  cookie.name ==  'q_c0':
                      qc_0    =   'q_c0=' + cookie.value
            cookies = qc_1 +';'  +xsrf+'; l_c=1'+';'+qc_0  #生成cookie
            print '所使用的cookie:' + cookies
            print u'登陆成功！'
            return True
        else:
            print u'登陆失败'
            printDict(result)
            return False 

test = ZhihuHelper()
test.login()
