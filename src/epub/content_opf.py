# -*- coding: utf-8 -*-
from src.epub.base import Base

class Metadata(Base):
    def add_title(self, title):
        template = self.get_template('metadata', 'cover')
        self.content += template.format(title=title)
        return

    def add_creator(self, creator):
        template = self.get_template('metadata', 'creator')
        self.content += template.format(creator=creator)
        return

    def add_identifier(self, book_id, uid='urn:uuid:create-by-yao-ze-yuan-Tsingtao'):
        template = self.get_template('metadata', 'identifier')
        self.content += template.format(book_id=book_id, uid=uid)
        return

    def add_cover(self, image_id):
        template = self.get_template('metadata', 'cover')
        self.content += template.format(image_id=image_id)
        return


class Manifest(Base):
    id = 0

    def get_id(self):
        Manifest.id += 1
        return str(Manifest.id)

    def add_css(self, href):
        id = self.get_id()
        self.add_item(id, href, 'text/css')
        return id

    def add_image(self, href):
        u"""
        只允许添加jpg格式的图片
        至少后缀名要改成jpg
        """
        id = self.get_id()
        self.add_item(id, href, 'image/jpeg')
        return id

    def add_html(self, href):
        id = self.get_id()
        self.add_item(id, href, 'application/xhtml+xml')
        return id

    def add_item(self, id, href, media_type):
        template = self.get_template('metadata', 'item')
        self.content += template.format(id=id, href=href, media_type=media_type)
        return

class Spine(Base):
    def add_item(self,id):
        template = self.get_template('spine', 'item')
        self.content += template.format(id=id)
        return

    def add_item_nolinear(self,id):
        template = self.get_template('spine', 'item_nolinear')
        self.content += template.format(id=id)
        return

class Guide(Base):
    def add_cover(self,href, title):
        template = self.get_template('guide', 'item')
        self.content += template.format(href=href, title=title, item_type='Cover')
        return

    def add_title_page(self,href, title):
        template = self.get_template('guide', 'item')
        self.content += template.format(href=href, title=title, item_type='title-page')
        return

    def add_index(self,href, title):
        template = self.get_template('guide', 'item')
        self.content += template.format(href=href, title=title, item_type='toc')
        return

class OPF(object):
    def __init__(self):
        self.guide = Guide()
        self.manifest = Manifest()
        self.metadata = Metadata()
        self.spine = Spine()
        return
