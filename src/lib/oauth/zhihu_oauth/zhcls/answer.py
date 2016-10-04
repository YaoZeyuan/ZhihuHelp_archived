# coding=utf-8

from __future__ import unicode_literals

from .base import Base
from .generator import generator_of
from .other import other_obj
from .normal import normal_attr
from .streaming import streaming
from .utils import common_save
from .urls import (
    ANSWER_DETAIL_URL,
    ANSWER_COLLECTIONS_URL,
    ANSWER_COMMENTS_URL,
    ANSWER_VOTERS_URL,
)

__all__ = ["Answer"]


class Answer(Base):
    def __init__(self, aid, cache, session):
        super(Answer, self).__init__(aid, cache, session)

    def _build_url(self):
        return ANSWER_DETAIL_URL.format(self.id)

    # ----- simple info -----

    @property
    @other_obj('people')
    def author(self):
        return None

    @property
    @streaming()
    def can_comment(self):
        """
        大概表示允不允许当前用户评论吧。

        常见返回值：

        .. code-block:: python

            {
                'status': True,
                'reason': ''
            }
        """
        return None

    @property
    @normal_attr()
    def comment_count(self):
        return None

    @property
    @normal_attr()
    def comment_permission(self):
        """
        评论权限，现在已知有：

        ==========  ========================
        值(str)     说明
        ==========  ========================
        all         允许所有人评论
        followee    允许答主关注的人评论
        nobody      关闭评论
        ==========  ========================
        """
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
    def excerpt(self):
        return None

    @property
    @normal_attr()
    def id(self):
        return self._id

    @property
    @normal_attr()
    def is_copyable(self):
        return None

    @property
    @normal_attr()
    def is_mine(self):
        return None

    @property
    @other_obj()
    def question(self):
        return None

    @property
    @streaming(use_cache=False)
    def suggest_edit(self):
        """
        答案是否处于「被建议修改」状态，常见返回值为：

        ..  code-block:: python

            {'status': False, 'title': '', 'reason': '', 'tip': '', 'url': ''}

            {
                'status': True,
                'title': '为什么回答会被建议修改',
                'tip': '作者修改内容通过后，回答会重新显示。如果一周内未得到有效修改，回答会自动折叠',
                'reason': '回答被建议修改：\\n不宜公开讨论的政治内容',
                'url': 'zhihu://questions/24752645'
            }

        """
        return None

    @property
    @normal_attr()
    def thanks_count(self):
        return None

    @property
    @normal_attr()
    def updated_time(self):
        return None

    @property
    @normal_attr()
    def voteup_count(self):
        return None

    # ----- generators -----

    @property
    @generator_of(ANSWER_COLLECTIONS_URL)
    def collections(self):
        return None

    @property
    @generator_of(ANSWER_COMMENTS_URL)
    def comments(self):
        return None

    @property
    @generator_of(ANSWER_VOTERS_URL, 'people')
    def voters(self):
        return None

    # ----- other operate -----

    def save(self, path='.', filename=None, invalid_chars=None):
        """
        保存答案到当前文件夹。

        :param str|unicode path: 目录名，可选。不提供的话会保存到当前目录。
        :param str|unicode filename: 文件名，可选。
            不提供的话会使用答主名。注意不要带后缀名
        :param list[char] invalid_chars: 非法字符传列表。
            目录名和文件名都会使用这个列表过滤一遍。
            如果不提供则会使用内置的列表。
        :return: 无返回值

        .. note:: TIPS

            建议的使用方法：

            ..  code-block:: python

                # 对于保存问题的所有答案
                for answer in question.answers:
                    print(answer.author.name)
                    answer.save(question.title)

                # 对于保存收藏夹的所有答案
                for answer in collection.answers:
                    name = answer.question.title + ' - ' + answer.author.name
                    print(name)
                    answer.save(collection.title, name)

            因为这样会将答案保存在以问题标题（或者收藏夹名字）命名的文件夹里。

        ..  note:: TIPS

            对于一个问题下有多个匿名用户的情况，不要担心，会被自动命名为
            匿名用户 - 001.html，匿名用户 - 002.html……

        ..  todo:: 优化存在重复文件时的算法……

        """
        if self._cache is None:
            self._get_data()
        common_save(path, filename, self.content,
                    self.author.name, invalid_chars)
