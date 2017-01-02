# coding=utf-8

# from __future__ import unicode_literals

try:
    # python2
    from urllib import urlencode
except ImportError:
    # python3
    # noinspection PyUnresolvedReferences,PyCompatibility
    from urllib.parse import urlencode

ZHIHU_API_ROOT = 'https://api.zhihu.com'
"""知乎 API 的根目录"""

# ------- Zhihu OAuth Keys -------

CLIENT_ID = '8d5227e0aaaa4797a763ac64e0c3b8'
"""
默认的 CLIENT ID。
如果 :class:`.ZhihuClient` 构造时没有提供 CLIENT ID，则使用这个值。
"""

APP_SECRET = 'ecbefbf6b17e47ecb9035107866380'
"""
默认的 SECRET。
如果 :class:`.ZhihuClient` 构造时没有提供 SECRET，则使用这个值。
"""

# ------- Zhihu Client Info -------

API_VERSION = '3.0.40'
"""
模拟 Android 官方客户端使用的参数，表示使用的 API 版本。
如果 :class:`.ImZhihuAndroidClient` 构造时没有提供 api_version，则使用这个值。
"""

APP_VERSION = '4.11.0'
"""
模拟 Android 官方客户端使用的参数，表示使用的 APP 版本。
如果 :class:`.ImZhihuAndroidClient` 构造时没有提供 app_version，则使用这个值。
"""

APP_BUILD = 'release'
"""
模拟 Android 官方客户端使用的参数，表示使用的 APP 的 Build 类型。
如果 :class:`.ImZhihuAndroidClient` 构造时没有提供 app_build，则使用这个值。
"""

UUID = 'AEAAr9mZtwpLBXhKkMM1KBVkyjX1MarA2KE='
"""
新加的一个东西，暂时不知道是啥的 ID
"""

DEFAULT_UA = 'Futureve/4.11.0 Mozilla/5.0 (Linux; Android 6.0.1; ' \
             'ONEPLUS A3000 Build/MXB48T; wv) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Version/4.0 Chrome/54.0.2840.85 ' \
             'Mobile Safari/537.36 Google-HTTP-Java-Client/1.22.0 (gzip)'
"""
新版本的 API 开始检查 UA了。
"""

APP_ZA = urlencode({
    'OS': 'Android',
    'Release': '6.0.1',
    'Model': 'ONEPLUS A3000',
    'VersionName': '4.11.0',
    'VersionCode': '446',
    'Width': '1080',
    'Height': '1920',
    'Installer': 'Google Play',
})
"""
模拟 Android 官方客户端使用的参数，表示使用的 APP 的 杂项数据。
如果 :class:`.ImZhihuAndroidClient` 构造时没有提供 app_za，则使用这个值。

..  note::
    它是一个 url encode 后的 dict

    参见 :meth:`.ImZhihuAndroidClient.__init__`
"""

# ------- Zhihu API URL for Login -------

CAPTCHA_URL = ZHIHU_API_ROOT + '/captcha'
"""
验证码相关

:GET: 是否需要验证码
:PUT: 获取验证码
:POST: 提交验证码
"""

# sign_in - POST - 用户登录

LOGIN_URL = ZHIHU_API_ROOT + '/sign_in'
"""
OAuth 登录地址
"""

LOGIN_DATA = {
    'grant_type': 'password',
    'source': 'com.zhihu.android',
    'client_id': '',
    'signature': '',
    'timestamp': '',
    'username': '',
    'password': '',
}
"""
登录数据格式。需要填充的只有用户名和密码。

`client_id` 会由 :class:`.ZhihuClient` 填写。

`timestamp` 和 `signature` 会由 :class:`.ZhihuClient` 内部调用的
:func:`.login_signature` 自动填写。
"""
