# coding=utf-8

from __future__ import unicode_literals

from .base import Base
from .generator import generator_of
from .normal import normal_attr
from zhihu_oauth.zhcls.urls import (
    COMMENT_CONVERSION_URL,
    COMMENT_REPLIES_URL,
)

__all__ = ['Comment']


class Comment(Base):
    def __init__(self, cid, cache, session):
        super(Comment, self).__init__(cid, cache, session)

    def _get_data(self):
        self._data = None

    def _build_url(self):
        return ''

    # ----- simple info -----

    @property
    @normal_attr()
    def allow_delete(self):
        return None

    @property
    @normal_attr()
    def allow_like(self):
        return None

    @property
    @normal_attr()
    def allow_reply(self):
        return None

    @property
    @normal_attr()
    def ancestor(self):
        """
        不知道是啥，貌似永远都是 False。
        """
        return None

    @property
    def author(self):
        from .people import People
        if self._cache and 'author' in self._cache:
            cache = self._cache['author']
        else:
            self._get_data()
            if self._data and 'author' in self._data:
                cache = self._data['author']
            else:
                cache = None
        if cache:
            if 'member' in cache:
                cache = cache['member']
            return People(cache['id'], cache, self._session)
        else:
            return None

    @property
    @normal_attr()
    def content(self):
        return None

    @property
    @normal_attr()
    def created_time(self):
        return None

    @property
    @normal_attr()
    def id(self):
        return None

    @property
    @normal_attr()
    def is_author(self):
        """
        是否是 答案/文章/etc 的作者的评论。
        """
        return None

    @property
    @normal_attr()
    def is_delete(self):
        """
        是否被删除？话说被删除了还能获取到？我没测试……
        """
        return None

    @property
    @normal_attr()
    def is_parent_author(self):
        """
        也没搞懂这个属性，貌似永远和 :meth:`is_author` 保持一致。
        """
        return None

    @property
    def reply_to(self):
        """
        获取这条评论的父评论的作者，如果并没有回复谁则返回 None

        :rtype: People
        """
        from .people import People
        if self._cache and 'reply_to_author' in self._cache:
            cache = self._cache['reply_to_author']
        else:
            self._get_data()
            if self._data and 'reply_to_author' in self._data:
                cache = self._data['reply_to_author']
            else:
                cache = None
        if cache:
            if 'member' in cache:
                cache = cache['member']
            return People(cache['id'], cache, self._session)
        else:
            return None

    @property
    @normal_attr()
    def resource_type(self):
        """
        是对什么东西的评论。

        ========  ==========
        值(str)   说明
        ========  ==========
        answer    答案
        article   文章
        question  问题
        favlist   收藏夹
        ========  ==========
        """
        return None

    @property
    @normal_attr()
    def vote_count(self):
        return None

    @property
    @normal_attr()
    def voting(self):
        """
        是否对这条评论点了赞。
        """
        return None

    # ----- generators -----

    @property
    @generator_of(COMMENT_REPLIES_URL, 'comment')
    def replies(self):
        """
        应该是用于实现「对话列表」的。

        :return: 回复本条评论的所有评论的列表（生成器）。
        :rtype: collections.Iterable[Comment]
        """
        return None

    @property
    @generator_of(COMMENT_CONVERSION_URL, 'comment')
    def conversation(self):
        """
        应该是用于实现「查看对话」的。

        有的评论有这个属性，有个没有，我也没搞清楚规律。

        :return: 包含此条评论的对话，体现为评论列表（生成器）
        :rtype: collections.Iterable[Comment]
        """
        return None
