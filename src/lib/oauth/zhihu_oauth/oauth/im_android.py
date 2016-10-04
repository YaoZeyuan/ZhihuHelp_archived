# coding=utf-8

# from __future__ import unicode_literals

from requests.auth import AuthBase

from .setting import (
    API_VERSION, APP_VERSION, APP_BUILD, APP_ZA, UUID, DEFAULT_UA
)

__all__ = ['ImZhihuAndroidClient']


class ImZhihuAndroidClient(AuthBase):
    def __init__(self, api_version=None, app_version=None,
                 app_build=None, app_za=None, uuid=None, ua=None):
        """
        ..  inheritance-diagram:: ImZhihuAndroidClient

        这个 Auth 类用于模拟一些 Android 上的知乎官方客户端的特殊参数

        :param str|unicode api_version: 所用 API 版本
        :param str|unicode app_version: 客户端(APK) 版本
        :param str|unicode app_build: APP 类型？
        :param str|unicode app_za: APP 杂项，是一个 urlencoded 的 params dict
        :param str|unicode uuid: 暂时不知道是什么
        :param str|unicode ua: User-Agent，新 API 会验证 UA 了
        """
        self._api_version = api_version or API_VERSION
        self._app_version = app_version or APP_VERSION
        self._app_build = app_build or APP_BUILD
        self._app_za = app_za or APP_ZA
        self._uuid = uuid or UUID
        self._ua = ua or DEFAULT_UA

    def __call__(self, r):
        """
        ..  note::
            requests 会自动调用这个方法

        此函数在 PreparedRequest 的 HTTP header
        里加上了模拟 Android 客户端所需要的附加属性

        ..  seealso::
            自动添加的属性参见 :meth:`__init__`
        """
        r.headers['x-api-version'] = self._api_version
        r.headers['x-app-version'] = self._app_version
        r.headers['x-app-build'] = self._app_build
        r.headers['x-app-za'] = self._app_za
        r.headers['x-uuid'] = self._uuid
        r.headers['User-Agent'] = self._ua
        return r
