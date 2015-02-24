# -*- coding: utf-8 -*-
from baseClass import *

import re
import ConfigParser
import os
class Setting(BaseClass):
    u"""
    *   account
        *   用户名
    *   password
        *   密码
    *   rememberAccount
        *   是否保存账号密码
            *   0
            *   1
    *   maxThread
        *   最大线程数
    *   picQuality
        *   图片质量
            *   0 =>   无图
            *   1 => 普通图
            *   2 => 高清图
    *   以下内容为答案过滤标准，不提供修改接口，只能在设置文件中手工修改
    *   contentLength
        *   答案长度
    *   contentAgree
        *   答案赞同数
    *   answerOrderBy
        *   答案排序依据
            *   length
            *   agree
            *   update
            *   userDefine(自定义排序顺序，为GUI做准备)
    *   questionOrderBy
        *   问题排序依据
            *   answerCount
            *   agreeCount
            *   userDefine
    *   contentLength
        *   答案长度
    """
    def __init__(self):
        self.config      = ConfigParser.SafeConfigParser() 
        self.settingList = ['account', 'password', 'rememberAccount', 'maxThread', 'picQuality', 'contentLength', 'contentAgree', 'answerOrderBy', 'questionOrderBy']
        self.setDict     = {
            'account'         : 'mengqingxue2014@qq.com',
            'password'        : '131724qingxue',
            'rememberAccount' : '0',
            'maxThread'       : '20',
            'picQuality'      : '0',
            'contentLength'   : '0',
            'contentAgree'    : '5',
            'answerOrderBy'   : 'agree',
            'questionOrderBy' : 'agreeCount',
        }
        self.initConfig()
        self.config.read('setting.ini')
        self.getSetting(self.settingList)

    def initConfig(self):
        config = self.config
        if not os.path.isfile('setting.ini'):
            f = open('setting.ini', 'w')
            f.close()
            config.add_section('ZhihuHelp') 
            for key in self.setDict:
                config.set('ZhihuHelp', key, self.setDict[key])
            config.write(open('setting.ini','w'))
        return

    def getSetting(self, setting=[]):
        config = self.config
        data   = {}
        if config.has_section('ZhihuHelp'): 
            for key in setting:
                if config.has_option('ZhihuHelp', key):
                    data[key] = config.get('ZhihuHelp', key, raw=True)
                else:
                    data[key] = '';
        return data
    
    def setSetting(self, setting={}):  
        config = self.config
        if not config.has_section('ZhihuHelp'): 
            config.add_section('ZhihuHelp') 
        for key in self.settingList:
            if key in setting:
                config.set('ZhihuHelp', key, str(setting[key]))
        config.write(open('setting.ini', 'w'))
        return
    
    def guide(self):
        print u'您好，欢迎使用知乎助手'
        print u'当前大版本号:1.7.X'
        print u'1.7版本系列将作为助手从命令行界面向图形界面过渡的中间版本，在这一系列中助手将不再能够保存知乎用户答案，涵请见谅：）'
        print u'助手的全部代码都已经开源并托管到了github之上(https://github.com/YaoZeyuan/ZhihuHelp__Python)并附在了压缩包中，您可以随时查阅。'
        print u'由于某些用户设定了隐私保护选项，为了获取全部的答案内容，助手需要您在登陆后使用'
        print u'当然，作者更推荐您使用内置的孟晴雪的账号密码进行登陆，这能更好的保护您的账号密码安全'
        print u'现在开始登陆流程，请根据提示输入您的账号密码'    

    def guideOfAccountAndPassword(self):
        print u'请输入您的用户名(知乎注册邮箱)，回车确认'
        print u'直接敲击回车则使用内置账号进行登陆'
        account = raw_input()
        if len(account) == 0:
            account  = "mengqingxue2014@qq.com"
            password = "131724qingxue"
        else:
            while re.search(r'\w+@[\w\.]{3,}', account) == None:
                print u'抱歉，输入的账号不规范...\n请输入正确的知乎登录邮箱\n'
                print u'账号要求：1.必须是正确格式的邮箱\n2.邮箱用户名只能由数字、字母和下划线_构成\n3.@后面必须要有.而且长度至少为3位'
                print u'范例：mengqingxue2014@qq.com\n5719abc@sina.cn'
                print u'请重新输入账号，回车确认'
                account = raw_input()
            print u'OK,验证通过\n请输入密码，回车确认'
            password = raw_input()
            while len(password) < 6:
                print u'密码长度不科学，密码至少6位起~'
                print u'范例：helloworldvia27149,51zhihu'
                print u'请重新输入密码，回车确认'
                password = raw_input()
        return account, password
        
    def guideOfMaxThread(self):
        print u'开始设置最大同时打开的网页数量，数值越大下载网页的速度越快，丢失答案的概率也越高，推荐值为5~50之间，在这一范围内助手可以很好的解决遗漏答案的问题，默认值为20'
        print u'请输入最大同时打开的网页数(1~199)，回车确认'
        try:
            maxThread = int(raw_input())
        except ValueError as error:
            print error
            print u'嗯，数字转换错误。。。最大线程数重置为20，点击回车继续'
            maxThread = 20
            raw_input()
        if maxThread > 200 or maxThread < 1:
            if maxThread > 200:
                print u'最大线程数溢出'
            else:
                print u'最大线程数非法，该值不能小于零'
            print u'最大线程数重置为20'
            maxThread = 20
            print u'点击回车继续~'      
            raw_input()
        return maxThread

    def guideOfPicQuality(self):
        print u'请选择电子书内的图片质量'
        print u'输入0为无图模式，所生成的电子书最小'
        print u'输入1为标准模式，电子书内带图片，图片清晰度能满足绝大多数答案的需要，电子书内的答案小于1000条时推荐使用'
        print u'输入2为高清模式，电子书内带为知乎原图，清晰度最高，但电子书体积是标准模式的4倍，只有答案条目小于100条时才可以考虑使用'
        print u'请输入图片模式(0、1或2)，回车确认'
        try:
            picQuality = int(raw_input())
        except ValueError as error:
            print error
            print u'嗯，数字转换错误。。。'
            print u'图片模式重置为标准模式，点击回车继续'
            picQuality = 1
            raw_input()
        if picQuality != 0 and picQuality != 1 and picQuality != 2:
            print u'输入数值非法'
            print u'图片模式重置为标准模式，点击回车继续'
            picQuality = 1
            raw_input()
        return picQuality
