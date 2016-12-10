# -*- coding: utf-8 -*-

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
