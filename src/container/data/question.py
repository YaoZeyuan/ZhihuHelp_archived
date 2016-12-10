# -*- coding: utf-8 -*-


class Question(object):
    def __init__(self, data):
        self.question_id = data['question_id']
        self.answer_count = data['answer_count']
        self.comment_count = data['comment_count']
        self.follower_count = data['follower_count']
        self.title = data['title']
        self.detail = data['detail']
        self.updated_time = data['updated_time']
        return