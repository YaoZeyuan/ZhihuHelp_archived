# -*- coding: utf-8 -*-
from src.tools.type import Type


class Task(object):
    def __init__(self, task_type):
        self.task_type = task_type
        return

    def get_task_type(self):
        return self.task_type


class AuthorTask(Task):
    def __init__(self, author_page_id):
        Task.__init__(self, Type.author)
        self.author_page_id = author_page_id
        return


class TopicTask(Task):
    def __init__(self, topic_id):
        Task.__init__(self, Type.topic)
        self.topic_id = int(topic_id)
        return


class CollectionTask(Task):
    def __init__(self, collection_id):
        Task.__init__(self, Type.collection)
        self.collection_id = int(collection_id)
        return


class QuestionTask(Task):
    def __init__(self, question_id):
        Task.__init__(self, Type.question)
        self.question_id = int(question_id)
        return


class AnswerTask(Task):
    def __init__(self, question_id, answer_id):
        Task.__init__(self, Type.answer)
        self.question_id = int(question_id)
        self.answer_id = int(answer_id)
        return


class ColumnTask(Task):
    def __init__(self, column_id):
        Task.__init__(self, Type.column)
        self.column_id = int(column_id)
        return


class ArticleTask(Task):
    def __init__(self, column_id, article_id):
        Task.__init__(self, Type.article)
        self.column_id = int(column_id)
        self.article_id = int(article_id)
        return
