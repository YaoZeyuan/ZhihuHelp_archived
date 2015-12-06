# -*- coding: utf-8 -*-
from src.container.book import Book
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
        self.book = Book()
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
            self.merge_answer_book_list()
        if Type.question in self.book_list:
            self.merge_question_book_list()
        if Type.article in self.book_list:
            self.merge_article_book_list()
        return self

    def merge_article_book_list(self):
        book_list = self.book_list[Type.article]
        book = Book()
        answer = []
        for item in book_list:
            answer.append(item.sql.answer)
        book.kind = Type.article
        book.sql.answer = 'select * from Article where ({})'.format(' or '.join(answer))
        self.book_list[Type.article] = [book]
        return

    def merge_answer_book_list(self):
        book_list = self.book_list[Type.answer]
        book = Book()
        question = []
        answer = []
        for item in book_list:
            question.append(item.sql.question)
            answer.append(item.sql.answer)
        book.kind = Type.answer
        book.sql.question = 'select * from Question where ({})'.format(' or '.join(question))
        book.sql.answer = 'select * from Answer where ({})'.format(' or '.join(answer))
        self.book_list[Type.answer] = [book]
        return

    def merge_question_book_list(self):
        book_list = self.book_list[Type.question]
        book = Book()
        question = []
        answer = []
        for item in book_list:
            question.append(item.sql.question)
            answer.append(item.sql.answer)
        book.kind = Type.question
        book.sql.question = 'select * from Question where ({})'.format(' or '.join(question))
        book.sql.answer = 'select * from Answer where ({})'.format(' or '.join(answer))
        self.book_list[Type.question] = [book]
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
