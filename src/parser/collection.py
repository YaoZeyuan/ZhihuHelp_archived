# -*- coding: utf-8 -*-
from src.parser.author import AuthorParser
from src.parser.info.collection import CollectionInfo


class CollectionParser(AuthorParser):
    def get_answer_dom_list(self):
        return self.dom.select('div.zm-item')

    def get_extra_info(self):
        collection = CollectionInfo(self.dom)
        return collection.get_info()
