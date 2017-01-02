# coding=utf-8

from __future__ import unicode_literals

from .people import People
from .urls import (
    ANSWER_CANCEL_THANKS_URL,
    ANSWER_CANCEL_UNHELPFUL_URL,
    ANSWER_COLLECT_URL,
    ANSWER_DETAIL_URL,
    ANSWER_THANKS_URL,
    ANSWER_UNHELPFUL_URL,
    ANSWER_VOTERS_URL,
    ARTICLE_DETAIL_URL,
    ARTICLE_VOTE_URL,
    BLOCK_PEOPLE_URL,
    CANCEL_BLOCK_PEOPLE_URL,
    COLLECTION_CANCEL_FOLLOW_URL,
    COLLECTION_DETAIL_URL,
    COLLECTION_FOLLOWERS_URL,
    COLUMN_CANCEL_FOLLOW_URL,
    COLUMN_FOLLOWERS_URL,
    COMMENT_CANCEL_VOTE_URL,
    COMMENT_DETAIL_URL,
    COMMENT_VOTE_URL,
    LIVE_LIKE_URL,
    PEOPLE_CANCEL_FOLLOWERS_URL,
    PEOPLE_FOLLOWERS_URL,
    PEOPLE_FOLLOWING_COLLECTIONS_URL,
    QUESTION_CANCEL_FOLLOWERS_URL,
    QUESTION_FOLLOWERS_URL,
    SELF_DETAIL_URL,
    SEND_COMMENT_URL,
    SEND_MESSAGE_URL,
    TOPIC_CANCEL_FOLLOW_URL,
    TOPIC_FOLLOWERS_URL,
    WHISPERS_URL,
)
from .generator import generator_of
from .utils import get_result_or_error

__all__ = ['Me']


class Me(People):
    def __init__(self, pid, cache, session):
        """
        是 :any:`People` 的子类，表示当前登录的用户。
        除了提供用户的基本信息外，还提供各种用户操作
        （点赞，评论，收藏，私信、删除等）。

        ..  inheritance-diagram:: Me

        ..  seealso:: :class:`People`

        """
        super(Me, self).__init__(pid, cache, session)

    def _build_url(self):
        return SELF_DETAIL_URL

    # ----- generators -----

    @property
    @generator_of(PEOPLE_FOLLOWING_COLLECTIONS_URL, 'collection')
    def following_collections(self):
        """
        ..  warning:: 注意

            这一方法是 :any:`Me` 类独有的，其父类 :any:`People` 类没有此方法。

            根本原因是知乎并不允许获取除自己（登录用户）以外用户关注的收藏夹，
            至于为什么，我哪知道呀QAQ
        """
        return None

    @property
    @generator_of(WHISPERS_URL)
    def whispers(self):
        """
        私信列表
        """
        return None

    # ----- operations -----

    def vote(self, what, op='up'):
        """
        投票操作。也就是赞同，反对，或者清除（取消赞同和反对）。

        操作对象可以是答案，文章和评论。

        :param what: 要点赞的对象，可以是 :any:`Answer` 或 :any:`Article`
          或 :any:`Comment` 对象。
        :param str|unicode op: 对于答案可取值 'up', 'down', 'clear'，
          分别表示赞同、反对和清除。
          对于文章和评论，只能取 'up' 和 'clear'。默认值是 'up'。
        :return: 表示结果的二元组，第一项表示是否成功，第二项表示原因。
        :rtype: (bool, str)
        :raise: :any:`UnexpectedResponseException`
          当服务器回复和预期不符，不知道是否成功时。
        """
        from . import Answer, Article, Comment
        if isinstance(what, Answer):
            if op not in {'up', 'down', 'clear'}:
                raise ValueError(
                    'Operate must be up, down or clear for Answer.')
            return self._common_vote(ANSWER_VOTERS_URL, what, op)
        elif isinstance(what, Article):
            if op not in {'up', 'clear'}:
                raise ValueError('Operate must be up or clear for Article')
            return self._common_vote(ARTICLE_VOTE_URL, what, op)
        elif isinstance(what, Comment):
            if op not in {'up', 'clear'}:
                raise ValueError('Operate must be up or clear for Comment')
            return self._common_click(what, op == 'clear', COMMENT_VOTE_URL,
                                      COMMENT_CANCEL_VOTE_URL)
        else:
            raise TypeError(
                'Unable to voteup a {0}.'.format(what.__class__.__name__))

    def thanks(self, answer, thanks=True):
        """
        感谢或者取消感谢答案。

        ..  seealso::

            返回值和可能的异常同 :any:`vote` 方法

        :param  Answer answer: 要感谢的答案
        :param bool thanks: 如果是想取消感谢，请设置为 False
        """
        from .answer import Answer
        if not isinstance(answer, Answer):
            raise TypeError('This method only accept Answer object.')
        return self._common_click(answer, not thanks,
                                  ANSWER_THANKS_URL, ANSWER_CANCEL_THANKS_URL)

    def unhelpful(self, answer, unhelpful=True):
        """
        给答案点没有帮助，或者取消没有帮助。

        ..  seealso::

            返回值和可能的异常同 :any:`vote` 方法

        :param Answer answer: 要操作的答案
        :param bool unhelpful: 如果是想撤销没有帮助，请设置为 False
        """
        from .answer import Answer
        if not isinstance(answer, Answer):
            raise TypeError('This method only accept Answer object.')
        return self._common_click(answer, not unhelpful,
                                  ANSWER_UNHELPFUL_URL,
                                  ANSWER_CANCEL_UNHELPFUL_URL)

    def follow(self, what, follow=True):
        """
        关注或者取消关注问题/话题/用户/专栏/收藏夹/Live。

        ..  seealso::

            返回值和可能的异常同 :any:`vote` 方法

        :param what: 操作对象
        :param follow: 要取消关注的话把这个设置成 False
        """
        from . import Question, Topic, People, Column, Collection, Live
        if isinstance(what, Question):
            return self._common_click(what, not follow,
                                      QUESTION_FOLLOWERS_URL,
                                      QUESTION_CANCEL_FOLLOWERS_URL)
        elif isinstance(what, Topic):
            return self._common_click(what, not follow, TOPIC_FOLLOWERS_URL,
                                      TOPIC_CANCEL_FOLLOW_URL)
        elif isinstance(what, People):
            what._get_data()
            return self._common_click(what, not follow, PEOPLE_FOLLOWERS_URL,
                                      PEOPLE_CANCEL_FOLLOWERS_URL)
        elif isinstance(what, Column):
            return self._common_click(what, not follow, COLUMN_FOLLOWERS_URL,
                                      COLUMN_CANCEL_FOLLOW_URL)
        elif isinstance(what, Collection):
            return self._common_click(what, not follow,
                                      COLLECTION_FOLLOWERS_URL,
                                      COLLECTION_CANCEL_FOLLOW_URL)
        elif isinstance(what, Live):
            return self._common_click(what, not follow,
                                      LIVE_LIKE_URL, LIVE_LIKE_URL)
        else:
            raise TypeError(
                'Unable to follow a {0}.'.format(what.__class__.__name__))

    def block(self, what, block=True):
        """
        屏蔽用户/话题

        ..  seealso::

            返回值和可能的异常同 :any:`vote` 方法

        :param what: 操作对象，用户或话题
        :param bool block: 如果要取消屏蔽请设置为 False
        """
        from . import People
        if isinstance(what, People):
            return self._common_block(what, not block, BLOCK_PEOPLE_URL,
                                      CANCEL_BLOCK_PEOPLE_URL)
        else:
            raise TypeError(
                'Unable to block a {0}.'.format(what.__class__.__name__))

    def collect(self, answer, collection, collect=True):
        """
        收藏答案进收藏夹。

        ..  warning::

            就算你提供的是别人的收藏夹也会返回成功……但是操作其实是无效的

        ..  seealso::

            返回值和可能的异常同 :any:`vote` 方法

        :param Answer answer: 要收藏的答案
        :param Collection collection: 要加入哪个收藏夹
        :param bool collect: 如果想要取消收藏请设置为 False
        """
        from . import Answer, Collection
        if not isinstance(answer, Answer):
            raise TypeError('Unable to add a {0} to collection.'.format(
                answer.__class__.__name__))
        if not isinstance(collection, Collection):
            raise TypeError('Unable add answer to a {0}.'.format(
                collection.__class__.__name__))
        if collect:
            data = {'add_collections': collection.id}
        else:
            data = {'remove_collections': collection.id}
        url = ANSWER_COLLECT_URL.format(answer.id)
        res = self._session.put(url, data=data)
        return get_result_or_error(url, res)

    def message(self, who, content):
        """
        发送私信。

        ..  seealso::

            返回值和可能的异常同 :any:`vote` 方法

        :param  People who: 接收者
        :param str|unicode content: 私信内容
        """
        from . import People
        if not isinstance(who, People):
            raise TypeError(
                'Unable to send message to {0}'.format(who.__class__.__name__))
        _ = who.name
        data = {
            'receiver_id': who.id,
            'content': content,
        }
        res = self._session.post(SEND_MESSAGE_URL, data=data)
        return get_result_or_error(SEND_MESSAGE_URL, res)

    def comment(self, what, content, parent=None):
        """
        向答案发送评论

        ..  seealso::

            返回值和可能的异常同 :any:`vote` 方法

        ..  warning:: 奇怪

            让我很诧异的是，就算「想要回复的评论」不属于「想要评论的主体」，
            知乎的 API 也会返回执行成功。而且经过测试，这条回复真的有效，
            会出现在评论主体的评论列表里。暂时不知道被评论用户的会不会收到消息。

            另外，莫名其妙的还可以回复自己的评论……

        :param what: 向哪里发送评论，可以是 :any:`Answer`, :any:`Article`
          :any:`Question`, :any:`Collection`
        :param str|unicode content: 评论内容
        :param Comment parent: 想要回复的评论，默认值为 None，则为正常的添加评论
        """
        from . import Answer, Article, Question, Collection, Comment
        data = {'content': content}
        if parent is not None:
            if not isinstance(parent, Comment):
                raise TypeError(
                    'parent comment must be Comment object, {0} given.'.format(
                        parent.__class__.__name__))
            data.update(comment_id=parent.id)
        if isinstance(what, (Answer, Article, Collection, Question)):
            data.update({'type': what.__class__.__name__.lower(),
                         'resource_id': what.id})
        else:
            raise TypeError('Can\'t add comment to a {0}.'.format(
                what.__class__.__name__))
        res = self._session.post(SEND_COMMENT_URL, data=data)
        print(res.text)
        return get_result_or_error(SEND_COMMENT_URL, res)

    def delete(self, what):
        """
        删除……一些东西，目前可以删除答案，评论，收藏夹，文章。

        ..  seealso::

            返回值和可能的异常同 :any:`vote` 方法

        ..  warning::

            请注意，本方法没有经过完整的测试，加上删除操作不可撤销，
            所以使用时请谨慎。

        :param what: 要删除的对象，可以是 :any:`Answer`, :any:`Comment`,
          :any:`Collection`, :any:`Article`
        """
        from . import Answer, Comment, Collection, Article
        if isinstance(what, Answer):
            url = ANSWER_DETAIL_URL.format(what.id)
        elif isinstance(what, Comment):
            url = COMMENT_DETAIL_URL.format(what.id)
        elif isinstance(what, Collection):
            url = COLLECTION_DETAIL_URL.format(what.id)
        elif isinstance(what, Article):
            url = ARTICLE_DETAIL_URL.format(what.id)
        else:
            raise TypeError(
                'Can\'t delete a {0}.'.format(what.__class__.__name__))
        res = self._session.delete(url)
        return get_result_or_error(url, res)

    def _common_click(self, what, cancel, click_url, cancel_url):
        if cancel:
            method = 'DELETE'
            url = cancel_url.format(what.id, self.id)
        else:
            method = 'POST'
            url = click_url.format(what.id)
        res = self._session.request(method, url)
        return get_result_or_error(url, res)

    def _common_vote(self, url, what, op):
        data = {
            'voteup_count': 0,
            'voting': {'up': 1, 'down': -1, 'clear': 0}[op],
        }
        url = url.format(what.id)
        res = self._session.post(url, data=data)
        return get_result_or_error(url, res)

    def _common_block(self, what, cancel, block_url, cancel_url):
        _ = what.name
        if cancel:
            method = 'DELETE'
            data = None
            url = cancel_url.format(what.id)
        else:
            method = 'POST'
            data = {'people_id': what.id}
            url = block_url
        res = self._session.request(method, url, data=data)
        return get_result_or_error(url, res)
