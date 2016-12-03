# -*- coding: utf-8 -*-
from src.tools.db import DB


class Answer(object):
    def __init__(self, data):
        self.answer_id = data['answer_id']
        self.question_id = data['question_id']
        self.author_id = data['author_id']
        self.author_name = data['author_name']
        self.author_headline = data['author_headline']
        self.author_avatar_url = data['author_avatar_url']
        self.author_gender = data['author_gender']
        self.comment_count = data['comment_count']
        self.content = data['content']
        self.created_time = data['created_time']
        self.updated_time = data['updated_time']
        self.is_copyable = data['is_copyable']
        self.thanks_count = data['thanks_count']
        self.voteup_count = data['voteup_count']
        self.suggest_edit_status = data['suggest_edit_status']
        self.suggest_edit_reason = data['suggest_edit_reason']
        return


class Question(object):
    u"""
    问题容器
    """
    def __init__(self, question_id):
        self.question_id = question_id
        self.question_info = {}
        self.answer_list = []
        return

    def add_answer(self, answer_id):
        raw_answer = DB.query_row('Select * from Answer where answer_id={}'.format(answer_id))
        answer = Answer(raw_answer)
        self.answer_list.append(answer)
        return

    def append_answer(self, answer):
        """
        :type answer: Answer
        :return:
        """
        self.answer_list.append(answer)
        return

    def get_question_info(self, question_id):
        self.question_info = DB.query_row('Select * from Question where id = {}'.format(question_id))
        return

    def get_answer_list(self):
        return self.answer_list


class Article(object):
    u"""
    文章容器
    """
    def __init__(self, data):
        self.article_id = data['article_id']
        self.title = data['title']
        self.updated = data['updated']
        self.created = data['created']
        self.voteup_count = data['voteup_count']
        self.column_id = data['column_id']
        self.content = data['content']
        self.comment_count = data['comment_count']
        self.author_id = data['author_id']
        return


class Column(object):
    u"""
    专栏容器
    """

    def __init__(self, column_id):
        self.column_id = column_id
        self.article_list = []
        return

    def add_article(self, data={}):
        return


class TaskResult(object):
    u"""
    收集任务执行的结果
    """

    def __init__(self, task):
        u"""

        :type task src.container.task.Task
        """
        self.task_type = task.task_type
        self.task = task
        self.question_list = []
        self.article_list = []
        self.info_page = {}
        return

    def __extract_data(self):
        u"""
        根据task类型，从数据库中抽取数据
        :return:
        """

        return
