# -*- coding: utf-8 -*-
import copy

from src.container.initialbook import HtmlBookPackage
from src.container.image import ImageContainer
from src.lib.epub.epub import Epub
from src.tools.config import Config
from src.tools.html_creator import HtmlCreator
from src.tools.match import Match
from src.tools.path import Path
from src.tools.template_config import TemplateConfig
from src.tools.type import Type


class Book(object):
    u"""
    负责将Book转换为Epub
    """

    def __init__(self, raw_sql_book_list):
        raw_book_list = [book.catch_data() for book in self.flatten(raw_sql_book_list)]
        book_list = self.volume_book(raw_book_list)
        self.book_list = [self.create_book_package(book) for book in book_list]
        return

    @staticmethod
    def flatten(task_list):
        book_list = []
        for kind in Type.type_list:
            if kind in task_list:
                book_list += task_list[kind]
        return book_list

    @staticmethod
    def volume_book(raw_book_list):
        def split(raw_book, surplus, index=1):
            if (raw_book.epub.answer_count <= surplus) or (raw_book.epub.article_count <= 1):
                raw_book.epub.split_index = index
                return [raw_book]
            article_list = []
            while surplus > 0:
                article = raw_book.article_list[0]
                raw_book.article_list = raw_book.article_list[1:]
                article_list.append(article)
                surplus -= article['answer_count']
                raw_book.epub.answer_count -= article['answer_count']
            book = copy.deepcopy(raw_book)
            book.set_article_list(article_list)
            book.epub.split_index = index
            return [book] + split(raw_book, Config.max_answer, index + 1)

        counter = 0
        book = []
        book_list = []
        while len(raw_book_list):
            raw_book = raw_book_list.pop()
            if not raw_book.epub.answer_count:
                # 若书中没有答案则直接跳过
                continue
            if (counter + raw_book.epub.answer_count) < Config.max_answer:
                book.append(raw_book)
            elif (counter + raw_book.epub.answer_count) == Config.max_answer:
                book.append(raw_book)
                book_list.append(book)
                book = []
                counter = 0
            elif (counter + raw_book.epub.answer_count) > Config.max_answer:
                split_list = split(raw_book, Config.max_answer - counter)
                book.append(split_list[0])
                book_list.append(book)
                book = []
                counter = 0
                raw_book_list = split_list[1:] + raw_book_list
        book_list.append(book)
        return book_list

    def book_to_html(self, book, index, creator):
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

    def create_book_package(self, book_list):
        index = 0
        epub_book_list = []
        image_container = ImageContainer()
        creator = HtmlCreator(image_container)
        for book in book_list:
            epub_book = self.book_to_html(book, index, creator)
            epub_book_list.append(epub_book)
            index += 1

        book_package = HtmlBookPackage()
        book_package.book_list = epub_book_list
        book_package.image_list = image_container.get_filename_list()
        book_package.image_container = image_container
        return book_package

    def create_book(self, book_package):
        book_package.image_container.set_save_path(Path.image_pool_path)
        book_package.image_container.start_download()
        title = book_package.get_title()
        if not title:
            # 电子书题目为空时自动跳过
            # 否则会发生『rm -rf / 』的惨剧
            return
        Path.chdir(Path.base_path + u'/知乎电子书临时资源库/')
        epub = Epub(title)
        html_tmp_path = Path.html_pool_path + u'/'
        image_tmp_path = Path.image_pool_path + u'/'
        epub.set_creator(u'ZhihuHelp1.7.0')
        epub.set_book_id()
        epub.set_output_path(Path.result_path)
        epub.add_css(Path.base_path + u'/www/css/markdown.css')
        epub.add_css(Path.base_path + u'/www/css/customer.css')
        epub.add_css(Path.base_path + u'/www/css/normalize.css')
        for book in book_package.book_list:
            page = book.page_list[0]
            with open(html_tmp_path + page.filename, u'w') as html:
                html.write(page.content)
            epub.create_chapter(html_tmp_path + page.filename, page.title)
            for page in book.page_list[1:]:
                with open(html_tmp_path + page.filename, u'w') as html:
                    html.write(page.content)
                epub.add_html(html_tmp_path + page.filename, page.title)
            epub.finish_chapter()
        for image in book_package.image_list:
            epub.add_image(image_tmp_path + image['filename'])
        epub.create()
        Path.reset_path()
        return

    def create_single_html_book(self, book_package):
        title = book_package.get_title()
        if not title:
            # 电子书题目为空时自动跳过
            # 否则会发生『rm -rf / 』的惨剧
            return
        Path.reset_path()
        Path.chdir(Path.result_path)
        Path.rmdir(u'./' + title)
        Path.mkdir(u'./' + title)
        Path.chdir(u'./' + title)
        page = []
        for book in book_package.book_list:
            page += book.page_list
        content = u' \r\n '.join([Match.html_body(x.content) for x in page]).replace(u'../images/', u'./images/')
        with open(TemplateConfig.content_base_uri) as html:
            content = html.read().format(title=title, body=content).replace(u'../style/', u'./')
        with open(title + u'.html', 'w') as html:
            html.write(content)
        Path.copy(Path.html_pool_path + u'/../{}/OEBPS/images'.format(title), u'./images')
        Path.copy(Path.www_css + u'/customer.css', u'./customer.css')
        Path.copy(Path.www_css + u'/markdown.css', u'./markdown.css')
        Path.copy(Path.www_css + u'/normalize.css', u'./normalize.css')
        Path.reset_path()
        return

    def create(self):
        for book_package in self.book_list:
            self.create_book(book_package)
            self.create_single_html_book(book_package)
        return
