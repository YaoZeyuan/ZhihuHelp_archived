# -*- coding: utf-8 -*-
import shutil

from rawbook import RawBook
from src.lib.epub.epub import Epub
from src.tools.match import Match
from src.tools.path import Path
from src.tools.template_config import TemplateConfig


class EpubCreator(object):
    """
    一次只做一本书
    而且只做知乎相关书目
    """

    def __init__(self, epub_book):
        self.book = epub_book
        self.book_list = epub_book.book_list
        self.image_container = epub_book.image_container
        return

    def create_single_html_book(self):
        title = '_'.join([book.epub.title for book in self.book_list])
        title = Match.fix_filename(title) # 移除特殊字符,控制文件名长度
        if not title:
            # 电子书题目为空时自动跳过
            # 否则会发生『rm -rf / 』的惨剧。。。
            return
        Path.reset_path()
        Path.chdir(Path.result_path)
        Path.rmdir(u'./' + title)
        Path.mkdir(u'./' + title)
        Path.chdir(u'./' + title)
        page = []
        for book in self.book_list:
            page += book.page_list
        content = u' \r\n '.join([Match.html_body(x.content) for x in page]).replace(u'../images/', u'./images/')
        with open(TemplateConfig.content_base_uri) as html:
            content = html.read().format(title=title, body=content).replace(u'../style/',u'./')
        with open(title + u'.html', 'w') as html:
            html.write(content)
        shutil.copytree(Path.html_pool_path + u'/../{}/OEBPS/images'.format(title), u'./images')
        shutil.copy(Path.www_css + u'/customer.css' , u'./customer.css')
        shutil.copy(Path.www_css + u'/markdown.css' , u'./markdown.css')
        shutil.copy(Path.www_css + u'/normalize.css' , u'./normalize.css')
        Path.reset_path()
        return

    def create(self):
        self.image_container.set_save_path(Path.image_pool_path)
        self.image_container.start_download()
        title = '_'.join([book.epub.title for book in self.book_list])
        title = Match.fix_filename(title) # 移除特殊字符
        if not title:
            # 电子书题目为空时自动跳过
            # 否则会发生『rm -rf / 』的惨剧。。。
            return
        Path.chdir(Path.base_path + u'/知乎电子书临时资源库/')
        epub = Epub(title)
        html_tmp_path = Path.html_pool_path + u'/'
        image_tmp_path = Path.image_pool_path + u'/'
        epub.set_creator(u'ZhihuHelp1.7.0')
        epub.set_book_id()
        epub.add_css(Path.base_path + u'/www/css/markdown.css')
        epub.add_css(Path.base_path + u'/www/css/customer.css')
        epub.add_css(Path.base_path + u'/www/css/normalize.css')
        for book in self.book_list:
            page = book.page_list[0]
            with open(html_tmp_path + page.filename, u'w') as html:
                html.write(page.content)
            epub.create_chapter(html_tmp_path + page.filename, page.title)
            for page in book.page_list[1:]:
                with open(html_tmp_path + page.filename, u'w') as html:
                    html.write(page.content)
                epub.add_html(html_tmp_path + page.filename, page.title)
            epub.finish_chapter()
        for image in self.book.image_list:
            epub.add_image(image_tmp_path + image['filename'])


        epub.create()
        Path.reset_path()
        return


def create_epub(task_package):
    """
    传入的为一个list的电子书，不能明确电子书的种类，也不能知道list中有多少电子书
    所以最终生成的时候，需要将所有电子书都合并在一个包里，每本书为一个章节
    """
    raw_book = RawBook(task_package.book_list)
    epub_book_list = raw_book.get_book_list()
    for book in epub_book_list:
        epub = EpubCreator(book)
        epub.create()
        epub.create_single_html_book()
    return
