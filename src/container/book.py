# -*- coding: utf-8 -*-
import uuid

from src.container.image_container import ImageContainer
from src.lib.epub.epub import Epub
from src.tools.extra_tools import ExtraTools
from src.tools.match import Match
from src.tools.path import Path
from src.tools.template import Template


class Book(object):
    u"""
    正式用于渲染书籍的容器
    """

    def __init__(self, task_result_list):
        u"""

        :param task_result_list:
        :type task_result_list: list[src.container.task_result.TaskResult]
        """
        self.task_result_list = task_result_list

        #   分卷相关
        self.is_split = False  # 是否是被拆分后的结果集
        self.chapter_no = 0  # 若是被拆分后的结果集，那么是哪一集

        #   图片下载相关
        self.img_container = ImageContainer()

        #   文件内容
        self.index_html = u''
        self.book_title = u''

        return

    def auto_split(self, max_size_page_kb=50 * 1024):
        """
        :rtype: list[Book]
        """
        if max_size_page_kb < 1 * 1024:
            #   不能任意小啊
            max_size_page_kb = 1 * 1024

        # 如果图书没有名字的话，要先生成图书的名字，避免混乱
        if len(self.book_title) == 0:
            self.book_title = self.generate_book_title()

        if self.get_total_img_size_kb() <= max_size_page_kb:
            #   大小符合要求，最好
            return [self]

        if not self.is_split:
            # 第一次分隔，序号应该为卷1
            self.is_split = True
            self.chapter_no = 1

        new_book = Book([])
        new_book.is_split = True
        new_book.chapter_no = self.chapter_no + 1
        new_book.book_title = self.book_title

        while self.get_total_img_size_kb() > max_size_page_kb:
            task_result = self.task_result_list.pop()
            if len(self.task_result_list) == 0:
                # 最后一个任务
                legal_task_result, remain_task_result = task_result.auto_split(max_size_page_kb)
                self.task_result_list.append(legal_task_result)
                new_book.task_result_list.insert(0, remain_task_result)
                return [self] + new_book.auto_split(max_size_page_kb)
            else:
                new_book.task_result_list.insert(0, task_result)
        return [self] + new_book.auto_split(max_size_page_kb)

    def get_total_img_size_kb(self):
        total_img_size_kb = 0
        for task_result in self.task_result_list:
            total_img_size_kb += task_result.get_total_img_size_kb()
        return total_img_size_kb

    def generate_book_title(self):
        """
        生成并设置
        :return:
        :rtype:str
        """
        title_list = []
        for task_result in self.task_result_list:
            title_list.append(task_result.get_title())
        title = u'_'.join(title_list)
        if len(title) > 50:
            title = title[:50] + u'。。。等' + str(len(title_list)) + u'本电子书'
        title = Match.replace_danger_char_for_filesystem(title)

        self.book_title = title
        return title

    def create_book(self):
        #   确定文件信息
        title = self.book_title
        if self.is_split:
            title = self.book_title + u'_卷{}'.format(self.chapter_no)

        # epub = Epub(title)
        # for task_result in self.task_result_list:
        #    epub.create_chapter(,task_result.get_title())
        #
        #
        #    epub.finish_chapter()

        #   生成目录
        #   生成信息页
        #   生成具体内容
        #   下载图片
        #   放置于指定位置
        #   压缩成zip
        return

    def generate_book_info_page(self):
        """
        生成图书信息页
        :return:
        :rtype:
        """
        filename = self.get_random_html_file_name()
        content = Template.book_info.format({'title': self.book_title})
        uri = Path.html_pool_path + '/' + filename
        buf_file = open(uri, 'w')
        buf_file.write(content)
        buf_file.close()
        return uri

    def generate_question_info_page(self, info_page):
        """
        :param info_page:
        :type info_page: src.container.data.question.Question
        :return:
        :rtype:
        """
        filename = self.get_random_html_file_name()
        content = Template.question_info.format({
            'title': info_page.title,
            'answer_count': info_page.answer_count,
            'follower_count': info_page.follower_count,
            'comment_count': info_page.comment_count,
        })
        uri = Path.html_pool_path + '/' + filename
        buf_file = open(uri, 'w')
        buf_file.write(content)
        buf_file.close()
        return uri

    def generate_author_info_page(self, info_page):
        """
        :param info_page:
        :type info_page: src.container.data.author.Author
        :return:
        :rtype:
        """
        return

    def generate_topic_info_page(self, info_page):
        """
        :param info_page:
        :type info_page: src.container.data.topic.Topic
        :return:
        :rtype:
        """
        return

    def generate_collection_info_page(self, info_page):
        """
        :param info_page:
        :type info_page: src.container.data.collection.Collection
        :return:
        :rtype:
        """
        return

    def generate_column_info_page(self, info_page):
        """
        :param info_page:
        :type info_page: src.container.data.column.Column
        :return:
        :rtype:
        """
        return

    def generate_article_info_page(self, info_page):
        """
        :param info_page:
        :type info_page: src.container.data.article.Article
        :return:
        :rtype:
        """
        return

    def get_random_html_file_name(self):
        u"""
        生成一个随机html
        :return:
        :rtype:
        """
        filename = ExtraTools.md5(str(uuid.uuid4())) + '.html'
        return filename
