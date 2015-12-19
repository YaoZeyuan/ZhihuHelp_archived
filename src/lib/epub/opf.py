# -*- coding: utf-8 -*-
from .tools.base import Base
from .tools.epub_config import EpubConfig
from .tools.epub_path import EpubPath


class Metadata(Base):
    def set_title(self, title=EpubConfig.book_title):
        template = self.get_template('metadata', 'title')
        self.title = template.format(title=title)
        return

    def set_creator(self, creator=EpubConfig.creator):
        template = self.get_template('metadata', 'creator')
        self.creator = template.format(creator=creator)
        return

    def set_book_id(self, book_id=EpubConfig.book_id, uid=EpubConfig.uid):
        template = self.get_template('metadata', 'book_id')
        self.book_id = template.format(book_id=book_id, uid=uid)
        return

    def set_cover(self, image_id):
        template = self.get_template('metadata', 'cover')
        self.cover = template.format(image_id=image_id)
        return

    def get_content(self):
        for key in ['title', 'creator', 'book_id', 'cover']:
            if hasattr(self, key):
                self.content += getattr(self, key)
        return self.content


class Manifest(Base):
    resource_id = 0

    def get_resource_id(self):
        Manifest.resource_id += 1
        return str(Manifest.resource_id)

    def add_css(self, href):
        resource_id = self.get_resource_id()
        self.add_item(resource_id, href, 'text/css')
        return resource_id

    def add_image(self, href):
        u"""
        只允许添加jpg格式的图片
        至少后缀名要改成jpg
        """
        resource_id = self.get_resource_id()
        self.add_item(resource_id, href, 'image/jpeg')
        return resource_id

    def add_html(self, href):
        resource_id = self.get_resource_id()
        self.add_item(resource_id, href, 'application/xhtml+xml')
        return resource_id

    def add_item(self, resource_id, href, media_type):
        template = self.get_template('manifest', 'item')
        self.content += template.format(resource_id=resource_id, href=href, media_type=media_type)
        return


class Spine(Base):
    def add_item(self, resource_id):
        template = self.get_template('spine', 'item')
        self.content += template.format(resource_id=resource_id)
        return

    def add_item_nolinear(self, resource_id):
        template = self.get_template('spine', 'item_nolinear')
        self.content += template.format(resource_id=resource_id)
        return


class Guide(Base):
    def add_cover(self, href, title='Cover'):
        template = self.get_template('guide', 'item')
        self.content += template.format(href=href, title=title, item_type='Cover')
        return

    def add_title_page(self, href, title='title_page'):
        template = self.get_template('guide', 'item')
        self.content += template.format(href=href, title=title, item_type='title-page')
        return

    def add_index(self, href, title='index'):
        template = self.get_template('guide', 'item')
        self.content += template.format(href=href, title=title, item_type='toc')
        return


class OPF(Base):
    def __init__(self):
        self.guide = Guide()
        self.manifest = Manifest()
        self.metadata = Metadata()
        self.spine = Spine()
        self.metadata_completed = set()
        self.uid = EpubConfig.uid
        return

    def set_title(self, title=EpubConfig.book_title):
        self.metadata.set_title(title)
        self.metadata_completed.add('title')
        return

    def set_creator(self, creator=EpubConfig.creator):
        self.metadata.set_creator(creator)
        self.metadata_completed.add('creator')
        return

    def set_book_id(self, book_id=EpubConfig.book_id, uid=EpubConfig.uid):
        self.metadata.set_book_id(book_id, uid=uid)
        self.metadata_completed.add('book_id')
        self.uid = uid
        return

    def add_html(self, src):
        resource_id = self.manifest.add_html(src)
        self.spine.add_item(resource_id)
        return resource_id

    def add_css(self, src):
        resource_id = self.manifest.add_css(src)
        return resource_id

    def add_image(self, src):
        resource_id = self.manifest.add_image(src)
        return resource_id

    def add_title_page_html(self, src):
        resource_id = self.manifest.add_html(src)
        self.spine.add_item_nolinear(resource_id)
        self.guide.add_title_page(src)
        return resource_id

    def add_cover_image(self, src):
        resource_id = self.manifest.add_image(src)
        self.guide.add_cover(src)
        self.metadata.set_cover(resource_id)
        return resource_id

    def add_index(self, src):
        resource_id = self.manifest.add_html(src)
        self.guide.add_index(src)
        return resource_id

    def create(self):
        self.check_metadate()
        self.create_content()
        return

    def check_metadate(self):
        if not 'title' in self.metadata_completed:
            self.set_title()
        if not 'creator' in self.metadata_completed:
            self.set_creator()
        if not 'book_id' in self.metadata_completed:
            print u'请先设置book_id!'
            exit()
        return

    def create_content(self):
        content = {
            'metadata': self.metadata.get_content(),
            'manifest': self.manifest.get_content(),
            'spine': self.spine.get_content(),
            'guide': self.guide.get_content(),
            'uid': self.uid,
        }
        template = self.get_template('opf', 'content')
        content = template.format(**content)
        with open(EpubPath.oebps_path + u'/content.opf', 'w') as opf:
            opf.write(content)
        return
