# -*- coding: utf-8 -*-


class Author(object):
    def __init__(self, data):
        self.author_id = data['author_id']
        self.author_page_id = data['author_page_id']
        self.answer_count = data['answer_count']
        self.articles_count = data['articles_count']
        self.avatar_url = data['avatar_url']
        self.columns_count = data['columns_count']
        self.description = data['description']
        self.favorite_count = data['favorite_count']
        self.favorited_count = data['favorited_count']
        self.follower_count = data['follower_count']
        self.following_columns_count = data['following_columns_count']
        self.following_count = data['following_count']
        self.following_question_count = data['following_question_count']
        self.following_topic_count = data['following_topic_count']
        self.gender = data['gender']
        self.headline = data['headline']
        self.name = data['name']
        self.question_count = data['question_count']
        self.shared_count = data['shared_count']
        self.is_bind_sina = data['is_bind_sina']
        self.thanked_count = data['thanked_count']
        self.sina_weibo_name = data['sina_weibo_name']
        self.sina_weibo_url = data['sina_weibo_url']
        self.voteup_count = data['voteup_count']
        return