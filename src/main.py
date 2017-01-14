# -*- coding: utf-8 -*-
import os
import sqlite3

from src.container.book import Book
from src.container.task_result import TaskResult
from src.tools.config import Config
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.path import Path
from login import Login
from command_parser import CommandParser
from src.worker import Worker


class ZhihuHelp(object):
    def __init__(self):
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
        zhihu_client = login.get_login_client()
        Worker.set_zhihu_client(zhihu_client)

        Debug.logger.info(u"开始读取ReadList.txt设置信息")

        if not Path.is_file('./ReadList.txt'):
            #  当ReadList不存在的时候自动创建之
            with open('./ReadList.txt', 'w') as read_list:
                read_list.close()
            print Debug.logger.info(u"ReadList.txt 内容为空，自动退出")
            return
        book_counter = self.read_list()

        Debug.logger.info(u"所有书籍制作完成。")
        Debug.logger.info(u"本次共制作书籍{0}本".format(book_counter))
        Debug.logger.info(u"感谢您的使用")
        Debug.logger.info(u"点按任意键退出")
        return

    def read_list(self):
        book_counter = 0  # 统计累计制作了多少本书籍
        #   遍历ReadList，根据指令生成电子书
        with open('./ReadList.txt', 'r') as read_list:
            for line in read_list:
                line = line.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '').split('#')[0]  # 移除空白字符
                if len(line) == 0:
                    continue
                book_counter += 1
                self.create_book(line, book_counter)
        return book_counter

    def create_book(self, command, counter):
        Path.reset_path()
        Debug.logger.info(u"开始制作第 {} 本电子书".format(counter))
        Debug.logger.info(u"对记录 {} 进行分析".format(command))
        task_list = CommandParser.get_task_list(command)  # 分析命令

        if len(task_list) == 0:
            return

        for task in task_list:
            if Config.debug_for_create_book:
                pass
            else:
                Worker.distribute(task)
        Debug.logger.info(u"网页信息抓取完毕")

        task_result_list = []
        for task in task_list:
            task_result = TaskResult(task)
            task_result.extract_data()
            task_result_list.append(task_result)
        Debug.logger.info(u"数据库信息获取完毕")

        #   下载图片
        for task_result in task_result_list:
            task_result.download_img()
        Debug.logger.info(u"所有任务图片获取完毕")

        #   按体积自动分卷
        #   渲染html && 压缩为电子书
        book = Book(task_result_list)
        book_list = book.auto_split(Config.max_book_size_mb)
        for chapter in book_list:
            chapter.create_book()
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
        if Config.debug:
            # 当位于debug模式时，不检查更新
            return
        try:
            content = Http.get_content(u"https://www.yaozeyuan.online/zhihuhelp/upgrade.txt")
            if not content:
                raise Exception('HttpError')
            time, url = [x.strip() for x in content.strip('\n').split('\n')]
            if time == Config.update_time:
                return
            else:
                print u"发现新版本，\n更新日期:{} ，点按回车进入更新页面".format(time)
                print u'新版本下载地址:' + url
                raw_input()
                import webbrowser
                webbrowser.open_new_tab(url)
        except Exception:
            # 不论发生任何异常均直接返回
            return
