# -*- coding: utf-8 -*-
from baseClass import SqlClass
from codes.epubBuilder.image_container import ImageContainer


class Filter(object):
    u"""
    负责在数据库中提取数据和对数据进行简单处理,返回包含了所有信息的dict和所有待下载图片的imgContainer
    """

    def __init__(self, raw_book_info):
        self.raw_info = raw_book_info
        self.imgContainer = ImageContainer()
        self.book = {}
        self.init_book()
        return

    def init_book(self):
        self.book['info'] = ''
        self.book['article_list'] = []
        return

    def get_question_raw_data(self):
        question_list = [SqlClass.wrap('question', x) for x in self.get_result_list(self.raw_info['question'])]
        answer_list = [SqlClass.wrap('answer', x) for x in self.get_result_list(self.raw_info['answer'])]

        def merge_answer_into_question():
            question_dict = {x['question_id']: {'question': x.copy(), 'answer': []} for x in question_list}
            for answer in answer_list:
                question_dict[answer['question_id']]['answer'].append(answer)
            return question_dict

        return merge_answer_into_question()

    def get_article_raw_data(self):
        article_list = [SqlClass.wrap('article', x) for x in self.get_result_list(self.raw_info['answer'])]
        return article_list

    def get_result_list(self, sql):
        result = SqlClass.cursor.execute(sql).fetchall()
        return result

    def get_book(self):
        self.book['info'] = self.create_info_dict(self.raw_info['kind'], self.raw_info['info'])
        if self.raw_info['kind'] in ['article', 'column']:
            self.book['article_list'] = self.get_article_raw_data()
        else:
            self.book['article_list'] = self.get_question_raw_data()
        return self.book

    def get_image_container(self):
        return self.imgContainer

    def create_info_dict(self, kind, raw):
        info = {}

        def init_property():
            info['base_image_path'] = './image/'
            info['logo_liu_kan_shan'] = './image/kanshan.png'
            return

        def add_css():
            info['markdown_css'] = './markdown.css'
            info['front_css'] = './front.css'
            return

        def add_article_info():
            info['title'] = u'知乎专栏文章集锦'
            info['author_name'] = u'知乎网友'
            return

        def add_answer_info():
            info['title'] = u'知乎回答集锦'
            info['author_name'] = u'知乎网友'
            return

        def add_question_info():
            info['title'] = u'知乎问题集锦'
            info['author_name'] = u'知乎网友'
            return

        def add_topic_info():
            info.update(raw)
            info['logo'] = self.imgContainer.add(raw['logo'])
            return

        def add_collection_info():
            info.update(raw)
            return

        def add_column_info():
            info.update(raw)
            return

        add_customer_info = {'answer': add_answer_info, 'question': add_question_info, 'topic': add_topic_info,
                             'collection': add_collection_info, 'article': add_article_info,
                             'column': add_column_info, }

        init_property()
        add_css()
        add_customer_info[kind]()
        return info

    def create_info_page(self, kind, info_sql):
        info = {}
        with open('./html_template/info/{}.html'.format(kind)) as file:
            template = file.read()
        result = SqlClass.cursor.execute(info_sql).fetchone()
        info = self.create_info_dict(kind, SqlClass.wrap(kind, result))
        return template.format(info)
