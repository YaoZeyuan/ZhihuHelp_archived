Streaming JSON - 流式 JSON
==========================

本模块用于处理在 知乎 API 返回的 JSON数据里的一部分流式 JSON 数据。

流式 JSON 属性的含义请看\ :ref:`这里 <intro_streaming_json>`。

如 :any:`People.locations`，:any:`Question.suggest_edit` 等。

Class intro - 类的介绍
----------------------

..  autoclass:: zhihu_oauth.zhcls.streaming.StreamingJSON
    :members:
    :undoc-members:
    :special-members: __init__, __getitem__, __getattr__, __iter__

Ancillary decorator - 配套装饰器
--------------------------------

下面这个装饰器就是各知乎类中用于标明哪些是流式 JSON 属性的，
类里的定义只是为了方便构建文档。真正返回数据的操作均由这一装饰器完成。

..  autofunction:: zhihu_oauth.zhcls.streaming.streaming
