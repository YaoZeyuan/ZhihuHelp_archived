# -*- coding: utf-8 -*-

import urllib  # 编码请求字串，用于处理验证码
import json
import pickle
import datetime

from setting import *


class Login():
    def __init__(self):
        self.setting = Setting()
        self.cookieJar = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))
        urllib2.install_opener(self.opener)

    def sendMessage(self, account, password, captcha=''):
        content = HttpBaseClass.get_http_content('http://www.zhihu.com/')
        xsrf = self.get_xsrf(content)
        if not xsrf:
            BaseClass.logger.info(u'知乎网页打开失败')
            BaseClass.logger.info(u'请敲击回车重新发送登陆请求')
            return False
        xsrf = xsrf.split('=')[1]
        # add xsrf as cookie into cookieJar,
        cookie = HttpBaseClass.make_cookie(name='_xsrf', value=xsrf, domain='www.zhihu.com')
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
            'Origin':'http://www.zhihu.com',
            'Referer':'http://www.zhihu.com/',
        }
        result = HttpBaseClass.get_http_content(url = r'http://www.zhihu.com/login/email',data=post_data,extra_header=header)
        if not result:
            BaseClass.logger.info(u'登陆失败，请敲击回车重新登陆')
            return False
        response = json.loads(result)

        if response['r'] == 0:
            print u'登陆成功！'
            print u'登陆账号:', account
            print u'请问是否需要记住帐号密码？输入yes记住，输入其它任意字符跳过，回车确认'
            if raw_input() == 'yes':
                SettingClass.ACCOUNT = account
                SettingClass.PASSWORD = password
                SettingClass.REMEMBERACCOUNT = True
                print u'帐号密码已保存,可通过修改setting.ini进行修改密码等操作'
            else:
                SettingClass.ACCOUNT = ''
                SettingClass.PASSWORD = ''
                SettingClass.REMEMBERACCOUNT = False
                print u'跳过保存环节，进入下一流程'
            self.setting.save()
            cookie = self.saveCookieJar()
            data = {}
            data['account'] = account
            data['password'] = password
            data['recordDate'] = datetime.date.today().isoformat()
            data['cookieStr'] = cookie
            SqlClass.save2DB(data, 'LoginRecord')
            SqlClass.commit()
            return True
        else:
            print u'登陆失败'
            BaseClass.printDict(response)
            return False

    def getCaptcha(self):
        content = HttpBaseClass.get_http_content('http://www.zhihu.com/captcha.gif')  # 开始拉取验证码
        f = open(u'我是登陆知乎时的验证码.gif', 'wb')
        f.write(content)
        f.close()
        print u'请输入您所看到的验证码，验证码在助手所处的文件夹中,\n双击打开『我是登陆知乎时的验证码.gif』即可\n如果不需要输入验证码可以敲击回车跳过此步'
        captcha = raw_input()
        return captcha

    def login(self):
        self.setting.guide()
        account, password = self.setting.login_guide()
        captcha = ''
        while not self.sendMessage(account, password, captcha):
            print u'啊哦，登录失败了'
            print u'请问是否需要更换登陆账号？输入『yes』后按回车可以更换账号密码'
            print u'或者猛击回车进入获取验证码的流程'
            confirm = raw_input()
            if confirm == 'yes':
                account, password = self.setting.login_guide()
            captcha = self.getCaptcha()
        return

    def saveCookieJar(self):
        fileName = u'./theFileNameIsSoLongThatYouWontKnowWhatIsThat.txt'
        f = open(fileName, 'w')
        f.close()
        self.cookieJar.save(fileName)
        f = open(fileName, 'r')
        content = f.read()
        f.close()
        os.remove(fileName)
        return content

    def get_xsrf(self, content=''):
        u'''
        提取xsrf信息
        '''
        xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', content)
        if xsrf:
            return '_xsrf=' + xsrf.group(0)
        return ''