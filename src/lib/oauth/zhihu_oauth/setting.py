# coding=utf-8

from __future__ import unicode_literals

import re
import requests.adapters

ADAPTER_WITH_RETRY = requests.adapters.HTTPAdapter(
    max_retries=requests.adapters.Retry(
        total=10,
        status_forcelist=[403, 408, 500, 502]
    )
)

CAPTCHA_FILE = 'captcha.gif'
"""
请求验证码后储存文件名的默认值，现在的值是当前目录下的 captcha.gif。

仅在 :meth:`.ZhihuClient.login_in_terminal` 中被使用。
"""

re_answer_url = re.compile(
    r'^(?:https?://)?www.zhihu.com/question/\d+/answer/(\d+)/?$')
"""
答案 URL 的正则，用于 :any:`ZhihuClient.from_url` 方法。
"""

re_article_url = re.compile(r'^(?:https?://)?zhuanlan.zhihu.com/p/(\d+)/?$')
"""
文章 URL 的正则，用于 :any:`ZhihuClient.from_url` 方法。
"""

re_collection_url = re.compile(
    r'^(?:https?://)?www.zhihu.com/collection/(\d+)/?$')
"""
收藏夹 URL 的正则，用于 :any:`ZhihuClient.from_url` 方法。
"""

# TODO: 详细了解专栏 slug 的构成，更新正则
re_column_url = re.compile(r'^(?:https?://)?zhuanlan.zhihu.com/([^/ ]+)/?$')
"""
专栏 URL 的正则，用于 :any:`ZhihuClient.from_url` 方法。
"""

re_live_url = re.compile(r'^(?:https?://)?www.zhihu.com/lives/(\d+)/?$')
"""
Live URL 的正则，用于 :any:`ZhihuClient.from_url` 方法。
"""

re_people_url = re.compile(r'^(?:https?://)?www.zhihu.com/people/([^/ ]+)/?$')
"""
用户 URL 的正则，用于 :any:`ZhihuClient.from_url` 方法。
"""

re_question_url = re.compile(r'^(?:https?://)?www.zhihu.com/question/(\d+)/?$')
"""
问题 URL 的正则，用于 :any:`ZhihuClient.from_url` 方法。
"""

re_topic_url = re.compile(r'^(?:https?://)?www.zhihu.com/topic/(\d+)/?$')
"""
问题 URL 的正则，用于 :any:`ZhihuClient.from_url` 方法。
"""


RE_FUNC_MAP = {
    # RE             func      int id
    re_answer_url: ('answer', True),
    re_article_url: ('article', True),
    re_collection_url: ('collection', True),
    re_column_url: ('column', False),
    re_live_url: ('live', True),
    re_people_url: ('people', False),
    re_question_url: ('question', True),
    re_topic_url: ('topic', True),
}
"""
正则表达式于 :any:`ZhihuClient` 的方法的对应关系。

键是正则，值是二元组，两个值分别是方法名和是否需要将 ``id`` 转化为整数。
"""
