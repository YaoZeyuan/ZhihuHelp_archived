# coding=utf-8

from __future__ import unicode_literals

import functools
import importlib

__all__ = ['other_obj']


def other_obj(class_name=None, name_in_json=None):
    """

    本装饰器的作用为：

    1. 标识这个属性为另一个知乎对象。
    2. 自动从当前对象的数据中取出对应属性，构建成所需要的对象。

    生成对象流程如下：

    1. 尝试导入类名表示的类，如果获取失败则设为 :any:`Base` 类。
    2. 尝试从 ``cache`` 中获取用来建立对象的数据。失败转 3，成功转 5。
    3. 如果当前对象没有 ``data`` 则调用知乎 API 获取。
    4. 尝试从 ``data`` 中获取数据。失败则将数据设置为被装饰函数的返回值。
    5. 将获取到的数据作为 ``cache`` 构建第一步中的导入的知乎类对象。

    ..  seealso:: 关于 cache 和 data

        请看 :any:`Base` 类中的\ :any:`说明 <Base.__init__>`。

    :param class_name: 要生成的对象类名
    :param name_in_json: 属性在 JSON 里的键名。
    """
    def wrappers_wrapper(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            cls_name = class_name or func.__name__
            cls_name = cls_name.capitalize()
            name_in_j = name_in_json or func.__name__
            file_name = '.' + cls_name.lower()

            try:
                module = importlib.import_module(file_name, 'zhihu_oauth.zhcls')
                cls = getattr(module, cls_name)
            except (ImportError, AttributeError):
                from .base import Base
                cls = Base

            if self._cache and name_in_j in self._cache:
                cache = self._cache[name_in_j]
            else:
                self._get_data()
                if self._data and name_in_j in self._data:
                    cache = self._data[name_in_j]
                else:
                    cache = func(self, *args, **kwargs)

            if cache is not None and 'id' in cache:
                return cls(cache['id'], cache, self._session)
            else:
                return None

        return wrapper

    return wrappers_wrapper
