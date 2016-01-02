# -*- coding: utf-8 -*-
from src.container.initialbook import InitialBook
from src.tools.type import Type


class Spider(object):
    def __init__(self):
        self.href = ''
        return


class SingleTask(object):
    u"""
    任务信息应当以对象属性的方式进行存储，用字典存的话记不住
    """

    def __init__(self):
        self.kind = ''
        self.spider = Spider()
        self.book = InitialBook()
        return


class TaskPackage():
    def __init__(self):
        self.work_list = {}
        self.book_list = {}
        return

    def add_task(self, single_task=SingleTask()):
        if not single_task.kind in self.work_list:
            self.work_list[single_task.kind] = []
        self.work_list[single_task.kind].append(single_task.spider.href)

        if not single_task.kind in self.book_list:
            self.book_list[single_task.kind] = []
        self.book_list[single_task.kind].append(single_task.book)
        return

    def get_task(self):
        if Type.answer in self.book_list:
            self.merge_question_book_list(book_type=Type.answer)
        if Type.question in self.book_list:
            self.merge_question_book_list(book_type=Type.question)
        if Type.article in self.book_list:
            self.merge_article_book_list()
        return self

    def merge_article_book_list(self):
        book_list = self.book_list[Type.article]
        book = InitialBook()
        answer = [item.sql.answer for item in book_list]
        info = [item.sql.info for item in book_list]
        book.kind = Type.article
        book.sql.info = 'select * from Article where ({})'.format(' or '.join(info))
        book.sql.answer = 'select * from Article where ({})'.format(' or '.join(answer))
        self.book_list[Type.article] = [book]
        return

    def merge_question_book_list(self, book_type):
        book_list = self.book_list[book_type]
        book = InitialBook()
        question = [item.sql.question for item in book_list]
        answer = [item.sql.answer for item in book_list]
        info = [item.sql.info for item in book_list]
        book.kind = book_type
        book.sql.info = 'select * from Question where ({})'.format(' or '.join(info))
        book.sql.question = 'select * from Question where ({})'.format(' or '.join(question))
        book.sql.answer = 'select * from Answer where ({})'.format(' or '.join(answer))
        self.book_list[book_type] = [book]
        return

    def is_work_list_empty(self):
        for kind in Type.type_list:
            if self.work_list.get(kind):
                return False
        return True

    def is_book_list_empty(self):
        for kind in Type.type_list:
            if self.book_list.get(kind):
                return False
        return True
