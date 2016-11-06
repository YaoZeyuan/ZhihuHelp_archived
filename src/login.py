# -*- coding: utf-8 -*-
import os
import sys
import platform
import webbrowser
import json
import time

import guide
from src.lib.oauth.zhihu_oauth import ZhihuClient
from src.lib.oauth.zhihu_oauth.exception import NeedCaptchaException

from src.tools.config import Config
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.extra_tools import ExtraTools
from src.tools.http import Http
from src.tools.match import Match
from src.tools.path import Path

class Login():
    u"""
    登录部分，登录完成后返回一个可用的client对象，用于进一步获取知乎网对应信息
    """
    def __init__(self):
        self.client = ZhihuClient()

    def login(self, account, password, captcha=''):
        try:
            is_login_success, reason = self.client.login(account, password)
        except NeedCaptchaException:
            # 保存验证码并提示输入，重新登录
            print u'登录失败，需要输入验证码'
            return False
        if is_login_success:
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
            return True
        else:
            print u'登陆失败'
            print u"失败原因 => " + str(reason)
            return False

    def get_captcha(self):
        captcha_path = Path.base_path + u'/我是登陆知乎时的验证码.gif'

        image = open(captcha_path, 'wb')
        image.write(self.client.get_captcha())
        image.close()

        print u'请输入您所看到的验证码'
        print u'验证码在助手所处的文件夹中'
        print u'验证码位置:'
        print captcha_path
        # 尝试自动打开验证码
        webbrowser.get().open_new_tab(u'file:///' + captcha_path)

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
        return self.client
