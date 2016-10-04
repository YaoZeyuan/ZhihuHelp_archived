# coding=utf-8

# from __future__ import unicode_literals

from .im_android import ImZhihuAndroidClient

__all__ = ['BeforeLoginAuth']


class BeforeLoginAuth(ImZhihuAndroidClient):
    def __init__(self, client_id, api_version=None, app_version=None,
                 app_build=None, app_za=None, uuid=None, ua=None):
        """
        ..  inheritance-diagram:: BeforeLoginAuth
            :parts: 1

        这个 Auth 在 :class:`.ImZhihuAndroidClient`
        的基础上加上了发送 ``client_id`` 的功能。表示登录之前的基础验证。

        :param str|unicode client_id: 客户端 ID

        ..  seealso::
            以下参数的文档参见 :meth:`.ImZhihuAndroidClient.__init__`

        :param str|unicode api_version:
        :param str|unicode app_version:
        :param str|unicode app_build:
        :param str|unicode app_za:
        :param str|unicode uuid:
        :param str|unicode ua:
        """
        super(BeforeLoginAuth, self).__init__(
            api_version, app_version, app_build, app_za, uuid, ua)
        self._client_id = client_id

    def __call__(self, r):
        """
        ..  note::
            requests 会自动调用这个方法

        此函数在 PreparedRequest 的 HTTP header
        里加上了 HTTP Authorization 头，值为 CLIENT_ID。

        由于是 :class:`.ImZhihuAndroidClient` 的子类，也会自动加上描述 APP 信息的头。

        ..  seealso::
            :meth:`.ImZhihuAndroidClient.__call__`
        """
        r = super(BeforeLoginAuth, self).__call__(r)
        r.headers['Authorization'] = 'oauth {0}'.format(str(self._client_id))
        return r
