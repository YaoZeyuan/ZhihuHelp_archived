# -*- coding: utf-8 -*-
from src.epub.tools.epub_path import EpubPath


class MimeType(object):
    def __int__(self):
        self.content = 'application/epub+zip'
        return

    def create(self):
        with open(EpubPath.base_path, 'w') as mimetype:
            mimetype.write(self.content)
        return
