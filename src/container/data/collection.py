# -*- coding: utf-8 -*-


class Collection(object):
    def __init__(self, data):
        self.collection_id = data['collection_id']
        self.answer_count = data['answer_count']
        self.comment_count = data['comment_count']
        self.created_time = data['created_time']
        self.follower_count = data['follower_count']
        self.description = data['description']
        self.title = data['title']
        self.updated_time = data['updated_time']
        self.creator_id = data['creator_id']
        self.creator_name = data['creator_name']
        self.creator_headline = data['creator_headline']
        self.creator_avatar_url = data['creator_avatar_url']
        self.collected_answer_id_list = data['collected_answer_id_list']
        return