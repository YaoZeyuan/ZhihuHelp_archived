# coding=utf-8

from __future__ import unicode_literals

from .base import Base
from .generator import generator_of
from .other import other_obj
from .normal import normal_attr
from .urls import (
    COLLECTION_DETAIL_URL,
    COLLECTION_ANSWERS_URL,
    COLLECTION_COMMENTS_URL,
    COLLECTION_FOLLOWERS_URL,
)


class Collection(Base):
    def __init__(self, cid, cache, session):
        super(Collection, self).__init__(cid, cache, session)

    def _build_url(self):
        return COLLECTION_DETAIL_URL.format(self.id)

    # ---- simple info -----

    @property
    @normal_attr()
    def answer_count(self):
        return None

    @property
    @normal_attr()
    def created_time(self):
        return None

    @property
    @other_obj('people')
    def creator(self):
        return None

    @property
    @normal_attr()
    def comment_count(self):
        return None

    @property
    @normal_attr()
    def description(self):
        return None

    @property
    @normal_attr()
    def follower_count(self):
        return None

    @property
    @normal_attr()
    def id(self):
        return self._id

    @property
    @normal_attr()
    def is_public(self):
        return None

    @property
    @normal_attr()
    def title(self):
        return None

    @property
    @normal_attr()
    def updated_time(self):
        return None

    # ----- generators -----

    @property
    @generator_of(COLLECTION_ANSWERS_URL)
    def answers(self):
        return None

    @property
    @generator_of(COLLECTION_COMMENTS_URL)
    def comments(self):
        return None

    @property
    @generator_of(COLLECTION_FOLLOWERS_URL, 'people')
    def followers(self):
        """
        ..  warning:: 注意！

            知乎的这个 API 有问题，返回一些之后会将 is_end 设置为 True，
            导致无法获取到所有的关注者。

            并且此问题在知乎官方 Android APP 上也存在。你可以试着
            找个很多人关注的收藏夹，然后查看关注者，一直往下拉。
            大概加载 100 - 200（不固定，有时候一个都出不来）
            之后就没法往下刷了。

            起码在我这个地区是这样的。欢迎各路少侠反馈。

        """
        # TODO: collection.followers 这个 API 不稳定
        return None
