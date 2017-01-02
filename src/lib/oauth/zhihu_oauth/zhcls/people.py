# coding=utf-8

from __future__ import unicode_literals

from .base import Base
from .generator import generator_of
from .normal import normal_attr
from .streaming import streaming
from .urls import (
    PEOPLE_ACTIVITIES_URL,
    PEOPLE_ANSWERS_URL,
    PEOPLE_ARTICLES_URL,
    PEOPLE_COLLECTIONS_URL,
    PEOPLE_COLUMNS_URL,
    PEOPLE_DETAIL_URL,
    PEOPLE_FOLLOWERS_URL,
    PEOPLE_FOLLOWING_COLUMNS_URL,
    PEOPLE_FOLLOWING_QUESTIONS_URL,
    PEOPLE_FOLLOWING_TOPICS_URL,
    PEOPLE_FOLLOWINGS_URL,
    PEOPLE_LIKED_LIVES_URL,
    PEOPLE_LIVES_URL,
    PEOPLE_QUESTIONS_URL,
)
from ..exception import GetDataErrorException

__all__ = ['ANONYMOUS', 'People']


class _Anonymous(object):
    def __init__(self):
        self.id = 0
        self.name = '匿名用户'

    def __getattr__(self, _):
        # 匿名用户除了姓名和 ID 以外所有属性均为 None
        return None


ANONYMOUS = _Anonymous()
"""
.. role:: py_code(code)
   :language: python

统一的匿名用户对象，可以使用 :py_code:`if people is ANONYMOUS:` 判断是否是匿名用户
"""


class People(Base):
    def __new__(cls, pid, cache, session):
        if pid == '0':
            return ANONYMOUS
        else:
            return super(People, cls).__new__(cls)

    def __init__(self, pid, cache, session):
        self._over_e = None
        super(People, self).__init__(pid, cache, session)

    def _build_url(self):
        return PEOPLE_DETAIL_URL.format(self.id)

    @property
    def over(self):
        """
        尝试获取用户信息，如果出错返回 True，没出错返回 False。

        一般来说出错的情况只有「被知乎反屏蔽系统限制」……所以这函数起名叫 over =。=

        调用结果如果是 True，则可使用 :any:`over_reason` 函数获取原因。

        .. note:: 例子

            ..  code-block:: python

                for follower in me.followers:
                    if follower.over:
                        print(follower.over_reason)
                        continue

                    print(follower.name)
                    # ... process follower data

        ..  note:: 也可以不用此函数，用 ``try...catch`` 来处理也行

            ..  code-block:: python

                from zhihu_oauth import ZhihuClient, GetDataErrorException

                for follower in me.followers:
                    try:
                        # get and process user data
                    except GetDataErrorException as e:
                        print("Get data error", e.reason)

        :return: 是否被限制
        :rtype: bool
        """
        if self._over_e is not None:
            return True
        try:
            self._get_data()
            return False
        except GetDataErrorException as e:
            self._over_e = e
            return True

    @property
    def over_reason(self):
        """
        获取无法得到用户信息的原因。

        ..  warning::

            此方法只能在 :any:`over` 方法调用结果为 True 之后才能调用。

        :rtype: str
        """
        if self._over_e is None:
            return None
        return self._over_e.reason if self._over_e.reason else str(self._over_e)

    # ---------- simple info ---------

    @property
    @normal_attr()
    def answer_count(self):
        return None

    @property
    @normal_attr()
    def articles_count(self):
        return None

    @property
    @normal_attr()
    def avatar_url(self):
        return None

    @property
    @streaming()
    def business(self):
        """
        用户所在行业。

        常见返回值：

        ..  code-block:: python

            {
                'introduction': '',
                'id': '19619368',
                'url': 'https://api.zhihu.com/topics/19619368',
                'type': 'topic',
                'avatar_url': 'http://pic1.zhimg.com/e82bab09c_s.jpg',
                'name': '计算机软件',
                'excerpt': '',
            }

        使用属性时必须先判断是否有效，如

        ..  code-block:: python

            if 'people.business:
                data = people.business.name

        """
        return {}

    @property
    @normal_attr('favorited_count')
    def collected_count(self):
        return None

    @property
    @normal_attr('favorite_count')
    def collection_count(self):
        return None

    @property
    @normal_attr('columns_count')
    def column_count(self):
        return None

    @property
    def columns_count(self):
        return self.column_count

    @property
    @normal_attr()
    def created_at(self):
        return None

    @property
    @normal_attr()
    def description(self):
        return None

    @property
    @normal_attr()
    def draft_count(self):
        return None

    @property
    @streaming()
    def educations(self):
        """
        教育信息。

        常见返回值：

        ..  code-block:: python

            [
                {
                    'major': {
                        'introduction': '计算机专业。<br>大众认为会是唯一会“修电脑”的专业。',
                        'id': '19639658',
                        'url': 'https://api.zhihu.com/topics/19639658',
                        'type': 'topic',
                        'avatar_url': 'http://pic2.zhimg.com/7e2fe4615_s.jpg',
                        'name': '计算机科学与技术',
                        'excerpt': '计算机专业。大众认为会是唯一会“修电脑”的专业。',
                    },
                    'school': {
                        'introduction': '',
                        'id': '1234567',
                        'url': 'https://api.zhihu.com/topics/1234567',
                        'type': 'topic',
                        'avatar_url': 'http://pic4.zhimg.com/8e6y3xd47_s.jpg',
                        'name': 'XX 大学',
                        'excerpt': '',
                    },
                },
            ]

        使用属性时必须先判断存不存在，如:

        ..  code-block:: python

            for education in people.educations:
                if 'school' in education:
                    data += education.school.name
                if 'major' in education:
                    data += education.major.name'
        """
        return []

    @property
    @streaming()
    def employments(self):
        """
        职业信息。

        常见返回值：

        ..  code-block:: python

            [
                {
                    'job': {
                        'introduction': '',
                        'url': 'https://api.zhihu.com/topics/19551336',
                        'avatar_url': 'http://pic3.zhimg.com/4eac47b76_s.jpg',
                        'excerpt': '',
                        'type': 'topic',
                        'name': '测试',
                        'id': '19551336',
                    },
                    'company': {
                        'excerpt': '',
                        'url': '',
                        'avatar_url': 'http://pic1.zhimg.com/e82bab09c_s.jpg',
                        'introduction': '',
                        'type': 'topic',
                        'name': 'Gayhub',
                        'experience ': '',
                        'id': '',
                    },
                },
            ],

        使用属性时必须先判断存不存在，如:

        ..  code-block:: python

            for employment in people.employments:
                if 'company' in employment:
                    data += employment.company.name
                if 'job' in employment:
                    data += employment.job.name'
        """
        return []

    @property
    @normal_attr()
    def email(self):
        return None

    @property
    def favorite_count(self):
        return self.collection_count

    @property
    def favorited_count(self):
        return self.collected_count

    @property
    @normal_attr()
    def follower_count(self):
        return None

    @property
    @normal_attr('following_columns_count')
    def following_column_count(self):
        return None

    @property
    @normal_attr()
    def following_count(self):
        return None

    @property
    @normal_attr()
    def following_question_count(self):
        return None

    @property
    @normal_attr()
    def following_topic_count(self):
        return None

    @property
    @normal_attr()
    def friendly_score(self):
        return None

    @property
    @normal_attr()
    def gender(self):
        """
        性别。

        =======  ==========
        值(int)  说明
        =======  ==========
        0        女
        1        男
        -1       未填
        =======  ==========

        我该如何吐槽……
        """
        return None

    @property
    @normal_attr()
    def has_daily_recommend_permission(self):
        return None

    @property
    @normal_attr()
    def headline(self):
        """
        就是那个显示在名字后面的，和签名类似的东西。
        """
        return None

    @property
    @normal_attr()
    def is_active(self):
        return None

    @property
    @normal_attr()
    def id(self):
        return self._id

    @property
    @normal_attr()
    def is_baned(self):
        return None

    @property
    @normal_attr()
    def is_bind_sina(self):
        return None

    @property
    @normal_attr()
    def is_locked(self):
        return None

    @property
    @normal_attr()
    def is_moments_user(self):
        """
        不知道是啥。
        """
        return None

    @property
    @streaming()
    def locations(self):
        """
        常见返回值。

        ..  code-block:: python

            [
                {
                    'introduction': '天津，简称津，地处华北平原，balabala,
                    'url': 'https://api.zhihu.com/topics/19577238',
                    'avatar_url': 'http://pic4.zhimg.com/acad405e7_s.jpg',
                    'excerpt': '天津，简称津，地处华北平原 balabalabala',
                    'type': 'topic',
                    'name': '天津',
                    'id': '19577238',
                },
            ],

        使用属性时基本不用判断存不存在，如:

        ..  code-block:: python

            for location in people.locations:
                data += location.name
        """
        return []

    @property
    @normal_attr()
    def name(self):
        return None

    @property
    @normal_attr()
    def question_count(self):
        return None

    @property
    @normal_attr()
    def shared_count(self):
        return None

    @property
    @normal_attr()
    def sina_weibo_name(self):
        return None

    @property
    @normal_attr()
    def sina_weibo_url(self):
        return None

    @property
    @normal_attr()
    def thanked_count(self):
        return None

    @property
    @normal_attr()
    def uid(self):
        """
        没什么用的东西。
        """
        return None

    @property
    @normal_attr()
    def voteup_count(self):
        return None

    # ---------- generators ---------

    @property
    @generator_of(PEOPLE_ACTIVITIES_URL, 'activity')
    def activities(self):
        return None

    @property
    @generator_of(PEOPLE_ANSWERS_URL)
    def answers(self):
        return None

    @property
    @generator_of(PEOPLE_ARTICLES_URL)
    def articles(self):
        return None

    @property
    @generator_of(PEOPLE_COLLECTIONS_URL)
    def collections(self):
        return None

    @property
    @generator_of(PEOPLE_COLUMNS_URL)
    def columns(self):
        return None

    @property
    @generator_of(PEOPLE_FOLLOWERS_URL, 'people')
    def followers(self):
        """
        貌似知乎 API 有个限制，只允许获取前 5020 个粉丝，这好烦阿……
        """
        return None

    @property
    @generator_of(PEOPLE_FOLLOWING_COLUMNS_URL, 'column')
    def following_columns(self):
        return None

    @property
    @generator_of(PEOPLE_FOLLOWING_QUESTIONS_URL, 'question')
    def following_questions(self):
        return None

    @property
    @generator_of(PEOPLE_FOLLOWING_TOPICS_URL, 'topic')
    def following_topics(self):
        return None

    @property
    @generator_of(PEOPLE_FOLLOWINGS_URL, 'people')
    def followings(self):
        return None

    @property
    @generator_of(PEOPLE_LIVES_URL)
    def lives(self):
        """
        举办和参加的 Live
        """
        return None

    @property
    @generator_of(PEOPLE_LIKED_LIVES_URL, 'live')
    def liked_lives(self):
        """
        喜爱的 Live

        ..  warning:: 此接口未测试，不保证可用性。
        """
        return None

    @property
    @generator_of(PEOPLE_QUESTIONS_URL)
    def questions(self):
        return None
