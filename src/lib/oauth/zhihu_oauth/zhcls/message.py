from __future__ import unicode_literals

from .base import Base
from .other import other_obj
from .normal import normal_attr

__all__ = ['Message']


class Message(Base):
    def __init__(self, mid, cache, session):
        super(Message, self).__init__(mid, cache, session)

    def _build_url(self):
        return ''

    # ----- simple info -----

    @property
    @normal_attr()
    def created_time(self):
        return None

    @property
    @normal_attr()
    def content(self):
        return None

    @property
    @other_obj('people')
    def sender(self):
        return None

    @property
    @other_obj('people')
    def receiver(self):
        return None

    def format(self, template='[{time}] {sender} --> {receiver}: {content}'):
        """
        格式化输出消息

        ``{time}`` 时间戳；``{sender}`` 发送者用户名；``{receiver}`` 接收者用户名；
        ``{content}`` 消息内容

        用法参见示例。

        :param str template: 格式化模板
        :return: 格式化后的字符串
        :rtype: str
        """
        return template.format(
            time=self.created_time,
            sender=self.sender.name,
            receiver=self.receiver.name,
            content=self.content,
        )

    def __str__(self):
        return self.format()

    __repr__ = __str__
