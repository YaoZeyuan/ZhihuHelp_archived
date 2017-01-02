# coding=utf-8

from __future__ import unicode_literals

from .base import Base
from .generator import generator_of
from .other import other_obj
from .normal import normal_attr
from .urls import (
    COLLECTION_DETAIL_URL,
    COLLECTION_CONTENTS_URL,
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
    def answers(self):
        """
        获取收藏夹里的所有答案。

        ..  warning::  无法被 shield

            因为内部是调用 :any:`Collection.contents` 的，
            所以此生成器无法被 :any:`shield` 保护。

            但是内部其实是用 shield 保护过 contents 的获取的，
            如果这个生成器异常了那还是处理下吧。

        ..  seealso:: :any:`Collection.articles`, :any:`Collection.contents`
        """
        from .answer import Answer
        from ..helpers import shield

        contents = self.contents
        if contents is None:
            return

        # noinspection PyTypeChecker
        for x in shield(contents):
            if isinstance(x, Answer):
                yield x

    @property
    def articles(self):
        """
        获取收藏夹里的所有文章。

        ..  warning::  无法被 shield

            因为内部是调用 :any:`Collection.contents` 的，
            所以此生成器无法被 :any:`shield` 保护。

            但是内部其实是用 shield 保护过 contents 的获取的，
            如果这个生成器异常了那还是处理下吧。

        ..  seealso:: :any:`Collection.answers`, :any:`Collection.contents`
        """
        from .article import Article
        from ..helpers import shield

        contents = self.contents
        if contents is None:
            return

        # noinspection PyTypeChecker
        for x in shield(contents):
            if isinstance(x, Article):
                yield x

    @property
    @generator_of(COLLECTION_COMMENTS_URL)
    def comments(self):
        return None

    @property
    @generator_of(COLLECTION_CONTENTS_URL, 'CollectionContent')
    def contents(self):
        """
        新版知乎专栏支持收藏文章了，这个生成器生成的对象可能是 :any:`Answer` 也可能是
        :any:`Article`，使用时要用 ``isinstance`` 判断类型后再获取对应对象的属性。

        ..  code-block:: python

            from zhihu_oauth import ZhihuClient, Answer, Article

            collection = client.collection(37770691)

            for content in collection.contents:
                if isinstance(content, Answer):
                    answer = content
                    print(answer.question.title)
                elif isinstance(content, Article):
                    article = content
                    print(article.title)

        如果你只需要答案或者只需要文章类型的数据，可以使用 :any:`Collection.answers`
        或者 :any:`Collection.articles` 进行获取。

        不过需要注意的是，这两个属性内部其实会调用 :any:`Collection.contents`，
        然后只返回相应类型的对象。所以其实也是遍历了所有内容的，
        效率与使用本函数然后自己判断类型一样。

        ..  seealso:: :any:`Collection.answers`, :any:`Collection.articles`
        """
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
