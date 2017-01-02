# coding=utf-8

from __future__ import unicode_literals

from .base import Base
from .other import other_obj
from .generator import generator_of
from .normal import normal_attr
from .urls import MESSAGES_URL

__all__ = ['Whisper']


class Whisper(Base):
    """
    唔，其实就是「和某人的所有消息」。

    为这个东西命名我想了半天……最后群里的一个小姐姐说叫 Whisper 吧，我觉得很可以诶~

    后来发现知乎接口里把这个叫做 Thread，嗯，不想改，我就是这么任性……
    """
    def _build_url(self):
        return ''

    def _get_data(self):
        pass

    def __init__(self, wid, cache, session):
        super(Whisper, self).__init__(wid, cache, session)

    # ----- simple info -----

    @property
    @normal_attr()
    def allow_reply(self):
        return None

    @property
    def id(self):
        return self._id

    @property
    @normal_attr()
    def snippet(self):
        """
        最后一次私信的摘要
        """
        return None

    @property
    @normal_attr()
    def updated_time(self):
        return None

    @property
    @normal_attr()
    def unread_count(self):
        return None

    @property
    @other_obj('people', 'participant')
    def who(self):
        """
        参与此私信会话的另一个知乎用户
        """
        return None

    @property
    @generator_of(MESSAGES_URL)
    def messages(self):
        return None
