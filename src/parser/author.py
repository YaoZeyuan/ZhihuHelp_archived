# -*- coding: utf-8 -*-
from src.parser.base import BaseParser
from src.parser.info.author import AuthorInfo


class AuthorParser(BaseParser):
    def get_extra_info(self):
        author = AuthorInfo(self.dom)
        return author.get_info()
