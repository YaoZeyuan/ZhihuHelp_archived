# coding=utf-8

from __future__ import unicode_literals

import hashlib
import hmac
import time

__all__ = ['login_signature']


def login_signature(data, secret):
    """
    为登录请求附加签名。

    :param dict data: POST 数据
    :param str|unicode secret: APP SECRET
    :return: 经过签名后的 dict， 增加了 timestamp 和 signature 两项
    """
    data['timestamp'] = str(int(time.time()))

    params = ''.join([
        data['grant_type'],
        data['client_id'],
        data['source'],
        data['timestamp'],
    ])

    data['signature'] = hmac.new(
        secret.encode('utf-8'),
        params.encode('utf-8'),
        hashlib.sha1
    ).hexdigest()
