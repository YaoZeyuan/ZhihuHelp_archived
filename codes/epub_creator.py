# -*- coding: utf-8 -*-
from image_container import ImageContainer
from filter import Filter, HtmlTranslator
from baseClass import BaseClass
from epub import Book

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
        BaseClass.make_dir(self.base_path + u'/知乎助手生成的电子书')
        BaseClass.make_dir(self.base_path + u'/知乎电子书临时资源库')
        BaseClass.make_dir(self.base_path + u'/知乎电子书临时资源库/知乎图片池')
        return

    def start(self):
        raw_book_list = self.init_book_data()
        book_list = [self.translate_book_into_html(book) for book in raw_book_list]
        for book in book_list:
            BaseClass.change_dir(self.base_path)
            BaseClass.change_dir(self.base_path + u'/知乎电子书临时资源库')
            epub = Book(book['info']['title'], 27149527)
            book.start_download_image()
            for page in book['page_list']:
                with open(self.base_path + u'/知乎电子书临时资源库' + page['filename'], 'w') as html:
                    html.write(page['content'])
                epub.addHtml(self.base_path + u'/知乎电子书临时资源库' + page['filename'], page['title'])
            for filename in book['image_list']:
                epub.addImg(self.base_path + u'/知乎电子书临时资源库/知乎图片池' + filename)
                book.addLanguage('zh-cn')
                epub.addCreator('ZhihuHelp1.7.0')
                epub.addDesc(u'该电子书由知乎助手生成，知乎助手是姚泽源为知友制作的仅供个人使用的简易电子书制作工具，源代码遵循WTFPL，希望大家能认真领会该协议的真谛，为飞面事业做出自己的贡献 XD')
                epub.addRight('CC')
                epub.addPublisher('ZhihuHelp')
                epub.addCss(u'../../../epubResource/markdownStyle.css')
                epub.addCss(u'../../../epubResource/userDefine.css')
                epub.buildingEpub()
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


def create_epub(task):
    return
