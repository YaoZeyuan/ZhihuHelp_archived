# -*- coding: utf-8 -*-
from src.epub.container import Container
from src.epub.content_opf import OPF
from src.epub.inf import INF
from src.epub.mime_type import MimeType
from src.epub.toc import TOC


class Epub(object):
    def __int__(self):
        self.mime_type = MimeType()
        self.meta_inf = INF()
        self.opf = OPF()
        self.toc = TOC()
        self.style_container = Container('style')
        self.html_container = Container('html')
        self.image_container = Container('image')
        return