# coding=utf-8

# from __future__ import unicode_literals

from .im_android import ImZhihuAndroidClient
from .token import ZhihuToken

__all__ = ['ZhihuOAuth']


class ZhihuOAuth(ImZhihuAndroidClient):
    def __init__(self, token, api_version=None, app_version=None,
                 app_build=None, app_za=None):
        """
        ..  inheritance-diagram:: ZhihuOAuth

        这个 Auth 在 :class:`.ImZhihuAndroidClient`
        的基础上加上了发送 token 的功能。

        :param ZhihuToken token: 成功登录后得到的 Token

        ..  seealso::
            以下参数的文档参见 :meth:`.ImZhihuAndroidClient.__init__`

        :param api_version:
        :param app_version:
        :param app_build:
        :param app_za:
        """
        assert isinstance(token, ZhihuToken)
        super(ZhihuOAuth, self).__init__(
            api_version, app_version, app_build, app_za)
        self._token = token

    def __call__(self, r):
        """
        ..  note::
            requests 会自动调用这个方法

        此函数在 PreparedRequest 的 HTTP header
        里加上了 HTTP Authorization 头，值为登录成功后 Zhihu 发的 access_token。

        由于是 :class:`.ImZhihuAndroidClient` 的子类，也会自动加上描述 APP 信息的头。

        ..  seealso::
            :meth:`.ImZhihuAndroidClient.__call__`
        """
        r = super(ZhihuOAuth, self).__call__(r)
        r.headers['Authorization'] = '{type} {token}'.format(
            type=str(self._token.type.capitalize()),
            token=str(self._token.token)
        )
        return r
