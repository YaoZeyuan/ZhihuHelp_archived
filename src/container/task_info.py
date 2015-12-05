# -*- coding: utf-8 -*-
from baseClass import TypeClass


class Spider(object):
    def __init__(self):
        self.href = ''
        return


class CommandBook(object):
    def __init__(self):
        self.kind = ''
        self.info = ''
        self.question = ''
        self.answer = ''
        return


class TaskInfo(object):
    u"""
    任务信息应当以对象属性的方式进行存储，用字典存的话记不住
    """

    def __init__(self):
        self.kind = ''
        self.spider = Spider()
        self.book = CommandBook()
        return


class Task():
    def __init__(self):
        self.work_list = {}
        self.book_list = {}
        return

    def add_task(self, task_info=TaskInfo()):
        if not task_info.kind in self.work_list:
            self.work_list[task_info.kind] = []
        self.work_list[task_info.kind].append(task_info.spider.href)
        if not task_info.kind in self.book_list:
            self.book_list[task_info.kind] = []
        self.book_list[task_info.kind].append(task_info.book)
        return

    def get_task(self):
        if TypeClass.answer in self.book_list:
            self.merge_answer_book_list()
        if TypeClass.question in self.book_list:
            self.merge_question_book_list()
        if TypeClass.article in self.book_list:
            self.merge_article_book_list()
        return self

    def merge_article_book_list(self):
        book_list = self.book_list['article']
        book = CommandBook()
        answer = []
        for item in book_list:
            answer.append(item.answer)
        book.kind = 'article'
        book.answer = 'select * from Article where ({})'.format(' or '.join(answer))
        self.book_list['article'] = [book]
        return

    def merge_answer_book_list(self):
        book_list = self.book_list[TypeClass.answer]
        book = CommandBook()
        question = []
        answer = []
        for item in book_list:
            question.append(item.question)
            answer.append(item.answer)
        book.kind = TypeClass.answer
        book.question = 'select * from Question where ({})'.format(' or '.join(question))
        book.answer = 'select * from Answer where ({})'.format(' or '.join(answer))
        self.book_list[TypeClass.answer] = [book]
        return

    def merge_question_book_list(self):
        book_list = self.book_list[TypeClass.question]
        book = CommandBook()
        question = []
        answer = []
        for item in book_list:
            question.append(item.question)
            answer.append(item.answer)
        book.kind = TypeClass.question
        book.question = 'select * from Question where ({})'.format(' or '.join(question))
        book.answer = 'select * from Answer where ({})'.format(' or '.join(answer))
        self.book_list[TypeClass.question] = [book]
        return
