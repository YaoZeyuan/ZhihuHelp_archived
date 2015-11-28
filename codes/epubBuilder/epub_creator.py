# -*- coding: utf-8 -*-
from image_container import ImageContainer
from filter import Filter, HtmlTranslator
from baseClass import BaseClass


class EpubCreator(object):
    """
    一次只做一本书
    而且只做知乎相关书目
    """

    def __init__(self, book_list, base_path):
        self.book_list = book_list
        self.base_path = base_path
        self.book_container = []
        self.image_container = ImageContainer()
        self.init_base_dir()
        return

    def init_base_dir(self):
        BaseClass.mkdir(self.base_path + u'/知乎助手生成的电子书')
        BaseClass.mkdir(self.base_path + u'/知乎电子书临时资源库')
        BaseClass.mkdir(self.base_path + u'/知乎电子书临时资源库/知乎图片池')
        return

    def start(self):
        raw_book_list = self.init_book_data()
        book_list = [self.translate_book_into_html(book) for book in raw_book_list]
        return

    def init_book_data(self):
        raw_book_data_list = []
        for raw_book_info in self.book_list:
            raw_book = self.parse_data(raw_book_info)
            raw_book_data_list.append(raw_book)
        return raw_book_data_list

    def translate_book_into_html(self, book):
        translator = HtmlTranslator(book)
        return translator.start()

    def parse_data(self, raw_book_info):
        raw_data = Filter(raw_book_info)
        return raw_data.get_book()

    def create_book(self, info):

        return
