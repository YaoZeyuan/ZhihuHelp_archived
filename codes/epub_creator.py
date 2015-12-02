# -*- coding: utf-8 -*-
from image_container import ImageContainer
from rawbook import RawBook
from baseClass import BaseClass
from epub import Book

class EpubCreator(object):
    """
    一次只做一本书
    而且只做知乎相关书目
    """
    def __init__(self, book):
        self.book = book
        self.book_list = book['book_list']
        self.image_container = book['image_container']
        return

    def create(self):
        self.image_container.set_save_path(BaseClass.base_path + u'/知乎电子书临时资源库/知乎图片池/')
        self.image_container.start_download()
        title = '_'.join([book['title'] for book in self.book_list])
        title = title.replace('\r', '').replace('\n', '')
        BaseClass.change_dir(BaseClass.base_path + u'/知乎电子书临时资源库/')
        epub = Book(title, 27149527)
        html_tmp_path = BaseClass.base_path + u'/知乎电子书临时资源库/知乎网页池/'
        image_tmp_path = BaseClass.base_path + u'/知乎电子书临时资源库/知乎图片池/'
        for book in self.book_list:
            page = book['page_list'][0]
            with open(html_tmp_path + page['filename'], 'w') as html:
                html.write(page['content'])
            epub.createChapter(html_tmp_path + page['filename'], BaseClass.get_time(), page['title'])

            for page in book['page_list'][1:]:
                with open(html_tmp_path + page['filename'], 'w') as html:
                    html.write(page['content'])
                epub.addHtml(html_tmp_path + page['filename'], page['title'])
        for image in self.book['image_list']:
            epub.addImg(image_tmp_path + image['filename'])
        epub.addLanguage('zh-cn')
        epub.addCreator('ZhihuHelp1.7.0')
        epub.addDesc(u'该电子书由知乎助手生成，知乎助手是姚泽源为知友制作的仅供个人使用的简易电子书制作工具，源代码遵循WTFPL，希望大家能认真领会该协议的真谛，为飞面事业做出自己的贡献 XD')
        epub.addRight('CC')
        epub.addPublisher('ZhihuHelp')
        BaseClass.logger.debug(u'当前目录为')
        BaseClass.printCurrentDir()
        epub.addCss(BaseClass.base_path + u'/epubResource/markdown.css')
        epub.addCss(BaseClass.base_path + u'/epubResource/front.css')
        epub.buildingEpub()
        return


def create_epub(task):
    """
    传入的为一个list的电子书，不能明确电子书的种类，也不能知道list中有多少电子书
    所以最终生成的时候，需要将所有电子书都合并在一个包里，每本书为一个章节
    """
    raw_book = RawBook(task['book_list'])
    book_list = raw_book.get_book_list()
    for book in book_list:
        epub = EpubCreator(book)
        epub.create()
    return
