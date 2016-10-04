# coding=utf-8

from __future__ import unicode_literals

from .base import Base
from .generator import generator_of
from .other import other_obj
from .normal import normal_attr
from .urls import (
    COLUMN_DETAIL_URL,
    COLUMN_ARTICLES_URL,
    COLUMN_FOLLOWERS_URL,
)

__all__ = ['Column']


class Column(Base):
    def __init__(self, cid, cache, session):
        super(Column, self).__init__(cid, cache, session)

    def _build_url(self):
        return COLUMN_DETAIL_URL.format(self.id)

    # ---- simple info -----

    @property
    @normal_attr('articles_count')
    def article_count(self):
        return None

    @property
    def articles_count(self):
        return self.article_count

    @property
    @other_obj('people')
    def author(self):
        return None

    @property
    @normal_attr()
    def comment_permission(self):
        return None

    @property
    @normal_attr()
    def description(self):
        return None

    @property
    @normal_attr('followers')
    def follower_count(self):
        return None

    @property
    @normal_attr()
    def id(self):
        return self._id

    @property
    @normal_attr()
    def image_url(self):
        return None

    @property
    @normal_attr()
    def title(self):
        return None

    @property
    @normal_attr('updated')
    def updated_time(self):
        return None

    @property
    def updated(self):
        return self.updated_time

    # ----- generators -----

    @property
    @generator_of(COLUMN_ARTICLES_URL)
    def articles(self):
        return None

    @property
    @generator_of(COLUMN_FOLLOWERS_URL, 'people')
    def followers(self):
        return None
