# -*- coding: utf-8 -*-
from src.epub.opf import OPF
from src.epub.inf import INF
from src.epub.mime_type import MimeType
from src.epub.toc import TOC
from src.epub.tools.epub_config import EpubConfig
from src.epub.tools.epub_path import EpubPath
from src.tools.path import Path


class Epub(object):
    def __init__(self, title):
        self.mime_type = MimeType()
        self.meta_inf = INF()
        self.opf = OPF()
        self.toc = TOC()
        self.title = title
        self.set_title(title)
        self.init_path()
        return

    def init_path(self):
        Path.reset_path()
        Path.rmdir(self.title)
        Path.mkdir(self.title)
        Path.chdir(self.title)
        EpubPath.init_epub_path(Path.get_pwd())
        return

    def add_html(self, src, title):
        Path.copy(src, EpubPath.html_path)
        filename = Path.get_filename(src)
        new_src = 'html/' + filename
        resource_id = self.opf.add_html(new_src)
        self.toc.add_item(resource_id, new_src, title)
        return

    def add_css(self, src):
        Path.copy(src, EpubPath.css_path)
        filename = Path.get_filename(src)
        new_src = 'css/' + filename
        resource_id = self.opf.add_css(new_src)
        return

    def add_image(self, src):
        Path.copy(src, EpubPath.image_path)
        filename = Path.get_filename(src)
        new_src = 'image/' + filename
        resource_id = self.opf.add_image(new_src)
        return

    def add_title_page_html(self, src, title):
        Path.copy(src, EpubPath.html_path)
        filename = Path.get_filename(src)
        new_src = 'html/' + filename
        resource_id = self.opf.add_title_page_html(new_src)
        self.toc.add_item(resource_id, new_src, title)
        return

    def add_cover_image(self, src):
        Path.copy(src, EpubPath.image_path)
        filename = Path.get_filename(src)
        new_src = 'image/' + filename
        resource_id = self.opf.add_cover_image(new_src)
        return

    def create(self):
        self.meta_inf.add_container()
        self.meta_inf.add_duokan_ext()
        self.mime_type.create()
        self.opf.create()
        self.toc.create()
        return

    def create_chapter(self, src, title):
        Path.copy(src, EpubPath.html_path)
        filename = Path.get_filename(src)
        new_src = 'html/' + filename
        resource_id = self.opf.add_title_page_html(new_src)
        self.toc.create_chapter(resource_id, new_src, title)
        return

    def finish_chapter(self):
        self.toc.finish_chapter()
        return

    def set_title(self, title):
        self.toc.set_title(title)
        self.opf.set_title(title)
        return

    def set_creator(self, creator):
        self.opf.set_creator(creator)
        return

    def set_book_id(self,book_id=EpubConfig.book_id, uid=EpubConfig.uid):
        self.opf.set_book_id(book_id,uid)
        self.toc.set_uid(uid)
        return
