# -*- coding: utf-8 -*-
from src.epub.base import Base


class Head(Base):
    def add_uid(self,uid='urn:uuid:create-by-yao-ze-yuan-Tsingtao'):
        template = self.get_template('head', 'uid')
        self.content += template.format(uid=uid)
        return

    def add_depth(self,depth=2):
        template = self.get_template('head', 'depth')
        self.content += template.format(depth=depth)
        return

class DocTitle(Base):
    def add_title(self,title):
        template = self.get_template('doc_title', 'title')
        self.content += template.format(title=title)
        return


class Ncx(Base):
    def create_item(self, id, href, title, extend_nav_point = ''):
        template = self.get_template('ncx', 'item')
        content = template.format(id=id,herf=href,title=title, extend_nav_point=extend_nav_point)
        return content

    def add_item(self, id, href, title, extend_nav_point = ''):
        content = self.create_item(id, href, title, extend_nav_point = '')
        self.content += content
        return


class TOC(object):
    def __init__(self):
        self.head = Head()
        self.doc_title = DocTitle()
        self.ncx = Ncx()
        return