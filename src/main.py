# -*- coding: utf-8 -*-
from src.tools.config import Config
from src.tools.http import Http
from src.tools.path import Path

import guide
import init

from worker import worker_factory
from login import *
from epub_creator import create_epub
from read_list_parser import ReadListParser


class ZhihuHelp(object):
    def __init__(self):
        u"""
        配置文件使用$符区隔，同一行内的配置文件归并至一本电子书内
        """
        init.init_database()
        Path.init_base_path()
        Config._load()
        return

    def init_config(self):
        login = Login()
        if Config.remember_account:
            print   u'检测到有设置文件，是否直接使用之前的设置？(帐号、密码、图片质量)'
            print   u'点按回车使用之前设置，敲入任意字符后点按回车进行重新设置'
            if raw_input():
                login.start()
                Config.picture_quality = guide.set_picture_quality()
            else:
                Http.set_cookie()
        else:
            login.start()
            Config.picture_quality = guide.set_picture_quality()

        # 储存设置
        Config._save()
        return

    def create_book(self, command, counter):
        BaseClass.reset_dir()

        BaseClass.logger.info(u"开始制作第 {} 本电子书".format(counter))
        BaseClass.logger.info(u"对记录 {} 进行分析".format(command))
        task = ReadListParser.get_task(command)  # 分析命令
        worker_factory(task.work_list)  # 执行抓取程序
        BaseClass.logger.info(u"网页信息抓取完毕")

        BaseClass.logger.info(u"开始自数据库中生成电子书数据")
        create_epub(task)
        return

    def start(self):
        #self.check_update()
        self.init_config()
        BaseClass.init_path()
        BaseClass.logger.info(u"开始读取ReadList.txt设置信息")
        with open('./ReadList.txt', 'r') as read_list:
            counter = 1
            for line in read_list:
                self.create_book(line, counter)  # 一行内容代表一本电子书
                counter += 1
        return

    def check_update(self):  # 强制更新
        u"""
            *   功能
                *   检测更新。
                *   若在服务器端检测到新版本，自动打开浏览器进入新版下载页面
                *   网页请求超时或者版本号正确都将自动跳过
            *   输入
                *   无
            *   返回
                *   无
        """
        print   u"检查更新。。。"
        try:
            updateTime = urllib2.urlopen(u"http://zhihuhelpbyyzy-zhihu.stor.sinaapp.com/ZhihuHelpUpdateTime.txt",
                                         timeout=10)
        except:
            return
        time = updateTime.readline().replace(u'\n', '').replace(u'\r', '')
        url = updateTime.readline().replace(u'\n', '').replace(u'\r', '')
        updateComment = updateTime.read()
        if time == SettingClass.UPDATETIME:
            return
        else:
            print u"发现新版本，\n更新说明:{}\n更新日期:{} ，点按回车进入更新页面".format(updateComment, time)
            print u'新版本下载地址:' + url
            raw_input()
            import webbrowser
            webbrowser.open_new_tab(url)
        return
