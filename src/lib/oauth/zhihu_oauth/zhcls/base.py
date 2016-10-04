# coding=utf-8

from __future__ import unicode_literals

import abc

from ..exception import MyJSONDecodeError, GetDataErrorException

from requests.adapters import MaxRetryError

__all__ = ['Base']


class Base(object):
    def __init__(self, zhihu_obj_id, cache, session):
        """

        ..  note:: Cache 与 Data

            :any:`Base` 类的 ``cache`` 参数表示已知的属性值。一般由另一个对象的
            JSON 数据中的一个属性充当。

            比如 :any:`Answer.author` 方法，由于在请求 :any:`Answer` 的数据时，
            原始 JSON 数据中就有关于作者的一些简单信息。比如 name，id，headline。
            在使用此方法时就会将这些不完整的数据传递到 ``answer`` 对象 （类型为
            :any:`People`）的 ``cache`` 中。这样一来，在执行
            ``answer.author.name`` 时，取出名字的操作可以省去一次网络请求。

            :any:`normal_attr`，:any:`other_obj` 和 :any:`streaming` 装饰器都会
            优先使用 ``cache`` 中的数据，当获取失败时才会调用
            :any:`_get_data` 方法请求数据。

        :param zhihu_obj_id: 构建知乎对象所用的 ID
        :param dict cache: 缓存数据，就是已知的这个对象的属性集
        :param session: 网络请求 Session
        """
        self._id = zhihu_obj_id
        self._cache = cache
        self._session = session
        self._data = None

    def _get_data(self):
        """
        调用知乎 API 接口获取数据的主要方法。

        url 从 :any:`_build_url` 中获取。

        method 从 :any:`_method` 中获取。

        params 从 :any:`_build_params` 中获取。

        data 从 :any:`_build_data` 中获取。

        :raise: 当返回的数据无法被解析成 JSON
          或 JSON 中含有 'message' 字段时，会抛出 :any:`GetDataErrorException`
        """
        if self._data is None:
            url = self._build_url()
            res = self._session.request(
                self._method(),
                url=url,
                params=self._build_params(),
                data=self._build_data(),
            )
            e = GetDataErrorException(
                url,
                res,
                'a valid Zhihu {0} JSON data'.format(self.__class__.__name__),
            )
            try:
                json_dict = res.json()
                if 'error' in json_dict:
                    raise e
                self._data = json_dict
            except MyJSONDecodeError:
                raise e

    @abc.abstractmethod
    def _build_url(self):
        """
        子类 **必须** 重载这一函数，提供获取数据的 API URL。

        一般格式为 ZHIHU_XXX_URL.format(self.id)
        """
        return ''

    # noinspection PyMethodMayBeStatic
    def _build_params(self):
        """
        子类可以重载这一函数，提供请求 API 时要传递的参数。默认值为 None。
        """
        return None

    # noinspection PyMethodMayBeStatic
    def _build_data(self):
        """
        子类可以重载这一函数，提供请求 API 时要传递的数据。默认值为 None。
        """
        return None

    # noinspection PyMethodMayBeStatic
    def _method(self):
        """
        子类可以重载这一函数，提供 HTTP 请求的类型，默认值为 GET。
        """
        return 'GET'

    def refresh(self):
        """
        删除自身的 cache 和 data，下一次获取属性会重新向知乎发送请求，获取最新数据。
        """
        self._data = self._cache = None

    @property
    def pure_data(self):
        """
        调试用。返回现在对象内的 JSON 数据。

        如果对象没有 cache 也没有 data，会自动发送数据请求 data。
        """
        if not self._cache:
            self._get_data()
        return {
            'cache': self._cache,
            'data': self._data,
        }
