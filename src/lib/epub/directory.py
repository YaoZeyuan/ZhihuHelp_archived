# -*- coding: utf-8 -*-
from .zhihuhelp_tools.path import Path
from .tools.base import Base


class Directory(Base):
    def __init__(self):
        Base.__init__(self)
        self.chapter_deep = 0
        return

    def add_html(self, src, title):
        template = self.get_template('directory', 'item_leaf')
        self.content += template.format(href=Path.get_filename(src), title=title)
        return

    def create_chapter(self, src, title):
        template = self.get_template('directory', 'item_root')
        item = template.format(href=Path.get_filename(src), title=title)
        if self.chapter_deep == 0:
            template = self.get_template('directory', 'chapter')
            item = template.format(item=item, title=u'目录')
        self.content += item

        self.chapter_deep += 1
        return

    def finish_chapter(self):
        if self.chapter_deep == 1:
            template = self.get_template('directory', 'finish_chapter')
            self.content += template

        self.chapter_deep -= 1
        return

    def get_content(self):
        template = self.get_template('directory', 'content')
        return template.format(content=self.content)
