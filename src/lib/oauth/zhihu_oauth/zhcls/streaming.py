# coding=utf-8

from __future__ import unicode_literals

import functools
import copy

__all__ = ['StreamingJSON', 'streaming']


class StreamingJSON:
    def __init__(self, json_data):
        """
        通过 ``dict`` 或者 ``list`` 来创建对象。
        """
        if not isinstance(json_data, (dict, list)):
            raise ValueError('Need dict or list to build StreamingJSON object.')
        self._json = copy.deepcopy(json_data)

    def raw_data(self):
        """
        有可能某些用户不喜欢使用 ``.`` 操作符而偏爱用 ``[]`` 来取字典内的数据，
        所以提供此方法返回未处理的数据 **的副本**，
        修改此副本对此对象内部数据无影响。

        :return: 内部封装数据的副本
        :rtype: dict|list
        """
        return copy.deepcopy(self._json)

    def __getattr__(self, item):
        """
        重写 ``.`` 操作符。``item`` 参数为 ``.`` 后要取的属性。也即将 ``obj.xxx``
        转换为 ``obj._json['xxx']``

        重载后的 ``__getattr__`` 的流程为：

        1. 判断 item 最后一个字符是不是 ``_``，若是则删去。这一步的作用是防止
           item 与 Python 内置关键字冲突。 参见：:any:`Question.redirection` 的
           ``from`` 数据以及 :ref:`说明 <tips-for-conflict-with-keyword>`。
        2. 取出 ``obj = self._json[item]``，若不存在则抛出异常。
        3. 如果 ``obj`` 是 ``dict`` 或者 ``list``， 返回 ``StreamingJSON(obj)``
        4. 否则直接返回 ``obj``。
        """
        if isinstance(self._json, dict):

            # 防止和 Python 内置关键字冲突
            if item.endswith('_'):
                item = item[:-1]
            if item in self._json:
                obj = self._json[item]
                if isinstance(obj, (dict, list)):
                    return StreamingJSON(obj)
                else:
                    return obj
            else:
                raise AttributeError("No attr {0} in my data {1}!".format(
                    item, self._json))
        else:
            raise ValueError("Can't use XX.xxx in list-like obj {0}, "
                             "please use XX[num].".format(self._json))

    def __getitem__(self, item):
        """
        重写 ``[]`` 操作符。item 参数为 ``[]`` 内数组下表。也即将 ``obj[0]``
        转换为 ``obj._json['0]``。

        如果 ``self._json`` 不是 ``list`` 型，或 ``item`` 不是 ``int`` 型，
        则抛出 ``ValueError``。

        如果取出的 ``obj`` 是 ``dict`` 或 ``list``，返回 ``StreamingJSON(obj)``
        否则直接返回 ``obj``。
        """
        if isinstance(self._json, list) and isinstance(item, int):
            obj = self._json[item]
            if isinstance(obj, (dict, list)):
                return StreamingJSON(obj)
            else:
                return obj

        raise ValueError("Can't use XX[num] in dict-like obj {0}, "
                         "please use XX.xxx.".format(self._json))

    def __iter__(self):
        """
        重写迭代行为。如果迭代对象是 ``dict`` 或 ``list``，返回
        ``StreamingJSON(obj)``，否则直接返回。
        """
        def _iter():
            for x in self._json:
                if isinstance(x, (dict, list)):
                    yield StreamingJSON(x)
                else:
                    yield x

        return _iter()

    def __len__(self):
        return len(self._json)

    def __str__(self):
        return str(self._json)

    def __repr__(self):
        return repr(self._json)

    def __contains__(self, item):
        return item in self._json

    def __bool__(self):
        return True if self._json else False

    def __nonzero__(self):
        return self.__bool__()


def streaming(name_in_json=None, use_cache=True):
    """

    本装饰器的作用为：

    1. 标识这个属性为流式 JSON 属性。
    2. 自动从对象的数据中取出对应属性，构建成 :any:`StreamingJSON` 对象。

    取数据流程如下：

    1. 如果 ``use_cache`` 为真，转 2，否则转 3。
    2. 尝试从 ``cache`` 中取需要的数据。失败转 3，成功转 5。
    3. 如果 ``data`` 不存在，则调用知乎 API 获取。
    4. 尝试从 ``data`` 中取需要的数据。失败则
       将被装饰方法的调用结果视为取到的数据。
    5. 如果取到数据是 ``dict`` 或 ``list`` 类型，则返回使用
       :any:`StreamingJSON` 包装过的结果。如果不是则抛出 ``ValueError`` 异常。

    ..  seealso:: 关于 cache 和 data

        请看 :any:`Base` 类中的\ :any:`说明 <Base.__init__>`。

    :param name_in_json: 要取的数据在 JSON
      中的名字。可空，默认为使用本装饰器的的方法名。
    :param use_cache: 是否使用缓存的数据。默认为 ``True``。如果为
      ``False`` 则只使用 data。
    :raise ValueError: 当最终取到的数据不是 ``dict`` 或 ``list`` 类型时。
    """
    def wrappers_wrapper(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            name = name_in_json if name_in_json else func.__name__
            if use_cache and self._cache and name in self._cache:
                cache = self._cache[name]
            else:
                self._get_data()
                if self._data and name in self._data:
                    cache = self._data[name]
                else:
                    cache = func(self, *args, **kwargs)

            if isinstance(cache, (dict, list)):
                return StreamingJSON(cache)
            else:
                raise TypeError('Only dict and list can be StreamingJSON.')

        return wrapper

    return wrappers_wrapper
