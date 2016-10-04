# coding=utf-8

from __future__ import unicode_literals

import functools

from .exception import NeedLoginException, IdMustBeIntException

__all__ = ['need_login', 'int_id']


def need_login(func):
    """
    装饰器。作用于 :class:`.ZhihuClient` 中的某些方法，
    强制它们必须在登录状态下才能被使用。
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.is_login():
            return func(self, *args, **kwargs)
        else:
            raise NeedLoginException(func.__name__)

    return wrapper


def int_id(func):
    """
    装饰器。作用于 :class:`.ZhihuClient` 中需要整型 ID 来构建对应知乎类的方法。
    作用就是个强制类型检查。

    :raise: :class:`.IdMustBeIntException` 当传过来的 ID 不是整型的时候
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            some_id = args[0]
        except IndexError:
            some_id = None
        if not isinstance(some_id, int):
            raise IdMustBeIntException(func)
        return func(self, *args, **kwargs)

    return wrapper
