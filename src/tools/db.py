# -*- coding: utf-8 -*-
from debug import Debug
from src.tools.type import Type


class DB(object):
    u'''
    用于存放常用的sql代码
    '''
    cursor = None
    conn = None

    @staticmethod
    def set_conn(conn):
        DB.conn = conn
        DB.conn.text_factory = str
        DB.cursor = conn.cursor()
        return

    @staticmethod
    def execute(sql):
        return DB.cursor.execute(sql)

    @staticmethod
    def commit():
        return DB.cursor.commit()

    @staticmethod
    def save(data={}, table_name=''):
        sql = "replace into {table_name} ({columns}) values ({items})".format(table_name=table_name,
                                                                              columns=','.join(data.keys()),
                                                                              items=(',?' * len(data.keys()))[1:])
        Debug.logger.debug(sql)
        DB.cursor.execute(sql, tuple(data.values()))
        return

    @staticmethod
    def commit():
        DB.conn.commit()
        return

    @staticmethod
    def get_result_list(sql):
        Debug.logger.debug(sql)
        result = DB.cursor.execute(sql).fetchall()
        return result

    @staticmethod
    def get_result(sql):
        result = DB.cursor.execute(sql).fetchone()
        return result

    @staticmethod
    def wrap(kind, result=()):
        u"""
        将s筛选出的列表按SQL名组装为字典对象
        """
        template = {Type.answer: (
            'author_id', 'author_sign', 'author_logo', 'author_name', 'agree', 'content', 'question_id', 'answer_id',
            'commit_date', 'edit_date', 'comment', 'no_record_flag', 'href',),
            Type.question: ('question_id', 'comment', 'views', 'answers', 'followers', 'title', 'description',),
            Type.article: ('author_id', 'author_hash', 'author_sign', 'author_name', 'author_logo', 'column_id', 'name',
                           'article_id', 'href', 'title', 'title_image', 'content', 'comment', 'agree',
                           'publish_date',),

            Type.author_info: (
                'logo', 'author_id', 'hash', 'sign', 'description', 'name', 'asks', 'answers', 'posts', 'collections',
                'logs', 'agree', 'thanks', 'collected', 'shared', 'followee', 'follower', 'followed_column',
                'followed_topic', 'viewed', 'gender', 'weibo',),
            Type.collection_info: ('collection_id', 'title', 'description', 'follower', 'comment',),
            Type.topic_info: ('title', 'logo', 'description', 'topic_id', 'follower',), Type.column_info: (
                'creator_id', 'creator_hash', 'creator_sign', 'creator_name', 'creator_logo', 'column_id', 'name',
                'logo', 'description', 'article', 'follower',),

            Type.collection_index: ('collection_id', 'href',), Type.topic_index: ('topic_id', 'href',), }
        return {k: v for (k, v) in zip(template[kind], result)}
