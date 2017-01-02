# coding=utf-8

from __future__ import unicode_literals

import itertools
import warnings

from ..exception import (
    MyJSONDecodeError,
    UnexpectedResponseException,
    CantGetTickets
)
from .base import Base
from .generator import generator_of
from .normal import normal_attr
from .other import other_obj
from .streaming import streaming
from .urls import (
    LIVE_DETAIL_URL,
    LIVE_ENDED_URL,
    LIVE_MEMBERS_URL,
    LIVE_ONGOING_URL,
    LIVE_RELATED_URL,
    LIVE_TICKETS_URL,
    LIVE_TICKETS_ENDED_URL,
    LIVE_TICKETS_QUIET_URL,
)

__all__ = ['Live', 'LiveTag', 'LiveTicket', 'LiveBadge']


class LiveBadge(Base):
    def __init__(self, lbid, cache, session):
        super(LiveBadge, self).__init__(lbid, cache, session)

    def _build_url(self):
        return None

    @property
    @normal_attr()
    def avatar_url(self):
        return None

    @property
    @normal_attr()
    def id(self):
        return self._id

    @property
    @normal_attr()
    def name(self):
        return None


class LiveTag(Base):
    def __init__(self, ltid, cache, session):
        super(LiveTag, self).__init__(ltid, cache, session)

    def _build_url(self):
        return None

    @property
    @normal_attr('available_num')
    def available_count(self):
        return None

    @property
    @normal_attr()
    def created_at(self):
        return None

    @property
    @normal_attr()
    def id(self):
        return self._id

    @property
    @normal_attr('live_num')
    def live_count(self):
        return None

    @property
    @normal_attr()
    def name(self):
        return None

    @property
    @normal_attr()
    def score(self):
        return None

    # ----- generators -----

    @property
    @generator_of(LIVE_ONGOING_URL, 'LiveOfTag')
    def lives_ongoing(self):
        return None

    @property
    @generator_of(LIVE_ENDED_URL, 'LiveOfTag')
    def lives_ended(self):
        return None

    @property
    def lives(self):
        from ..helpers import shield
        for live in itertools.chain(
                shield(self.lives_ongoing),
                shield(self.lives_ended)
        ):
            yield live


class LiveTicket(Base):
    def __init__(self, product_id, cache, session):
        super(LiveTicket, self).__init__(product_id, cache, session)

    def _build_url(self):
        return None

    @property
    @other_obj('LiveBadge', module_filename='live')
    def badge(self):
        return None

    @property
    @normal_attr('product_id')
    def id(self):
        return self._id

    @property
    @streaming('price')
    def __price(self):
        return None

    @property
    def price(self):
        return self.__price.amount

    @property
    def price_unit(self):
        return self.__price.unit


class Live(Base):
    def __init__(self, lid, cache, session):
        super(Live, self).__init__(lid, cache, session)

    def _build_url(self):
        return LIVE_DETAIL_URL.format(self.id)

    # ----- simple info -----

    @property
    @normal_attr()
    def alert(self):
        """
        提示语，就是客户端里显示为淡蓝色背景的那一块文字。
        """
        return None

    @property
    @normal_attr()
    def can_speak(self):
        return None

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
    def ends_at(self):
        return None

    @property
    @normal_attr()
    def ends_in(self):
        """
        正数表示还剩多久结束，0 应该表示已经结束了，如果是负数表示…………表示啥呢？
        """
        return None

    @property
    @streaming("fee")
    def __fee(self):
        return None

    @property
    def fee(self):
        """
        费用（一般这是最低票价），不过数值是 x 100 的，比如 999 表示 9.99
        """
        return self.__fee.amount

    @property
    def fee_unit(self):
        """
        费用的单位，一般就是 RMB 吧…………
        """
        return self.__fee.unit

    @property
    @normal_attr()
    def feedback_score(self):
        """
        反馈评分，应该是 0 - 5 吧。
        """
        return None

    @property
    @normal_attr()
    def has_feedback(self):
        """
        是否有反馈？
        """
        return None

    @property
    @normal_attr()
    def id(self):
        return self._id

    @property
    @normal_attr()
    def is_admin(self):
        return None

    @property
    @normal_attr()
    def in_promotion(self):
        """
        是否处于促销中
        """
        return None

    @property
    @normal_attr()
    def is_muted(self):
        return None

    @property
    @normal_attr()
    def liked(self):
        return None

    @property
    def liked_count(self):
        return self.liked_num

    @property
    @normal_attr()
    def liked_num(self):
        return None

    @property
    @normal_attr()
    def note(self):
        return None

    @property
    @normal_attr()
    def purchasable(self):
        """
        可否购买？
        """
        return None

    @property
    @normal_attr()
    def role(self):
        """
        返回一个字符串，表示于 Live 的关系。

        'visitor' 表示未参与 Live。

        ‘audience’ 表示参与了 Live，作为观众。

        '<一个我不知道的值>' 表示是组织者，因为我没开过 Live，所以不知道是什么值。

        '<另一个我不知道的值>' 表示是协作者，我也没协助过别人，所以也不知道 =。=
        """
        return None

    @property
    @streaming("seats")
    def seat(self):
        """
        Live 参与情况

        常见返回值：

        ..  code-block: javascript

            {
                "max": 500,     // 最多 500 人参与
                "taken": 278,   // 已有 278 人参与
            }

        做了两个 shortcut 属性 `:any:`seat_max` 和 :any:`seat_taken`， 可以直接使用。
        """
        return None

    @property
    def seat_max(self):
        """
        最大参与人数，其实是从 :any:`seat` 属性里取的。
        """
        return self.seat.max

    @property
    def seat_taken(self):
        """
        已参与人数，其实是从 :any:`seat` 属性里取的。
        """
        return self.seat.taken

    @property
    @streaming("speaker")
    def __speaker(self):
        return None

    @property
    @other_obj("people", "READ_FROM_RETURN_VALUE")
    def speaker(self):
        """
        演讲者，:any:`People` 对象。
        """
        return self.__speaker.member.raw_data()

    @property
    @normal_attr()
    def starts_at(self):
        return None

    @property
    @normal_attr()
    def subject(self):
        """
        Live 的主题，其实就是标题，所以有同功能的属性 :any:`Live.title`
        """
        return None

    @property
    def title(self):
        """
        ..  seealso:: :any:`subject`
        """
        return self.subject

    # ----- generators -----

    @property
    @streaming('cospeakers')
    def __cospeakers(self):
        return None

    @property
    def cospeakers(self):
        from .people import People

        # noinspection PyTypeChecker
        for people in self.__cospeakers:
            yield People(people.id, people.raw_data(), self._session)

    @property
    @generator_of(LIVE_MEMBERS_URL, "PeopleWithLiveBadge")
    def participants(self):
        """
        参与 Live 的人，这个生成器用法比较奇特，请看下面的例子：

        ..  code-block:: python

            live = client.live(789426202925346816)

            for role, badge, people in live.members:
                print(role, badge.name, people.name)

        其中 role 为 'audience' 表示观众，除了这个值暂时没发现别的取值。

        badge 为一个 :any:`LiveBadge` 对象，一般能用到的也就 id 和 name 属性。

        第三个 people 就是标准的 :any:`People` 对象了。
        """
        return None

    @property
    @generator_of(LIVE_RELATED_URL, 'live')
    def related(self):
        return None

    @property
    @streaming('tags')
    def __tags(self):
        return None

    @property
    def tags(self):
        """
        返回 :any:`LiveTag` 对象的生成器，但目前看来应该每个 Live 只有一个 Tag。
        """
        # noinspection PyTypeChecker
        for tag in self.__tags:
            yield LiveTag(tag.id, tag.raw_data(), self._session)

    def __try_ticket_request(self, url):
        res = self._session.post(url)
        try:
            data = res.json()
            return data
        except MyJSONDecodeError:
            raise UnexpectedResponseException(
                url, res,
                'a json string.',
            )

    @property
    def tickets(self):
        """
        ..  warning::

            此接口无法用于当前登录用户已参与的 Live。当强行调用时，
            此函数将产生一个警告并且不会有任何返回。

        正常情况下返回的是 :any:`LiveTicket` 对象的生成器。
        """

        if self.role != 'visitor':
            warnings.warn(CantGetTickets)
        else:
            normal_url = LIVE_TICKETS_URL.format(self.id)
            quiet_url = LIVE_TICKETS_QUIET_URL.format(self.id)
            ended_url = LIVE_TICKETS_ENDED_URL.format(self.id)

            if self.ends_in == 0:
                url = ended_url
            elif self.seat_taken >= self.seat_max:
                url = quiet_url
            else:
                url = normal_url

            data = self.__try_ticket_request(url)

            if 'error' in data and 'code' in data['error']:
                if data['error']['code'] == 4046:
                    data = self.__try_ticket_request(quiet_url)
                elif data['error']['code'] == 4048:
                    data = self.__try_ticket_request(ended_url)

            try:
                data = data['product_list']
            except KeyError:
                raise UnexpectedResponseException(
                    quiet_url, data,
                    'a json string contains [product_list] attr.',
                )

            for ticket in data:
                yield LiveTicket(ticket['product_id'], ticket, self._session)
