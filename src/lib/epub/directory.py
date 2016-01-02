# -*- coding: utf-8 -*-
from .zhihuhelp_tools.path import Path
from .tools.base import Base


class Directory(Base):
    def add_html(self, src, title):
        template = self.get_template('directory', 'html')
        self.content += template.format(href=Path.get_filename(src), title=title)
        return

    def create_chapter(self, src, title):
        template = self.get_template('directory', 'html')
        item = template.format(href=Path.get_filename(src), title=title)
        template = self.get_template('directory', 'chapter')
        self.content += template.format(item=item)
        return

    def finish_chapter(self):
        template = self.get_template('directory', 'finish_chapter')
        self.content += template
        return

    def get_content(self):
        template = self.get_template('directory', 'content')
        return template.format(content=self.content)
