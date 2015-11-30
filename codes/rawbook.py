# -*- coding: utf-8 -*-
from baseClass import SqlClass, SettingClass, TypeClass
from image_container import ImageContainer


class Book(object):
    u"""
    负责在数据库中提取数据，生成基本的book字典
    """
    def __init__(self, book_info):
        self.book_info = book_info
        self.kind = book_info['kind']
        self.book = {'kind': self.kind, 'info': None, 'article_list': [], }
        return

    def get_book(self):
        self.book['info'] = self.get_info()
        self.book['article_list'] = self.get_article_list()
        self.book['article_count'] = len(self.book['article_list'])
        self.book['answer_count'] = 0
        for x in self.book['article_list']:
            self.book['answer_count'] += x['answer_count']
        return self.book

    def get_info(self):
        info = dict()
        if self.book_info['info']:
            info = SqlClass.cursor.execute(self.book_info['info']).fetchone()
            info = SqlClass.wrap(TypeClass.info_table[self.kind], info)
        return info

    def get_article_list(self):
        if self.kind in ['article', 'column']:
            article_list = self.__get_question_list()
        else:
            article_list = self.__get_article_list()
        return article_list

    def __get_question_list(self):
        question_list = [SqlClass.wrap('question', x) for x in SqlClass.get_result_list(self.book_info['question'])]
        answer_list = [SqlClass.wrap('answer', x) for x in SqlClass.get_result_list(self.book_info['answer'])]

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
            question['answer_count'] = len(question['answer'])
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

        article_list = [SqlClass.wrap('article', x) for x in SqlClass.get_result_list(self.raw_info['answer'])]
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
        for img in re.findall(r'<img.*?>', content):
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

        answer_content = ''.join([create_answer(answer) for answer in question['article_list']])
        question['answer_content'] = answer_content
        with open('./html_template/content/question.html') as question_temp:
            template = question_temp.read()
        content = template.format(**question)
        page = dict()
        page['content'] = self.fix_image(content)
        page['filename'] = prefix + str(question['question_id']) + '.html'
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

    def create_info_page(self, kind, info, prefix=''):
        with open('./html_template/info/{}.html'.format(kind)) as file:
            template = file.read()
        content = template.format(**info)
        page = dict()
        page['content'] = self.fix_image(content)
        page['filename'] = prefix + 'info.html'
        page['title'] = self.info['title']
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
            if book['kind'] in ['article', 'column']:
                self.sort_article(book)
            else:
                self.sort_question(book)
        return

    def sort_article(self, book):
        article_list = book['article_list']
        article_list.sort(key=lambda x: x[SettingClass.ARTICLEORDERBY], reverse=SettingClass.ARTICLEORDERBYDESC)
        return

    def sort_question(self, book):
        def sort_answer(answer_list):
            answer_list.sort(key=lambda x: x[SettingClass.ANSWERORDERBY], reverse=SettingClass.ANSWERORDERBYDESC)
            return

        article_list = book['article_list']
        article_list.sort(key=lambda x: x[SettingClass.QUESTIONORDERBY], reverse=SettingClass.QUESTIONORDERBYDESC)
        for item in book['article_list']:
            sort_answer(item['answer_list'])
        return

    def __split(self):
        def split(book, surplus, index=1):
            if book['answer_count'] <= surplus:
                book['split_index'] = index
                return [book]
            article_list = []
            while surplus > 0:
                article = book['article_list'].pop()
                article_list.append(article)
                surplus -= article['answer_count']
                book['answer_count'] -= article['answer_count']
            new_book = book.copy()
            new_book['article_list'] = article_list
            new_book['split_index'] = index
            return [new_book] + split(book, SettingClass.MAXANSWER, index + 1)

        counter = 0
        book_list = []
        while len(self.raw_book_list):
            book = self.raw_book_list.pop()
            if (counter + book['answer_count']) < SettingClass.MAXANSWER:
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
        book['title'] = raw_book['info']['title']
        book['pre_fix'] = index

        page = creator.create_info_page(raw_book['info']['kind'], raw_book['info'], book['pre_fix'])
        book['page_list'].append(page)
        for article in raw_book['article_list']:
            if raw_book['info']['kind'] in TypeClass.article_type:
                page = creator.create_article(article, index)
            else:
                page = creator.create_question(article, index)
            book['page_list'].append(page)
        return book
