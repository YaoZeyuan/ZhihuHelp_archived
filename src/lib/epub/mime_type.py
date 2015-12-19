# -*- coding: utf-8 -*-
from src.lib.epub.tools.epub_path import EpubPath


class MimeType(object):
    def __init__(self):
        self.content = u'application/epub+zip'
        return

    def create(self):
        with open(EpubPath.base_path + '/mimetype', 'w') as mimetype:
            mimetype.write(self.content)
        return
