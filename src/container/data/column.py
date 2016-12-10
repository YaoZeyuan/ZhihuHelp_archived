# -*- coding: utf-8 -*-


class Column(object):
    def __init__(self, data):
        self.column_id = data['column_id']
        self.name = data['name']
        self.postsCount = data['postsCount']
        self.followersCount = data['followersCount']
        self.description = data['description']
        self.reason = data['reason']
        self.intro = data['intro']
        self.creator_id = data['creator_id']
        return