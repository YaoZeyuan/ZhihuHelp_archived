# -*- coding: utf-8 -*-
import init
from src import guide
from src.rawbook import RawBook
from src.tools.config import Config
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.path import Path

from worker import worker_factory
from login import Login
from read_list_parser import ReadListParser


class ZhihuHelp(object):
    def __init__(self):
        u"""
        配置文件使用$符区隔，同一行内的配置文件归并至一本电子书内
        """
        Path.init_base_path()
        Path.init_work_directory()
        init.init_database()
        Config._load()
        return

    def init_config(self):
        login = Login()
        if Config.remember_account:
            print u'检测到有设置文件，是否直接使用之前的设置？(帐号、密码、图片质量)'
            print u'点按回车使用之前设置，敲入任意字符后点按回车进行重新设置'
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

    def start(self):
        self.check_update()
        self.init_config()
        Debug.logger.info(u"开始读取ReadList.txt设置信息")
        with open('./ReadList.txt', 'r') as read_list:
            counter = 1
            for line in read_list:
                line = line.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')  # 移除空白字符
                self.create_book(line, counter)  # 一行内容代表一本电子书
                counter += 1
        return

    def create_book(self, command, counter):
        Path.reset_path()

        Debug.logger.info(u"开始制作第 {} 本电子书".format(counter))
        Debug.logger.info(u"对记录 {} 进行分析".format(command))
        task_package = ReadListParser.get_task(command)  # 分析命令

        if not task_package.is_work_list_empty():
            worker_factory(task_package.work_list)  # 执行抓取程序
            Debug.logger.info(u"网页信息抓取完毕")

        if not task_package.is_book_list_empty():
            Debug.logger.info(u"开始自数据库中生成电子书数据")
            book = RawBook(task_package)
            book.create()
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
            content = Http.get_content(u"http://zhihuhelpbyyzy-zhihu.stor.sinaapp.com/ZhihuHelpUpdateTime.txt")
        except:
            return
        time, url = [x.strip() for x in content.split('\n')]
        if time == Config.update_time:
            return
        else:
            print u"发现新版本，\n更新日期:{} ，点按回车进入更新页面".format(time)
            print u'新版本下载地址:' + url
            raw_input()
            import webbrowser
            webbrowser.open_new_tab(url)
        return
