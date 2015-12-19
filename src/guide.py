# -*- coding: utf-8 -*-
import re

from src.tools.config import Config


def hello_world():
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
    return


def set_account():
    print u'请输入您的知乎注册邮箱，回车确认'
    print u'####################################'
    print u'#直接敲击回车则使用内置账号进行登陆#'
    print u'####################################'
    account = raw_input()
    if account:
        while not re.search(r'\w+@[\w\.]{3,}', account):
            print u'抱歉，输入的账号不规范...\n请输入正确的知乎登录邮箱\n'
            print u'范例：mengqingxue2014@qq.com\n5719abc@sina.cn'
            print u'请重新输入账号，回车确认'
            account = raw_input()
        print u'请输入密码，回车确认'
        password = raw_input()
        while len(password) < 6:
            print u'密码长度不正确，密码至少6位'
            print u'请重新输入密码，回车确认'
            password = raw_input()
    else:
        account, password = Config.account, Config.password
    return account, password


def set_picture_quality():
    print u'请选择电子书内的图片质量'
    print u'输入0为无图模式，生成电子书体积最小'
    print u'输入1为标准模式，图片清晰度能满足绝大多数答案的需要'
    print u'输入2为高清模式，图片为知乎原图，清晰度最高，但电子书体积是标准模式的4倍，只有答案条目小于100条时才可以考虑使用'
    print u'请输入图片模式(0、1或2)，回车确认'
    try:
        quality = int(raw_input())
    except ValueError as error:
        print error
        print u'数字转换错误。。。'
        print u'图片模式重置为标准模式，点击回车继续'
        quality = 1
        raw_input()
    if not (quality in [0, 1, 2]):
        print u'输入数值非法'
        print u'图片模式重置为标准模式，点击回车继续'
        quality = 1
        raw_input()
    return quality
