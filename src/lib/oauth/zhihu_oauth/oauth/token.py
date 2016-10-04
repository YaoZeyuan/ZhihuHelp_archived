# coding=utf-8

from __future__ import unicode_literals

import json
import pickle
import time

from ..exception import MyJSONDecodeError

__all__ = ['ZhihuToken']


class ZhihuToken:
    def __init__(self, user_id, uid, access_token, expires_in, token_type,
                 refresh_token, cookie, lock_in=None, unlock_ticket=None):
        """
        知乎令牌。

        尽量不要直接使用这个类，而是用 :meth:`ZhihuToken.from_str` 或
        :meth:`ZhihuToken.form_dict` 或
        :meth:`ZhihuToken.from_file` 方法来构造。

        ..  note::

            本类仅在 :class:`.ZhihuClient` 类内使用，一般用户不需要了解。

        :param str|unicode user_id: 用户 ID
        :param int uid: 某个数字型用户 ID，貌似没啥用
        :param str|unicode access_token: 最重要的访问令牌
        :param int expires_in: 过期时间
        :param str|unicode token_type: 令牌类型
        :param str|unicode refresh_token: 刷新令牌
        :param str|unicode cookie: 登录成功后需要加上这段 Cookies
        :param int lock_in: 不知道用处
        :param str|unicode unlock_ticket: 不知道用处
        """
        self._create_at = time.time()
        self._user_id = uid
        self._uid = user_id
        self._access_token = access_token
        self._expires_in = expires_in
        self._expires_at = self._create_at + self._expires_in
        self._token_type = token_type
        self._refresh_token = refresh_token
        self._cookie = cookie

        # 以下两个属性暂时不知道用处
        self._lock_in = lock_in
        self._unlock_ticket = unlock_ticket

    @staticmethod
    def from_str(json_str):
        """
        从字符串读取 token。

        :param str|unicode json_str: 一个合法的代表知乎 Token 的 JSON 字符串
        :rtype: :class:`ZhihuToken`
        :raise ValueError: 提供的参数不合法时
        """
        try:
            return ZhihuToken.from_dict(json.loads(json_str))
        except (MyJSONDecodeError, ValueError):
            raise ValueError(
                '"{json_str}" is NOT a valid zhihu token json string.'.format(
                    json_str=json_str
                ))

    @staticmethod
    def from_dict(json_dict):
        """
        从字典读取 token。

        :param dict json_dict: 一个代表知乎 Token 的字典
        :rtype: :class:`ZhihuToken`
        :raise ValueError: 提供的参数不合法时
        """
        try:
            return ZhihuToken(**json_dict)
        except TypeError:
            raise ValueError(
                '"{json_dict}" is NOT a valid zhihu token json.'.format(
                    json_dict=json_dict
                ))

    @staticmethod
    def from_file(filename):
        """
        从文件读取 token。

        :param str|unicode filename: 文件名
        :rtype: :class:`ZhihuToken`
        """
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def save(self, filename):
        """
        将 token 保存成文件。

        :param str|unicode filename: 文件名
        :return: 无返回值
        """
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @property
    def user_id(self):
        """
        :return: 获取用户 ID
        :rtype: str
        """
        return self._user_id

    @property
    def type(self):
        """
        :return: 获取验证类型
        :rtype: str
        """
        return self._token_type

    @property
    def token(self):
        """
        :return: 获取访问令牌
        :rtype: str
        """
        return self._access_token
