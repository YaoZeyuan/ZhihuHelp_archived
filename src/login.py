# -*- coding: utf-8 -*-
import cookielib
import os
import json
import urllib2

import guide
from src.tools.config import Config
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.extra_tools import ExtraTools
from src.tools.http import Http
from src.tools.match import Match
from src.tools.path import Path


class Login():
    def __init__(self):
        self.cookieJar = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))
        urllib2.install_opener(self.opener)

    def login(self, account, password, captcha=''):
        content = Http.get_content('https://www.zhihu.com/')
        xsrf = Match.xsrf(content)
        if not xsrf:
            Debug.logger.info(u'登陆失败')
            Debug.logger.info(u'敲击回车重新发送登陆请求')
            return False
        xsrf = xsrf.split('=')[1]
        # add xsrf as cookie into cookieJar,
        cookie = Http.make_cookie(name='_xsrf', value=xsrf, domain='www.zhihu.com')
        self.cookieJar.set_cookie(cookie)
        if captcha:
            post_data = {'_xsrf': xsrf, 'email': account, 'password': password, 'remember_me': True,
                         'captcha': captcha}
        else:
            post_data = {'_xsrf': xsrf, 'email': account, 'password': password, 'remember_me': True}

        header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate',  # 主要属性，只要有此项知乎即认为来源非脚本
            'Accept-Language': 'zh,zh-CN;q=0.8,en-GB;q=0.6,en;q=0.4',
            'Host': 'www.zhihu.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/34.0.1847.116 Safari/537.36',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.zhihu.com',
            'Referer': 'https://www.zhihu.com/',
        }
        result = Http.get_content(url=r'https://www.zhihu.com/login/email', data=post_data, extra_header=header)
        if not result:
            Debug.logger.info(u'登陆失败，请敲击回车重新登陆')
            return False
        response = json.loads(result)

        if response['r'] == 0:
            print u'登陆成功！'
            print u'登陆账号:', account
            print u'请问是否需要记住帐号密码？输入yes记住，输入其它任意字符跳过，回车确认'
            if raw_input() == 'yes':
                Config.account, Config.password, Config.remember_account = account, password, True
                print u'帐号密码已保存,可通过修改config.json修改设置'
            else:
                Config.account, Config.password, Config.remember_account = '', '', False
                print u'跳过保存环节，进入下一流程'
            Config._save()
            cookie = self.get_cookie()
            data = {}
            data['account'] = account
            data['password'] = password
            data['recordDate'] = ExtraTools.get_today()
            data['cookieStr'] = cookie
            DB.save(data, 'LoginRecord')
            DB.commit()
            return True
        else:
            print u'登陆失败'
            Debug.print_dict(response)
            return False

    @staticmethod
    def get_captcha():
        content = Http.get_content('https://www.zhihu.com/captcha.gif')  # 开始拉取验证码
        captcha_path = Path.base_path + u'/我是登陆知乎时的验证码.gif'
        with open(captcha_path, 'wb') as image:
            image.write(content)
        print u'请输入您所看到的验证码'
        print u'验证码在助手所处的文件夹中'
        print u'验证码位置:'
        print captcha_path
        print u'如果不需要输入验证码可点按回车跳过此步'
        captcha = raw_input()
        return captcha

    def start(self):
        guide.hello_world()
        account, password = guide.set_account()
        captcha = ''
        while not self.login(account, password, captcha):
            print u'啊哦，登录失败，可能需要输入验证码'
            print u'输入『yes』按回车更换其他账号'
            print u'直接敲击回车获取验证码'
            confirm = raw_input()
            if confirm == 'yes':
                account, password = guide.set_account()
            captcha = self.get_captcha()
        return

    def get_cookie(self):
        filename = ExtraTools.md5(ExtraTools.get_time())
        with open(filename, 'w') as f:
            pass
        self.cookieJar.save(filename)
        with open(filename) as f:
            content = f.read()
        os.remove(filename)
        return content
