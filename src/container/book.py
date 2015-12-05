# -*- coding: utf-8 -*-

class BookProperty(object):
    class Sql(object):
        def __init__(self):
            self.question = ''
            self.answer = ''
            self.info = ''
            return

    class Epub(object):
        def __init__(self):
            self.article_count = 0
            self.answer_count = 0
            self.agree_count = 0
            self.char_count = 0

            self.title = ''
            self.id = ''
            self.split_index = 0
            return

    def __init__(self):
        self.sql = BookProperty.Sql()
        self.epub = BookProperty.Epub()
        return


class Book(object):
    def __init__(self):
        self.kind = ''
        self.property = BookProperty()
        self.info = {}
        self.split_index = 0
        self.article_list = []
        self.page_list = []
        return
