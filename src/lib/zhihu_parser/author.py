# -*- coding: utf-8 -*-
from src.lib.zhihu_parser.base import BaseParser
from src.lib.zhihu_parser.info.author import AuthorInfo


class AuthorParser(BaseParser):
    def get_extra_info(self):
        author = AuthorInfo(self.dom)
        return author.get_info()
