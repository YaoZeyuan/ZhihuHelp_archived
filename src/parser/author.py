# -*- coding: utf-8 -*-
class AuthorParser(BaseParser):
    def get_extra_info(self):
        author = AuthorInfo(self.dom)
        return author.get_info()
