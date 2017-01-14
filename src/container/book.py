# -*- coding: utf-8 -*-
import uuid

from src.container.image_container import ImageContainer
from src.lib.epub.epub import Epub
from src.tools.extra_tools import ExtraTools
from src.tools.match import Match
from src.tools.path import Path
from src.tools.template import Template
from src.tools.type import Type


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

        #   先切换到电子书临时资源目录下
        Path.chdir(Path.book_pool_path)
        epub = Epub(title)
        for task_result in self.task_result_list:
            chapter_src = ''
            # info_page
            if task_result.task.task_type == Type.question:
                chapter_src = self.generate_question_info_page(task_result.info_page)
            elif task_result.task.task_type == Type.answer:
                chapter_src = self.generate_question_info_page(task_result.info_page)
            elif task_result.task.task_type == Type.collection:
                chapter_src = self.generate_collection_info_page(task_result.info_page)
            elif task_result.task.task_type == Type.topic:
                chapter_src = self.generate_topic_info_page(task_result.info_page)
            elif task_result.task.task_type == Type.author:
                chapter_src = self.generate_author_info_page(task_result.info_page)
            elif task_result.task.task_type == Type.column:
                chapter_src = self.generate_column_info_page(task_result.info_page)
            elif task_result.task.task_type == Type.article:
                chapter_src = self.generate_article_info_page(task_result.info_page)
            epub.create_chapter(chapter_src, task_result.get_title())
            for question in task_result.question_list:
                #   添加图片文件
                for filename in question.img_filename_list:
                    epub.add_image(Path.image_pool_path + '/' + filename)
                question_src = self.generate_question_page(question)
                epub.add_html(question_src, question.question_info.title)

            for column in task_result.column_list:
                #   添加图片文件
                for filename in column.img_filename_list:
                    epub.add_image(Path.image_pool_path + '/' + filename)
                for article in column.article_list:
                    article_src = self.generate_article_page(article)
                    epub.add_html(article_src, article.title)
            epub.finish_chapter()

        epub.set_creator(u'ZhihuHelp1.8.0')
        epub.set_language(u'zh-cn')
        epub.set_book_id()
        epub.set_output_path(Path.result_path)
        epub.add_css(Path.base_path + u'/www/css/markdown.css')
        epub.add_css(Path.base_path + u'/www/css/customer.css')
        epub.add_css(Path.base_path + u'/www/css/normalize.css')
        epub.add_css(Path.base_path + u'/www/css/bootstrap.css')
        epub.create()

        Path.reset_path()
        return

    def generate_book_info_page(self):
        """
        生成图书信息页
        :return:
        :rtype:
        """
        filename = self.get_random_html_file_name()
        content = Template.book_info.format(
            **{
                'title': self.book_title
            }
        )
        uri = Path.html_pool_path + '/' + filename
        buf_file = open(uri, 'w')
        buf_file.write(content)
        buf_file.close()
        return uri

    def generate_question_info_page(self, info_page):
        """
        :param info_page:
        :type info_page: src.container.data.question.Question
        :return: src
        :rtype: str
        """
        filename = self.get_random_html_file_name()
        content = Template.question_info.format(
            **{
                'title': info_page.title,
                'answer_count': info_page.answer_count,
                'follower_count': info_page.follower_count,
                'comment_count': info_page.comment_count,
            }
        )
        uri = Path.html_pool_path + '/' + filename
        buf_file = open(uri, 'w')
        buf_file.write(content)
        buf_file.close()
        return uri

    def generate_author_info_page(self, info_page):
        """
        :param info_page:
        :type info_page: src.container.data.author.Author
        :return: src
        :rtype: str
        """
        filename = self.get_random_html_file_name()
        content = Template.author_info.format(
            **{
                'title': info_page.name + u'的知乎回答集锦',
                'name': info_page.name,
                'answer_count': info_page.answer_count,
                'follower_count': info_page.follower_count,
                'voteup_count': info_page.voteup_count,
            }
        )
        uri = Path.html_pool_path + '/' + filename
        buf_file = open(uri, 'w')
        buf_file.write(content)
        buf_file.close()
        return uri

    def generate_topic_info_page(self, info_page):
        """
        :param info_page:
        :type info_page: src.container.data.topic.Topic
        :return: src
        :rtype: str
        """
        filename = self.get_random_html_file_name()
        content = Template.topic_info.format(
            **{
                'title': "话题{}({})下精华回答集锦".format(info_page.name, info_page.topic_id),
                'name': info_page.name,
                'questions_count': info_page.questions_count,
            }
        )
        uri = Path.html_pool_path + '/' + filename
        buf_file = open(uri, 'w')
        buf_file.write(content)
        buf_file.close()
        return uri

    def generate_collection_info_page(self, info_page):
        """
        :param info_page:
        :type info_page: src.container.data.collection.Collection
        :return: src
        :rtype: str
        """
        filename = self.get_random_html_file_name()
        content = Template.collection_info.format(
            **{
                'title': info_page.title,
                'answer_count': info_page.answer_count,
                'follower_count': info_page.follower_count,
            }
        )
        uri = Path.html_pool_path + '/' + filename
        buf_file = open(uri, 'w')
        buf_file.write(content)
        buf_file.close()
        return uri

    def generate_column_info_page(self, info_page):
        """
        :param info_page:
        :type info_page: src.container.data.column.Column
        :return: src
        :rtype: str
        """
        filename = self.get_random_html_file_name()
        content = Template.column_info.format(
            **{
                'title': u"知乎专栏{}({})".format(info_page.title, info_page.column_id),
                'name': info_page.title,
                'postsCount': info_page.article_count,
            }
        )
        uri = Path.html_pool_path + '/' + filename
        buf_file = open(uri, 'w')
        buf_file.write(content)
        buf_file.close()
        return uri

    def generate_article_info_page(self, info_page):
        """
        :param info_page:
        :type info_page: src.container.data.article.Article
        :return: src
        :rtype: str
        """
        filename = self.get_random_html_file_name()
        content = Template.article_info.format(
            **{
                'title': info_page.title,
                'voteup_count': info_page.voteup_count,
            }
        )
        uri = Path.html_pool_path + '/' + filename
        buf_file = open(uri, 'w')
        buf_file.write(content)
        buf_file.close()
        return uri

    def generate_question_page(self, question):
        """
        :type question: src.container.task_result.Question
        :return:
        :rtype:
        """
        # 先输出answer的内容
        answer_content = u''
        for answer in question.answer_list:
            answer_content += Template.answer.format(
                **{
                    'author_avatar_url': answer.author_avatar_url,
                    'author_name': answer.author_name,
                    'author_id': answer.author_id,
                    'author_headline': answer.author_headline,

                    'content': answer.content,
                    'comment_count': answer.comment_count,
                    'voteup_count': answer.voteup_count,
                    'updated_time': ExtraTools.format_date('Y-m-d H:i:s', answer.updated_time),
                }
            )

        filename = self.get_random_html_file_name()
        content = Template.question.format(
            **{
                'title': question.question_info.title,
                'description': question.question_info.detail,
                'answer': answer_content
            }
        )
        uri = Path.html_pool_path + '/' + filename
        buf_file = open(uri, 'w')
        buf_file.write(content)
        buf_file.close()
        return uri

    def generate_article_page(self, article):
        """
        :type article: src.container.data.article.Article
        :return:
        :rtype:
        """
        answer_content = Template.answer.format(
            **{
                'author_avatar_url': article.author_avatar_url,
                'author_name': article.author_name,
                'author_id': article.author_id,
                'author_headline': article.author_headline,

                'content': article.content,
                'comment_count': article.comment_count,
                'voteup_count': article.voteup_count,
                'updated_time':  ExtraTools.format_date('Y-m-d H:i:s', article.updated_time),
            }
        )

        filename = self.get_random_html_file_name()
        content = Template.question.format(
            **{
                'title': article.title,
                'description': '',
                'answer': answer_content
            }
        )
        uri = Path.html_pool_path + '/' + filename
        buf_file = open(uri, 'w')
        buf_file.write(content)
        buf_file.close()
        return uri

    def get_random_html_file_name(self):
        u"""
        生成一个随机html
        :return:
        :rtype:
        """
        filename = ExtraTools.md5(str(uuid.uuid4())) + '.xhtml'
        return filename
