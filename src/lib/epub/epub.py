# -*- coding: utf-8 -*-
import os
import zipfile

from .directory import Directory
from .inf import INF
from .mime_type import MimeType
from .opf import OPF
from .toc import TOC
from .tools.epub_config import EpubConfig
from .tools.epub_path import EpubPath
from .zhihuhelp_tools.debug import Debug
from .zhihuhelp_tools.path import Path


class Epub(object):
    def __init__(self, title):
        self.mime_type = MimeType()
        self.meta_inf = INF()
        self.opf = OPF()
        self.toc = TOC()
        self.directory = Directory()
        self.title = title
        self.set_title(title)
        self.init_path()
        self.init_index()
        return

    def init_index(self):
        # 目录先放图片文件夹里
        open(EpubPath.style_path + u'/index.xhtml', 'w')
        self.add_html(EpubPath.style_path + u'/index.xhtml', u'目录')
        return

    def write_index(self):
        with open(EpubPath.html_path + u'/index.xhtml', 'w') as index:
            index.write(self.directory.get_content())
        return

    def init_path(self):
        Path.rmdir(u'./' + self.title)
        Path.mkdir(u'./' + self.title)
        Path.chdir(u'./' + self.title)
        EpubPath.init_epub_path(Path.get_pwd())
        return

    @staticmethod
    def set_output_path(output_path):
        EpubPath.set_output_path(output_path)
        return

    def add_html(self, src, title):
        Path.copy(src, EpubPath.html_path)
        filename = Path.get_filename(src)
        new_src = u'html/' + filename
        resource_id = self.opf.add_html(new_src)
        self.directory.add_html(new_src, title)
        self.toc.add_item(resource_id, new_src, title)
        return

    def add_css(self, src):
        Path.copy(src, EpubPath.style_path)
        filename = Path.get_filename(src)
        new_src = u'style/' + filename
        resource_id = self.opf.add_css(new_src)
        return

    def add_image(self, src):
        Path.copy(src, EpubPath.image_path)
        filename = Path.get_filename(src)
        new_src = u'image/' + filename
        resource_id = self.opf.add_image(new_src)
        return

    def add_title_page_html(self, src, title):
        Path.copy(src, EpubPath.html_path)
        filename = Path.get_filename(src)
        new_src = u'html/' + filename
        resource_id = self.opf.add_title_page_html(new_src)
        self.directory.add_html(new_src, title)
        self.toc.add_item(resource_id, new_src, title)
        return

    def add_cover_image(self, src):
        Path.copy(src, EpubPath.image_path)
        filename = Path.get_filename(src)
        new_src = u'image/' + filename
        resource_id = self.opf.add_cover_image(new_src)
        return

    def create(self):
        self.meta_inf.add_container()
        self.meta_inf.add_duokan_ext()
        self.mime_type.create()
        self.opf.create()
        self.toc.create()
        self.write_index()
        self.zip_to_epub()
        return

    def zip_to_epub(self):
        epub_name = self.title + u'.epub'
        file_path = EpubPath.output_path + '/' + epub_name
        EpubPath.reset_path()
        epub = zipfile.ZipFile(file=file_path, mode='w', compression=zipfile.ZIP_STORED, allowZip64=True)
        epub.write('./mimetype')
        for parent, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                if filename in [epub_name, 'mimetype']:
                    continue
                Debug.print_in_single_line(u'将{}添加至电子书内'.format(filename))
                epub.write(parent + '/' + filename, compress_type=zipfile.ZIP_STORED)
        epub.close()
        return

    def create_chapter(self, src, title):
        Path.copy(src, EpubPath.html_path)
        filename = Path.get_filename(src)
        new_src = u'html/' + filename
        resource_id = self.opf.add_title_page_html(new_src)
        self.directory.create_chapter(new_src, title)
        self.toc.create_chapter(resource_id, new_src, title)
        return

    def finish_chapter(self):
        self.directory.finish_chapter()
        self.toc.finish_chapter()
        return

    def set_title(self, title):
        self.toc.set_title(title)
        self.opf.set_title(title)
        return

    def set_creator(self, creator):
        self.opf.set_creator(creator)
        return

    def set_book_id(self, book_id=EpubConfig.book_id, uid=EpubConfig.uid):
        self.opf.set_book_id(book_id, uid)
        self.toc.set_uid(uid)
        return
