# -*- coding: utf-8 -*-
import random
from baseClass import SqlClass, SettingClass, TypeClass, BaseClass
from image_container import ImageContainer


class EpubArticle(object):
    def __init__(self):
        return


class EpubBookProperty(object):
    def __init__(self):
        self.article_count = 0
        self.answer_count = 0
        self.agree_count = 0
        self.char_count = 0

        self.title = ''
        self.id = ''
        self.split_index = 0
        return


class EpubBookConfig(object):
    def __init__(self):

        self.kind = ''
        self.article_list = []
        self.property = EpubBookProperty()

        self.info = {}
        return

    def set_article_list(self, article_list):
        for article in article_list:
            self.property.answer_count += article['answer_count']
            self.property.agree_count += article['agree_count']
            self.property.char_count += article['char_count']
        self.property.article_count = len(article_list)
        return

    def set_info(self, info):
        self.info.update(info)
        if self.kind == TypeClass.question:
            self.property.title = '知乎问题集锦({})'.format(BaseClass.get_time())
            self.property.id = BaseClass.get_time()
        if self.kind == TypeClass.answer:
            self.property.title = '知乎回答集锦({})'.format(BaseClass.get_time())
            self.property.id = BaseClass.get_time()
        if self.kind == TypeClass.article:
            self.property.title = '知乎专栏文章集锦({})'.format(BaseClass.get_time())
            self.property.id = BaseClass.get_time()

        if self.kind == TypeClass.topic:
            self.property.title = '话题_{}({})'.format(info['title'], info['topic_id'])
            self.property.id = info['topic_id']
        if self.kind == TypeClass.collection:
            self.property.title = '收藏夹_{}({})'.format(info['title'], info['collection_id'])
            self.property.id = info['collection_id']
        if self.kind == TypeClass.author:
            self.property.title = '作者_{}({})'.format(info['name'], info['author_id'])
            self.property.id = info['author_id']
        if self.kind == TypeClass.collection:
            self.property.title = '专栏_{}({})'.format(info['name'], info['column_id'])
            self.property.id = info['column_id']
        return

    def copy(self):
        new_book = EpubBookConfig()
        new_book.kind = self.kind
        new_book.property = EpubBookProperty()
        new_book.set_info(self.info)
        return

class Book(object):
    u"""
    负责在数据库中提取数据，生成基本的book字典
    只代表一本书
    """
    def __init__(self, book_info):
        self.book_info = book_info
        self.book = EpubBookConfig()

        self.book.kind = book_info.kind
        return

    def get_book(self):
        self.catch_info()
        self.get_article_list()
        return self.book

    def catch_info(self):
        info = {}
        if self.book_info.info:
            info = SqlClass.cursor.execute(self.book_info.info).fetchone()
            info = SqlClass.wrap(TypeClass.info_table[self.book.kind], info)
        self.book.set_info(info)
        return

    def get_article_list(self):
        if self.book.kind in ['article', 'column']:
            article_list = self.__get_article_list()
        else:
            article_list = self.__get_question_list()
        self.book.set_article_list(article_list)
        return

    def __get_question_list(self):
        question_list = [SqlClass.wrap('question', x) for x in SqlClass.get_result_list(self.book_info.question)]
        answer_list = [SqlClass.wrap('answer', x) for x in SqlClass.get_result_list(self.book_info.answer)]

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

        question_list = [add_property(x) for x in merge_answer_into_question()]
        return question_list

    def __get_article_list(self):
        def add_property(article):
            article['char_count'] = len(article['content'])
            article['agree_count'] = article['agree']
            article['update_date'] = article['publish_date']
            article['answer_count'] = 1
            return article

        article_list = [SqlClass.wrap('article', x) for x in SqlClass.get_result_list(self.book_info['answer'])]
        article_list = [add_property(x) for x in article_list]
        return article_list


import re


class CreateHtmlPage(object):
    u'''
    工具类，用于生成html页面
    '''

    def __init__(self, image_container):
        self.image_container = image_container
        return

    def fix_image(self, content):
        for img in re.findall(r'<img[^>]*', content):
            src = re.search(r'(?<=src=").*?(?=")', img)
            if not src:
                continue
            else:
                src = src.group(0)
                if src.replace(' ', '') == '':
                    continue
            src_download = CreateHtmlPage.fix_image_src(src)
            if src_download:
                filename = self.image_container.add(src_download)
            else:
                filename = ''
            content = content.replace('"{}"'.format(src), '"../images/{}"'.format(filename))
        return content

    @staticmethod
    def fix_image_src(href):
        if 'https' in href[:5]:  # 去除https
            href = 'http' + href[5:]

        if SettingClass.PICQUALITY == 0:
            return ''
        if 'equation?tex=' in href:  # 不处理tex图片
            return href
        if SettingClass.PICQUALITY == 1:
            return href
        if SettingClass.PICQUALITY == 2:
            if not ('_' in href):
                return href
            pos = href.rfind('_')
            return href[:pos] + href[pos + 2:]  # 删除'_m'等图片质量控制符，获取原图
        return href

    def create_question(self, question, prefix=''):
        def create_answer(answer):
            with open('./html_template/content/answer.html') as answer_temp:
                template = answer_temp.read()
            return template.format(**answer)

        answer_content = ''.join([create_answer(answer) for answer in question['answer_list']])
        question['answer_content'] = answer_content
        with open('./html_template/content/question.html') as question_temp:
            template = question_temp.read()
        question.update(question['question'])
        content = template.format(**question)
        page = dict()
        page['content'] = self.fix_image(content)
        page['filename'] = str(prefix) + str(question['question_id']) + '.html'
        page['title'] = question['title']
        return page

    def create_article(self, article, prefix=''):
        with open('./html_template/content/article.html') as article_temp:
            template = article_temp.read()
        content = template.format(**article)
        page = dict()
        page['content'] = self.fix_image(content)
        page['filename'] = prefix + str(article['article_id']) + '.html'
        page['title'] = article['title']
        return page

    def create_info_page(self, book, prefix=''):
        kind = book.kind
        info = book.info
        with open('./html_template/info/{}.html'.format(kind)) as file:
            template = file.read()
        content = template.format(**info)
        page = dict()
        page['content'] = self.fix_image(content)
        page['filename'] = str(prefix) + 'info.html'
        page['title'] = book.property.title
        if book.property.split_index:
            page['title'] += "_({})".format(book.property.split_index)
        return page


class BookSplit(object):
    def __init__(self, book_list):
        self.raw_book_list = book_list
        self.book_list = []
        return

    def get_book_list(self):
        self.__sort()
        self.__split()
        return self.book_list

    def __sort(self):
        for book in self.raw_book_list:
            if book.kind in TypeClass.article_type:
                self.sort_article(book)
            else:
                self.sort_question(book)
        return

    def sort_article(self, book):
        article_list = book.article_list
        article_list.sort(key=lambda x: x[SettingClass.ARTICLEORDERBY], reverse=SettingClass.ARTICLEORDERBYDESC)
        return

    def sort_question(self, book):
        def sort_answer(answer_list):
            answer_list.sort(key=lambda x: x[SettingClass.ANSWERORDERBY], reverse=SettingClass.ANSWERORDERBYDESC)
            return

        book.article_list.sort(key=lambda x: x[SettingClass.QUESTIONORDERBY], reverse=SettingClass.QUESTIONORDERBYDESC)
        for item in book.article_list:
            sort_answer(item['answer_list'])
        return

    def __split(self):
        def split(book, surplus, index=1):
            if book.property.answer_count <= surplus:
                book.property.split_index = index
                return [book]
            article_list = []
            while surplus > 0:
                article = book.article_list.pop()
                article_list.append(article)
                surplus -= article['answer_count']
                book.property.answer_count -= article['answer_count']
            new_book = book.copy()
            new_book.set_article_list(article_list)
            new_book.property.split_index = index
            return [new_book] + split(book, SettingClass.MAXANSWER, index + 1)

        counter = 0
        book_list = []
        while len(self.raw_book_list):
            book = self.raw_book_list.pop()
            if (counter + book.property.answer_count) < SettingClass.MAXANSWER:
                book_list.append(book)
            else:
                split_list = split(book, SettingClass.MAXANSWER - counter)
                book_list.append(split_list[0])
                self.book_list.append(book_list)
                self.raw_book_list += split_list[1:]
                counter = 0
        self.book_list.append(book_list)
        return

class RawBook(object):
    u"""
    负责数据进行处理,返回处理完毕的html信息和所有待下载图片的imgContainer
    """

    def __init__(self, raw_info):
        self.book_info_list = self.merge_raw_info(raw_info)
        return

    def merge_raw_info(self, raw_info):
        book_info_list = []
        for kind in TypeClass.type_list:
            if not kind in raw_info:
                continue
            for info in raw_info[kind]:
                book_info_list.append(info)
        return book_info_list

    def get_book_list(self):
        raw_book_list = self.sql2dict()
        book_split = BookSplit(raw_book_list)
        split_book_list = book_split.get_book_list()
        book_list = []
        for item in split_book_list:
            book = self.create_book(item)
            book_list.append(book)
        return book_list

    def sql2dict(self):
        book_list = []
        for info in self.book_info_list:
            book = Book(info)
            book_list.append(book.get_book())
        return book_list

    def create_book(self, book_list):
        index = 0
        epub_book_list = []
        image_container = ImageContainer()
        creator = CreateHtmlPage(image_container)
        for book in book_list:
            epub_book = self.create_single_book(book, index, creator)
            epub_book_list.append(epub_book)
            index += 1
        book = {'book_list': epub_book_list, 'image_list': image_container.get_filename_list(),
            'image_container': image_container, }
        return book

    def create_single_book(self, raw_book, index, creator):
        book = {'title': '', 'page_list': [], 'pre_fix': '', }

        book['title'] = raw_book.property.title
        if raw_book.property.split_index:
            book['title'] += "_({})".format(raw_book.property.split_index)

        book['pre_fix'] = index

        page = creator.create_info_page(raw_book, book['pre_fix'])
        book['page_list'].append(page)
        for article in raw_book.article_list:
            if raw_book.kind in TypeClass.article_type:
                page = creator.create_article(article, index)
            else:
                page = creator.create_question(article, index)
            book['page_list'].append(page)
        return book
