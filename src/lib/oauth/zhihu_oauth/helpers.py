# coding=utf-8

from __future__ import unicode_literals

import warnings

import requests.packages.urllib3 as urllib3

from .zhcls.utils import SimpleEnum
from .zhcls.generator import BaseGenerator, ActivityGenerator
from .exception import ZhihuException, ZhihuWarning


__all__ = ['SHIELD_ACTION', 'shield']


SHIELD_ACTION = SimpleEnum(
    ['EXCEPTION', 'PASS', 'STOP']
)
"""
ActType 是用于表示 shield 抵挡 Exception 达到最大次数后的动作的枚举类，取值如下：

================= ====================
常量名              说明
================= ====================
EXCEPTION          抛出异常
PASS               跳过，获取下一个数据
STOP               结束处理
================= ====================
"""


def shield(inner, durability=3, start_at=0, action=SHIELD_ACTION.EXCEPTION):
    """
    shield 函数用于自动处理知乎的各种生成器
    （如 :any:`People.followers`, :any:`Question.answers`） 在获取分页数据时出错的情况。

    ..  warning:: 用户动态的生成器因为获取方式比较特殊，无法被 shield 保护

    用法：

    比如我们想获取关注了某个专栏的用户分别关注了哪些话题……

    ..  code-block:: python

        column = client.column('zijingnotes')
        result = []
        for user in shield(column.followers, action=SHIELD_ACTION.PASS):
            L = []
            print("Start proc user", user.name)
            if user.over:
                print(user.over_reason)
                continue
            for topic in shield(user.following_topics, action=SHIELD_ACTION.PASS):
                print("Add topic", topic.name)
                L.append(topic.name)
            result.append(L)

        # output result

    :param inner: 需要被保护的生成器
    :param int durability: 耐久度，表示获取同一数据最多连续出错几次
    :param int start_at: 从第几个数据开始获取
    :param action: 当耐久度消耗完后的动作，参见 :any:`SHIELD_ACTION`，默认动作是抛出异常
    :return: 新的生成器……
    """
    if not isinstance(inner, BaseGenerator):
        raise ValueError('First argument must be Zhihu Generator Classes')
    if isinstance(inner, ActivityGenerator):
        raise ValueError(' Activity Generator is the only one can\'t be shield')
    offset = start_at
    hp = durability
    while True:
        i = -1
        try:
            for i, x in enumerate(inner.jump(offset)):
                yield x
                hp = durability
            break
        except (ZhihuException, urllib3.exceptions.MaxRetryError) as e:
            offset += i + 1
            hp -= 1
            warnings.warn(
                "[{type}: {e}] be shield when get NO.{offset} data".format(
                    type=e.__class__.__name__,
                    e=e,
                    offset=offset
                ),
                ZhihuWarning
            )
            if hp == 0:
                if action is SHIELD_ACTION.EXCEPTION:
                    raise e
                elif action is SHIELD_ACTION.PASS:
                    offset += 1
                    hp = durability
                elif action is SHIELD_ACTION.STOP:
                    break
                else:
                    raise e
