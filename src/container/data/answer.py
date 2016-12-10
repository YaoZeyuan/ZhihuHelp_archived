# -*- coding: utf-8 -*-


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