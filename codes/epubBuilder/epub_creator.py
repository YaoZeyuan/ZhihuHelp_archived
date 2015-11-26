# -*- coding: utf-8 -*-
from image_container import ImageContainer
from filter import Filter
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

    def init_book_data(self):
        raw_book_data_list = []
        for raw_book_info in self.book_list:
            data = self.parse_data(raw_book_info)
            raw_book_data_list.append(data)
        return raw_book_data_list

    def parse_data(self, raw_book_info):
        data = Filter(raw_book_info)
        return data

    def create_book(self, info):

        return
