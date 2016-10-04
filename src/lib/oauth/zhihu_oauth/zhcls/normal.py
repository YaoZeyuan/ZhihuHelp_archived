# coding=utf-8

from __future__ import unicode_literals, print_function

import functools

from .utils import can_get_from

__all__ = ['normal_attr']


def normal_attr(name_in_json=None):
    """

    本装饰器的作用为：

    1. 标识这个属性为常规属性。
    2. 自动从对象的数据中取对应属性返回，会自行判断需不需要请求网络。

    取数据流程如下：

    1. 如果 ``data`` 存在，转 2，否则转 3。
    2. 尝试从 ``data`` 中取数据，成功则返回数据，否则返回被装饰函数的执行结果。
    3. 尝试从 ``cache`` 中取需要的属性，成功则返回。
    4. 判断属性名是不是 ``id``。不是转 5，是则返回被装饰函数的执行结果。（因为
       ``id`` 属性一般在 :any:`_build_url` 方法中需要引用，
       如果这时向知乎请求数据会造成死循环。）
    5. 则使用 API 请求数据。然后转 2。

    ..  seealso:: 关于 cache 和 data

        请看 :any:`Base` 类中的\ :any:`说明 <Base.__init__>`。

    :param str|unicode name_in_json: 需要取的属性在 JSON 中的名字。可空，默认值为
      使用此装饰器的方法名。
    """
    def wrappers_wrapper(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):

            def use_data_or_func(the_name, data):
                if can_get_from(the_name, data):
                    return data[the_name]
                else:
                    return func(self, *args, **kwargs)

            name = name_in_json if name_in_json else func.__name__
            if self._data:
                return use_data_or_func(name, self._data)
            elif self._cache and can_get_from(name, self._cache):
                return self._cache[name]
            else:
                # id is important, when there is no data, _build_url need it,
                # so, just return the function result
                if name == 'id':
                    return func(self, *args, **kwargs)

                self._get_data()
                # noinspection PyTypeChecker
                if self._data:
                    return use_data_or_func(name, self._data)
        return wrapper

    return wrappers_wrapper
