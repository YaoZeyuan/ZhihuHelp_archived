# coding=utf-8

from __future__ import unicode_literals

from .base import Base
from .generator import generator_of
from .normal import normal_attr
from zhihu_oauth.zhcls.urls import (
    TOPIC_DETAIL_URL,
    TOPIC_BEST_ANSWERS_URL,
    TOPIC_BEST_ANSWERERS_URL,
    TOPIC_CHILDREN_URL,
    TOPIC_FOLLOWERS_URL,
    TOPIC_PARENTS_URL,
    TOPIC_UNANSWERED_QUESTION,
)

__all__ = ['Topic']


class Topic(Base):
    def __init__(self, tid, cache, session):
        super(Topic, self).__init__(tid, cache, session)

    def _build_url(self):
        return TOPIC_DETAIL_URL.format(self.id)

    # ---- simple info -----

    @property
    @normal_attr()
    def avatar_url(self):
        return None

    @property
    @normal_attr('best_answers_count')
    def best_answer_count(self):
        return None

    @property
    def best_answers_count(self):
        return self.best_answer_count

    @property
    @normal_attr()
    def id(self):
        return self._id

    @property
    @normal_attr()
    def introduction(self):
        return None

    @property
    @normal_attr()
    def excerpt(self):
        return None

    @property
    def father_count(self):
        return self.parent_count

    @property
    @normal_attr('followers_count')
    def follower_count(self):
        return None

    @property
    def followers_count(self):
        return self.follower_count

    @property
    @normal_attr()
    def name(self):
        return None

    @property
    @normal_attr('father_count')
    def parent_count(self):
        return None

    @property
    @normal_attr('questions_count')
    def question_count(self):
        return None

    @property
    def questions_count(self):
        return self.question_count

    @property
    @normal_attr()
    def unanswered_count(self):
        return None

    # ----- generators -----

    @property
    @generator_of(TOPIC_BEST_ANSWERS_URL, 'answer')
    def best_answers(self):
        """
        精华回答
        """
        return None

    @property
    @generator_of(TOPIC_BEST_ANSWERERS_URL, 'people')
    def best_answerers(self):
        """
        好像叫，最佳回答者吧……

        best_answerers……知乎真会起名字……
        """
        return None

    @property
    @generator_of(TOPIC_CHILDREN_URL, 'topic')
    def children(self):
        """
        子话题
        """
        return None

    @property
    @generator_of(TOPIC_FOLLOWERS_URL, 'people')
    def followers(self):
        return None

    @property
    @generator_of(TOPIC_PARENTS_URL, 'topic')
    def parents(self):
        """
        父话题
        """
        return None

    @property
    @generator_of(TOPIC_UNANSWERED_QUESTION, 'question')
    def unanswered_questions(self):
        return None
