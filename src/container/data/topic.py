# -*- coding: utf-8 -*-


class Topic(object):
    def __init__(self, data):
        self.topic_id = data['topic_id']
        self.avatar_url = data['avatar_url']
        self.best_answerers_count = data['best_answerers_count']
        self.best_answers_count = data['best_answers_count']
        self.excerpt = data['excerpt']
        self.followers_count = data['followers_count']
        self.introduction = data['introduction']
        self.name = data['name']
        self.questions_count = data['questions_count']
        self.unanswered_count = data['unanswered_count']
        self.best_answer_id_list = data['best_answer_id_list']
        return