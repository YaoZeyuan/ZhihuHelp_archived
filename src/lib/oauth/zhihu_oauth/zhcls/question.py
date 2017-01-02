# coding=utf-8

from __future__ import unicode_literals

from .base import Base
from .generator import generator_of
from .normal import normal_attr
from .streaming import streaming
from zhihu_oauth.zhcls.urls import (
    QUESTION_DETAIL_URL,
    QUESTION_ANSWERS_URL,
    QUESTION_COMMENTS_URL,
    QUESTION_FOLLOWERS_URL,
    QUESTION_TOPICS_URL,
)

__all__ = ['Question']


class Question(Base):
    def __init__(self, qid, cache, session):
        super(Question, self).__init__(qid, cache, session)

    def _build_url(self):
        return QUESTION_DETAIL_URL.format(self._id)

    # ----- simple info -----

    @property
    @normal_attr()
    def allow_delete(self):
        return None

    @property
    @normal_attr()
    def answer_count(self):
        return None

    @property
    @normal_attr()
    def comment_count(self):
        return None

    @property
    @normal_attr("created")
    def created_time(self):
        return None

    @property
    @normal_attr('except')
    def excerpt(self):
        """
        知乎返回的 json 里这一项叫做 except.... 也是醉了
        """
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
    def detail(self):
        return None

    @property
    @streaming()
    def redirection(self):
        """
        常见返回值：

        ..  code-block:: python

            {
                'to':
                {
                    'url': 'https://api.zhihu.com/questions/19570036',
                    'id': 19570036,
                    'type': 'question',
                    'title': '什么是「问题重定向」？如何正确使用该功能解决重复问题？'
                },
                'from':
                [
                    {
                        'url': 'https://api.zhihu.com/questions/19772082',
                        'id': 19772082,
                        'type': 'question',
                        'title': '知乎上有重复的问题吗？'
                    },
                    {
                        'url': 'https://api.zhihu.com/questions/20830682',
                        'id': 20830682,
                        'type': 'question',
                        'title': '各位知友以为同一问题重复出现，知乎应如何应对？'
                    }
                ]
            }

        在使用 from 属性时遇到语法错误？请看 :ref:`说明 <tips-for-conflict-with-keyword>`

        """
        return None

    @property
    @streaming()
    def status(self):
        return None

    @property
    @streaming(use_cache=False)
    def suggest_edit(self):
        """
        常见返回值：

        ..  code-block:: python

            {'status': False', reason': ''}

            {'status': True, 'reason': '问题表意不明'}
        """
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
    @generator_of(QUESTION_ANSWERS_URL)
    def answers(self):
        return None

    @property
    @generator_of(QUESTION_COMMENTS_URL)
    def comments(self):
        return None

    @property
    @generator_of(QUESTION_FOLLOWERS_URL, 'people')
    def followers(self):
        return None

    @property
    @generator_of(QUESTION_TOPICS_URL)
    def topics(self):
        return None
