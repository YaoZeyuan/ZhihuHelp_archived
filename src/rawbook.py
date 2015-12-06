# -*- coding: utf-8 -*-
import copy
from src.container.book import Page, EpubBook
from src.container.image import ImageContainer
from src.tools.config import Config
from src.tools.path import Path
from src.tools.type import Type

import re


class CreateHtmlPage(object):
    u"""
    工具类，用于生成html页面
    """

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

        if Config.picture_quality == 0:
            return ''
        if 'equation?tex=' in href:  # tex图片不必处理
            return href
        if Config.picture_quality == 1:
            return href
        if Config.picture_quality == 2:
            if not ('_' in href):
                return href
            pos = href.rfind('_')
            return href[:pos] + href[pos + 2:]  # 删除'_m'等图片质量控制符，获取原图
        return href

    def create_question(self, question, prefix=''):
        def create_answer(answer):
            with open('./src/template/content/answer.html') as answer_temp:
                template = answer_temp.read()
            return template.format(**answer)

        answer_content = ''.join([create_answer(answer) for answer in question['answer_list']])
        question['answer_content'] = answer_content
        with open('./src/template/content/question.html') as question_temp:
            template = question_temp.read()
        question.update(question['question'])
        content = template.format(**question)
        page = Page()
        page.content = self.fix_image(content)
        page.filename = str(prefix) + str(question['question_id']) + '.html'
        page.title = question['title']
        return page

    def create_article(self, article, prefix=''):
        with open('./src/template/content/article.html') as article_temp:
            template = article_temp.read()
        content = template.format(**article)
        page = Page()
        page.content = self.fix_image(content)
        page.filename = prefix + str(article['article_id']) + '.html'
        page.title = article['title']
        return page

    def create_info_page(self, book):
        kind = book.kind
        info = book.info
        Path.pwd()
        with open('./src/template/info/{}.html'.format(kind)) as file:
            template = file.read()
        content = template.format(**info)
        page = Page()
        page.content = self.fix_image(content)
        page.filename = str(book.epub.prefix) + 'info.html'
        page.title = book.epub.title
        if book.epub.split_index:
            page.title += "_({})".format(book.epub.split_index)
        return page


class RawBook(object):
    u"""
    负责数据进行处理,返回处理完毕的html信息和所有待下载图片的imgContainer
    """

    def __init__(self, raw_book_list):
        self.book_list = self.merge_raw_info(raw_book_list)
        self.result_list = []
        return

    def merge_raw_info(self, raw_book_list):
        book_list = []
        for kind in Type.type_list:
            if not kind in raw_book_list:
                continue
            for book in raw_book_list[kind]:
                book_list.append(book)
        return book_list

    def get_book_list(self):
        self.book_list = [x.catch_data() for x in self.book_list]
        self.split()
        book_list = []
        for item in self.result_list:
            book = self.create_book(item)
            book_list.append(book)
        return book_list

    def split(self):
        def split(book, surplus, index=1):
            if book.epub.answer_count <= surplus:
                book.epub.split_index = index
                return [book]
            article_list = []
            while surplus > 0:
                article = book.article_list.pop()
                article_list.append(article)
                surplus -= article['answer_count']
                book.epub.answer_count -= article['answer_count']
            new_book = copy.deepcopy(book)
            new_book.set_article_list(article_list)
            new_book.epub.split_index = index
            return [new_book] + split(book, Config.max_answer, index + 1)

        counter = 0
        book_list = []
        while len(self.book_list):
            book = self.book_list.pop()
            if (counter + book.epub.answer_count) < Config.max_answer:
                book_list.append(book)
            else:
                split_list = split(book, Config.max_answer - counter)
                book_list.append(split_list[0])
                self.result_list.append(book_list)
                self.book_list += split_list[1:]
                counter = 0
        self.result_list.append(book_list)
        return

    def create_book(self, book_list):
        index = 0
        epub_book_list = []
        image_container = ImageContainer()
        creator = CreateHtmlPage(image_container)
        for book in book_list:
            epub_book = self.create_single_book(book, index, creator)
            epub_book_list.append(epub_book)
            index += 1

        book_package = EpubBook()
        book_package.book_list = epub_book_list
        book_package.image_list = image_container.get_filename_list()
        book_package.image_container = image_container
        return book_package

    def create_single_book(self, book, index, creator):
        if book.epub.split_index:
            book.epub.title += "_({})".format(book.epub.split_index)

        book.epub.prefix = index

        page = creator.create_info_page(book)
        book.page_list.append(page)
        for article in book.article_list:
            if book.kind in Type.article_type_list:
                page = creator.create_article(article, index)
            else:
                page = creator.create_question(article, index)
            book.page_list.append(page)
        return book
