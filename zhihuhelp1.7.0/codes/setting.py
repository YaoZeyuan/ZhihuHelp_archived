# -*- coding: utf-8 -*-
import re
import json

from baseClass import *


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
        self.initSettingDict()
        self.loadSetting()

    def initSettingDict(self):
        self.setDict = {}
        self.sync()

    def encodeSetting(self):
        self.sync()
        return json.dumps(self.setDict, indent=4)

    def sync(self):
        for attr in dir(SettingClass):
            if attr.find("__") != 0:
                self.setDict[attr] = getattr(SettingClass, attr)
        return

    def save(self):
        f = open('setting.ini', 'w')
        f.write(self.encodeSetting())
        f.close()
        return

    def loadSetting(self):
        if not os.path.isfile('setting.ini'):
            f = open('setting.ini', 'w')
            f.write(self.encodeSetting())
            f.close()
        f = open('setting.ini', 'r')
        self.setDict = json.load(f)
        for key in self.setDict:
            setattr(SettingClass, key, self.setDict[key])
        f.close()
        return

    def printSetting(self):
        u'''
        测试设置值是否正确
        '''
        self.sync()
        BaseClass.printDict(self.setDict)

    def guide(self):
        print u'您好，欢迎使用知乎助手'
        print u''
        print u''
        print u'本版内置了公共账号『孟晴雪』，默认使用内置账号进行登陆'
        print u''
        print u''
        print u'全部代码均已开源，github地址:https://github.com/YaoZeyuan/ZhihuHelp__Python'
        print u'Tips：只有在获取私人收藏夹的内容时，助手才需要使用您的账号登陆，日常使用时直接用内置账号登陆即可'
        print u'现在开始登陆流程，请根据提示输入您的账号密码'
        print u''
        print u''

    def guideOfAccountAndPassword(self):
        print u'请输入您的用户名(知乎注册邮箱)，回车确认'
        print u'####################################'
        print u'#直接敲击回车则使用内置账号进行登陆#'
        print u'####################################'
        account = raw_input()
        if len(account) == 0:
            account = SettingClass.ACCOUNT
            password = SettingClass.PASSWORD
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
        print u'开始设置最大同时打开的网页数量，数值越大下载网页的速度越快，丢失答案的概率也越高，推荐值为5~20之间，在这一范围内助手可以很好的解决遗漏答案的问题，默认值为20'
        print u'请输入最大同时打开的网页数(1~199)，回车确认'
        try:
            maxThread = int(raw_input())
        except ValueError as error:
            print error
            print u'嗯，数字转换错误。。。最大线程数重置为{}，点击回车继续'.format(SettingClass.MAXTHREAD)
            maxThread = SettingClass.MAXTHREAD
            raw_input()
        if maxThread > 200 or maxThread < 1:
            if maxThread > 200:
                print u'最大线程数溢出'
            else:
                print u'最大线程数非法，该值不能小于零'
            print u'最大线程数重置为{}'.format(SettingClass.MAXTHREAD)
            maxThread = SettingClass.MAXTHREAD
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
