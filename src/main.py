# -*- coding: utf-8 -*-
import sqlite3

from src.book import Book
from src.tools.config import Config
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.path import Path
from login import Login
from read_list_parser import ReadListParser
from src.worker import worker_factory


class ZhihuHelp(object):
    def __init__(self):
        self.zhihu_api_client = None  # 知乎客户端，用于获取API数据
        #   初始化目录结构
        Path.init_base_path()
        Path.init_work_directory()
        #   初始化数据库链接
        DB.init_database()
        #   初始化配置
        Config.init_config()
        return

    def start(self):
        #   检查更新
        self.check_update()

        #   登录
        login = Login()
        self.zhihu_api_client = login.get_login_client()

        Debug.logger.info(u"开始读取ReadList.txt设置信息")
        counter = 1
        try:
            with open('./ReadList.txt', 'r') as read_list:
                counter = 1
                for line in read_list:
                    line = line.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')  # 移除空白字符
        except IOError as e:
            with open('./ReadList.txt', 'w') as read_list:
                read_list.close()

        if counter == 1:
            print u"ReadList.txt 内容为空"
        return

    def create_book(self, command, counter):
        Path.reset_path()
        Debug.logger.info(u"开始制作第 {} 本电子书".format(counter))
        Debug.logger.info(u"对记录 {} 进行分析".format(command))
        task_package = ReadListParser.get_task(command)  # 分析命令

        if not task_package.is_work_list_empty():
            worker_factory(self.zhihu_api_client, task_package.work_list)  # 执行抓取程序
            Debug.logger.info(u"网页信息抓取完毕")

        if not task_package.is_book_list_empty():
            Debug.logger.info(u"开始自数据库中生成电子书数据")
            book = Book(task_package.book_list)
            book.create()
        return

    @staticmethod
    def check_update():  # 强制更新
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
        print u"检查更新。。。"
        try:
            content = Http.get_content(u"http://zhihuhelpbyyzy-zhihu.stor.sinaapp.com/ZhihuHelpUpdateTime.txt")
            if not content:
                raise Exception('HttpError')
            time, url = [x.strip() for x in content.split('\n')]
            if time == Config.update_time:
                return
            else:
                print u"发现新版本，\n更新日期:{} ，点按回车进入更新页面".format(time)
                print u'新版本下载地址:' + url
                raw_input()
                import webbrowser
                webbrowser.open_new_tab(url)
        except:
            # 不论发生任何异常均直接返回
            return
