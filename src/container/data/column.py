# -*- coding: utf-8 -*-


class Column(object):
    def __init__(self, data):
        self.column_id = data['column_id']
        self.title = data['title']
        self.article_count = data['article_count']
        self.follower_count = data['follower_count']
        self.description = data['description']
        self.image_url = data['image_url']
        return
