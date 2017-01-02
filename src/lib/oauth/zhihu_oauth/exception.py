# coding=utf-8

from __future__ import unicode_literals

try:
    from json import JSONDecodeError as MyJSONDecodeError
except ImportError:
    MyJSONDecodeError = Exception
    """
    在 Py3 下是 json.JSONDecodeError。

    在 Py2 下是 BaseException，因为 Py2 的 json 模块没有提供解析异常。
    """

__all__ = [
    # warnings
    'ZhihuWarning',
    'IgnoreErrorDataWarning',
    'GetEmptyResponseWhenFetchData',
    'CantGetTicketsWarning',
    'CantGetTickets',
    # exceptions
    'ZhihuException',
    'UnexpectedResponseException',
    'GetDataErrorException',
    'NeedCaptchaException',
    'NeedLoginException',
    'IdMustBeIntException',
    'UnimplementedException',
    'MyJSONDecodeError',
]


class ZhihuException(Exception):
    pass


class UnexpectedResponseException(ZhihuException):
    def __init__(self, url, res, expect):
        """
        服务器回复了和预期格式不符的数据

        :param str|unicode url: 当前尝试访问的网址
        :param request.Response res: 服务器的回复
        :param str|unicode expect: 一个用来说明期望服务器回复的数据格式的字符串
        """
        self.url = url
        self.res = res
        self.expect = expect

    def __repr__(self):
        return 'Get an unexpected response when visit url ' \
               '"{self.url}", we expect "{self.expect}", ' \
               'but the response body is "{self.res.text}"'.format(self=self)

    __str__ = __repr__


class UnimplementedException(ZhihuException):
    def __init__(self, what):
        """
        处理当前遇到的情况的代码还未实现，只是开发的时候用于占位

        ..  note:: 一般用户不用管这个异常

        :param str|unicode what: 用来描述当前遇到的情况
        """
        self.what = what

    def __repr__(self):
        return 'Meet a unimplemented condition: {self.what}'.format(self=self)

    __str__ = __repr__


class GetDataErrorException(UnexpectedResponseException):
    def __init__(self, url, res, expect):
        """
        :class:`UnexpectedResponseException` 的子类，
        尝试获取服务器给出的错误信息。如果获取失败则显示父类的出错信息。

        ..  seealso:: :class:`UnexpectedResponseException`
        """
        super(GetDataErrorException, self).__init__(url, res, expect)
        try:
            self.reason = res.json()['error']['message']
        except (MyJSONDecodeError, KeyError):
            self.reason = None

    def __repr__(self):
        if self.reason:
            return 'A error happened when get data: {0}'.format(self.reason)
        else:
            base = super(GetDataErrorException, self).__repr__()
            return "Unknown error! " + base

    __str__ = __repr__


class NeedCaptchaException(ZhihuException):
    def __init__(self):
        """
        登录过程需要验证码
        """
        pass

    def __repr__(self):
        return "Need a captcha to login, " \
               "please catch this exception and " \
               "use client.get_captcha() to get it."

    __str__ = __repr__


class NeedLoginException(ZhihuException):
    def __init__(self, what):
        """
        使用某方法需要登录而当前客户端未登录

        :param str|unicode what: 当前试图调用的方法名
        """
        self.what = what

    def __repr__(self):
        return 'Need login to use the "{self.what}" method.'.format(self=self)

    __str__ = __repr__


class IdMustBeIntException(ZhihuException):
    def __init__(self, func):
        """
        获取对应的知乎类时，试图传递不是整数型的 ID

        :param function func: 当前试图调用的方法名
        """
        self.func = func.__name__

    def __repr__(self):
        return "You must provide a integer id " \
               "to use function: {self.func}".format(self=self)

    __str__ = __repr__


class ZhihuWarning(UserWarning):
    def __init__(self, message, *args, **kwargs):
        super(ZhihuWarning, self).__init__(*args, **kwargs)
        self._message = message

    def __str__(self):
        return str(self._message)

    __repr__ = __str__


class IgnoreErrorDataWarning(ZhihuWarning):
    def __init__(self, message, *args, **kwargs):
        super(IgnoreErrorDataWarning, self).__init__(message, *args, **kwargs)


GetEmptyResponseWhenFetchData = IgnoreErrorDataWarning(
    "试图获取下一项时，服务器返回了空数据。"
    "如果您是在获取某用户的粉丝，那么您可能遇到了知乎 5020 限制。"
    "虽然不知道为什么，但是好像知乎限制 API 只能访问前 5020 个粉丝，"
    "我也很为难，但是这是知乎做的限制，突破不了呀。"
    "目前在遇到这个问题时只能当作获取完处理了。"
)


class CantGetTicketsWarning(ZhihuWarning):
    def __init__(self, message, *args, **kwargs):
        super(CantGetTicketsWarning, self).__init__(message, *args, **kwargs)

CantGetTickets = CantGetTicketsWarning(
    '只能获取未参与过（也即 live.role == \'visitor\'）的 Live 的票价信息，'
    '对于其他情况此接口不会返回任何东西。这不会造成 for in 循环报错，'
    '但如果你不想看到这个警告，请……请在调用 tickets 属性前自行判断一下，'
    '或者偷懒强行过滤掉这个 warning ：）'
)
