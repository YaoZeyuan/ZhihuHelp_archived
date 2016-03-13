# -*- coding: utf-8 -*-
from .tools.base import Base
from .tools.epub_config import EpubConfig
from .tools.epub_path import EpubPath


class Head(Base):
    def set_uid(self, uid=EpubConfig.uid):
        template = self.get_template('head', 'uid')
        self.uid = template.format(uid=uid)
        return

    def set_depth(self, depth=2):
        template = self.get_template('head', 'depth')
        self.depth = template.format(depth=depth)
        return

    def get_content(self):
        self.content = self.uid + self.depth
        return self.content


class DocTitle(Base):
    def set_title(self, title=EpubConfig.book_title):
        template = self.get_template('doc_title', 'title')
        self.title = template.format(title=title)
        return


class Ncx(Base):
    def create_item(self, resource_id, href, title, extend_nav_point=''):
        template = self.get_template('ncx', 'item')
        content = template.format(resource_id=resource_id, href=href, title=title, extend_nav_point=extend_nav_point)
        return content

    def add_item(self, resource_id, href, title, extend_nav_point=''):
        content = self.create_item(resource_id, href, title, extend_nav_point=extend_nav_point)
        self.content += content
        return

    @staticmethod
    def create_chapter_item(resource_id, href, title, extend_nav_point=''):
        chapter = {
            'chapter': dict(zip(('resource_id', 'href', 'title', 'extend_nav_point'),
                                (resource_id, href, title, extend_nav_point))),
            'content': ''
        }
        return chapter


class TOC(Base):
    def __init__(self):
        self.head = Head()
        self.doc_title = DocTitle()
        self.ncx = Ncx()
        self.chapter_list = []
        self.content = ''
        self.metadata_completed = set()
        return

    def set_title(self, title=EpubConfig.book_title):
        self.doc_title.set_title(title)
        self.metadata_completed.add('title')
        return

    def set_uid(self, uid=EpubConfig.uid):
        self.head.set_uid(uid)
        self.metadata_completed.add('uid')
        return

    def set_depth(self, depth='2'):
        self.head.set_depth(depth)
        return

    def add_item(self, resource_id, href, title, extend_nav_point=''):
        if self.chapter_list:
            self.chapter_list[-1]['content'] += self.ncx.create_item(resource_id, href, title)
        else:
            self.ncx.add_item(resource_id, href, title, extend_nav_point)
        return

    def create_chapter(self, resource_id, href, title):
        chapter = self.ncx.create_chapter_item(resource_id, href, title)
        self.chapter_list += [chapter]
        return

    def finish_chapter(self):
        if not self.chapter_list:
            return
        chapter = self.chapter_list.pop()
        chapter['chapter']['extend_nav_point'] = chapter['content']
        self.add_item(**(chapter['chapter']))
        return

    def create(self):
        self.check()
        self.create_content()
        return

    def check(self):
        self.check_metadata()
        self.finish_all_chapter()
        return

    def finish_all_chapter(self):
        while self.chapter_list:
            self.finish_chapter()
        return

    def check_metadata(self):
        if not 'title' in self.metadata_completed:
            self.set_title()
        if not 'uid' in self.metadata_completed:
            self.set_uid()
        if not 'depth' in self.metadata_completed:
            self.set_depth()
        return

    def create_content(self):
        content = {
            'head': self.head.get_content(),
            'doc_title': self.doc_title.get_content(),
            'nav_point': self.ncx.get_content(),
        }
        template = self.get_template('toc', 'content')
        content = template.format(**content)
        with open(EpubPath.oebps_path + u'/toc.ncx', 'w') as toc:
            toc.write(content)
        return
