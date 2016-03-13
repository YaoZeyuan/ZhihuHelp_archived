# -*- coding: utf-8 -*-
from src.container.image import ImageContainer
from src.tools.config import Config
from src.tools.db import DB
from src.tools.extra_tools import ExtraTools
from src.tools.match import Match
from src.tools.type import Type


class InitialBook(object):
    class Sql(object):
        def __init__(self):
            self.question = ''
            self.answer = ''
            self.info = ''
            return

        def get_answer_sql(self):
            return self.answer + Config.sql_extend_answer_filter

    class Epub(object):
        def __init__(self):
            self.article_count = 0
            self.answer_count = 0
            self.agree_count = 0
            self.char_count = 0

            self.title = ''
            self.id = ''
            self.split_index = 0
            self.prefix = ''
            return

    def __init__(self):
        self.kind = ''
        self.sql = InitialBook.Sql()
        self.epub = InitialBook.Epub()
        self.info = {}
        self.article_list = []
        self.page_list = []
        self.prefix = ''
        return

    def catch_data(self):
        u"""
        从数据库中获取数据
        """
        self.catch_info()
        self.get_article_list()
        self.__sort()
        return self

    def catch_info(self):
        info = {}
        if self.sql.info:
            if self.kind in [Type.question, Type.answer]:
                info = self.catch_question_book_info(self.sql.info)
            elif self.kind == Type.article:
                info = self.catch_article_book_info(self.sql.info)
            else:
                info = DB.cursor.execute(self.sql.info).fetchone()
                info = DB.wrap(Type.info_table[self.kind], info)
        self.set_info(info)
        return

    def catch_question_book_info(self, sql):
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.question, item) for item in info_list]
        info = {}
        info['title'] = '_'.join([str(item['title']) for item in info_list])
        info['id'] = '_'.join([str(item['question_id']) for item in info_list])
        return info

    def catch_article_book_info(self, sql):
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.article, item) for item in info_list]
        info = {}
        info['title'] = '_'.join([str(item['title']) for item in info_list])
        info['id'] = '_'.join([str(item['article_id']) for item in info_list])
        return info

    def set_info(self, info):
        self.info.update(info)
        if self.kind == Type.question:
            self.epub.title = u'知乎问题集锦({})'.format(info['title'])
            self.epub.id = info['id']
        elif self.kind == Type.answer:
            self.epub.title = u'知乎回答集锦({})'.format(info['title'])
            self.epub.id = info['id']
        elif self.kind == Type.article:
            self.epub.title = u'知乎专栏文章集锦({})'.format(info['title'])
            self.epub.id = info['id']

        if self.kind == Type.topic:
            self.epub.title = u'话题_{}({})'.format(info['title'], info['topic_id'])
            self.epub.id = info['topic_id']
        if self.kind == Type.collection:
            self.epub.title = u'收藏夹_{}({})'.format(info['title'], info['collection_id'])
            self.epub.id = info['collection_id']
        if self.kind == Type.author:
            self.epub.title = u'作者_{}({})'.format(info['name'], info['author_id'])
            self.epub.id = info['author_id']
        if self.kind == Type.column:
            self.epub.title = u'专栏_{}({})'.format(info['name'], info['column_id'])
            self.epub.id = info['column_id']
        return

    def get_article_list(self):
        if self.kind in Type.article_type_list:
            article_list = self.__get_article_list()
        else:
            article_list = self.__get_question_list()
        self.set_article_list(article_list)
        return

    def __get_question_list(self):
        question_list = [DB.wrap('question', x) for x in DB.get_result_list(self.sql.question)]
        answer_list = [DB.wrap('answer', x) for x in DB.get_result_list(self.sql.get_answer_sql())]

        def merge_answer_into_question():
            question_dict = {x['question_id']: {'question': x.copy(), 'answer_list': [], 'agree': 0} for x in
                             question_list}
            for answer in answer_list:
                question_dict[answer['question_id']]['answer_list'].append(answer)
            return question_dict.values()

        def add_property(question):
            agree_count = 0
            char_count = 0
            for answer in question['answer_list']:
                answer['char_count'] = len(answer['content'])
                answer['agree_count'] = answer['agree']
                answer['update_date'] = answer['edit_date']
                agree_count += answer['agree']
                char_count += answer['char_count']
            question['answer_count'] = len(question['answer_list'])
            question['agree_count'] = agree_count
            question['char_count'] = char_count
            return question

        question_list = [add_property(x) for x in merge_answer_into_question() if len(x['answer_list'])]
        return question_list

    def __get_article_list(self):
        def add_property(article):
            article['char_count'] = len(article['content'])
            article['agree_count'] = article['agree']
            article['update_date'] = article['publish_date']
            article['answer_count'] = 1
            return article

        article_list = [DB.wrap(Type.article, x) for x in DB.get_result_list(self.sql.get_answer_sql())]
        article_list = [add_property(x) for x in article_list]
        return article_list

    def set_article_list(self, article_list):
        self.clear_property()
        for article in article_list:
            self.epub.answer_count += article['answer_count']
            self.epub.agree_count += article['agree_count']
            self.epub.char_count += article['char_count']
        self.epub.article_count = len(article_list)
        self.article_list = article_list
        return

    def clear_property(self):
        self.epub.answer_count = 0
        self.epub.agree_count = 0
        self.epub.char_count = 0
        self.epub.article_count = 0
        return

    def __sort(self):
        if self.kind in Type.article_type_list:
            self.sort_article()
        else:
            self.sort_question()
        return

    def sort_article(self):
        self.article_list.sort(key=lambda x: x[Config.article_order_by], reverse=Config.article_order_by_desc)
        return

    def sort_question(self):
        def sort_answer(answer_list):
            answer_list.sort(key=lambda x: x[Config.answer_order_by], reverse=Config.answer_order_by_desc)
            return

        self.article_list.sort(key=lambda x: x[Config.question_order_by], reverse=Config.question_order_by_desc)
        for item in self.article_list:
            sort_answer(item['answer_list'])
        return


class HtmlBookPackage(object):
    def __init__(self):
        self.book_list = []
        self.image_list = []
        self.image_container = ImageContainer()
        return

    def get_title(self):
        title = '_'.join([book.epub.title for book in self.book_list])
        title = Match.fix_filename(title)  # 移除特殊字符
        return title
