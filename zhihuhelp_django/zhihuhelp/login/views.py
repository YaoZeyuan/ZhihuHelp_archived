# -*- coding: utf-8 -*-

from django.http      import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response

#获取配置信息
from django.conf import settings

from zhihuhelp.login  import *
from zhihuhelp.login.models  import *
from zhihuhelp.lib.helper  import *
from zhihuhelp.lib.httpLib import *

import json
import cookielib

#验证时间
import time
import datetime
#下载验证码
import os

#初始化时的工作
cookieJarInMemory = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJarInMemory))
urllib2.install_opener(opener)
print u'初始化成功'


def login(request):
    print u'登陆流程开始'
    if request.POST.get('account') != '' and request.POST.get('password') != '':
        account  = request.POST.get('account')  
        password = request.POST.get('password')
        
        try:
            userInfo   = User.objects.get(account = account)
            today      = datetime.date.today()                                            
            diff       = 30 - (today - userInfo.loginDate).days                             
            if diff > 0:
                print u'登陆成功'
                print u'距离cookie过期日期还有{}天'.format(diff)
                return HttpResponse(json.dumps({'r':0, 'msg':{'':''}}))
        except User.DoesNotExist:
            userInfo   = User(account = account)
            print u'数据库中没有可用记录，开始登陆流程'
        
        captcha  = request.POST.get('captcha')
        xsrf     = getXsrf(getHttpContent('http://www.zhihu.com/login'))
        if xsrf != '':
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
                return HttpResponse(json.dumps({'r':1, 'msg':{'httpError':u'403错误，助手的登陆请求被知乎无情拒绝了，请稍后重试\n错误信息:' + str(error)}}))
            
            #若result为空，则要么登陆成功，要么知乎故障，假定登陆成功吧
            if result['r'] == 0:
                for cookie  in  cookieJarInMemory:
                      if  cookie.name ==  'q_c1':
                          qc_1    =   'q_c1=' + cookie.value
                      if  cookie.name ==  'q_c0':
                          qc_0    =   'q_c0=' + cookie.value
                cookies = qc_1 +';'  +xsrf+'; l_c=1'+';'+qc_0  #生成cookie
                userInfo.cookies = cookies    
                userInfo.save()
                print u'登陆成功！'
            else:
                print u'登陆失败'
                printDict(result)
            return HttpResponse(jsonData)
        else:
            return HttpResponse(json.dumps({'r':1, 'msg':{'wrong':u'知乎网站打开失败, 直接使用数据库调取cookie失败，请重新登陆'}}))

def index(request):
    return render_to_response('login.html')

def getCaptcha(Request):
    new_checkcode_url = u'http://www.zhihu.com/captcha.gif?r=' + str(int(time.time()))  #验证码网址，通过cookie鉴别身份
    buf = urllib2.urlopen(url=new_checkcode_url)  #开始拉取验证码

    static = os.path.join(os.path.dirname(__file__), '../static').replace('\\','/')
    f   = open(static + u"/captcha.gif", "wb")
    f.write(buf.read())
    f.close()
    return HttpResponse('success!')
