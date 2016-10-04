# coding=utf-8

from __future__ import unicode_literals

from .base import Base
from .generator import generator_of
from .other import other_obj
from .normal import normal_attr
from .streaming import streaming
from .utils import common_save
from .urls import (
    ARTICLE_DETAIL_URL,
    ARTICLE_COMMENTS_URL,
)

__all__ = ['Article']


class Article(Base):
    def __init__(self, aid, cache, session):
        super(Article, self).__init__(aid, cache, session)

    def _build_url(self):
        return ARTICLE_DETAIL_URL.format(self.id)

    # ----- simple info -----

    @property
    @other_obj('people')
    def author(self):
        return None

    @property
    @streaming()
    def can_comment(self):
        """
        ..  seealso:: :any:`Answer.can_comment`
        """
        return None

    @property
    @other_obj()
    def column(self):
        """
        文章所属专栏。

        .. warning:: 当文章不属于任何专栏时值为 None，使用其属性前应先做检查。
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
        ..  seealso:: :any:`Answer.comment_permission`
        """
        return None

    @property
    @normal_attr()
    def content(self):
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
    def image_url(self):
        return None

    @property
    @streaming(use_cache=False)
    def suggest_edit(self):
        """
        ..  seealso:: :any:`Answer.suggest_edit`
        """
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
    @normal_attr()
    def voteup_count(self):
        return None

    # ----- generators -----

    @property
    @generator_of(ARTICLE_COMMENTS_URL)
    def comments(self):
        return None

    # TODO: article.voters, API 接口未知

    # ----- other operate -----

    def save(self, path='.', filename=None, invalid_chars=None):
        """
        除了默认文件名是文章标题外，和 :any:`Answer.save` 完全一致。

        ..  seealso:: :any:`Answer.save`

        ..  note:: TIPS

            建议的使用方法：

            ..  code-block:: python

                for article in column.articles:
                    print(article.title)
                    article.save(column.title)

        """
        if self._cache is None:
            self._get_data()
        common_save(path, filename, self.content, self.title, invalid_chars)
