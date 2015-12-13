# -*- coding: utf-8 -*-
import copy
from src.container.book import EpubBook
from src.container.image import ImageContainer
from src.tools.config import Config
from src.tools.create_html import CreateHtml
from src.tools.match import Match
from src.tools.path import Path
from src.tools.type import Type

import re


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
            if (book.epub.answer_count <= surplus) or (book.epub.article_count <= 1):
                book.epub.split_index = index
                return [book]
            article_list = []
            while surplus > 0:
                article = book.article_list[0]
                book.article_list = book.article_list[1:]
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
            elif (counter + book.epub.answer_count) == Config.max_answer:
                book_list.append(book)
                self.result_list.append(book_list)
                book_list = []
                counter = 0
            elif (counter + book.epub.answer_count) > Config.max_answer:
                split_list = split(book, Config.max_answer - counter)
                book_list.append(split_list[0])
                self.result_list.append(book_list)
                book_list = []
                counter = 0
                self.book_list = split_list[1:] + self.book_list
        self.result_list.append(book_list)
        return

    def create_book(self, book_list):
        index = 0
        epub_book_list = []
        image_container = ImageContainer()
        creator = CreateHtml(image_container)
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
