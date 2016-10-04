Paging data process - 多页数据处理
==================================


intro - 介绍
------------

知乎有很多列表型数据，比如问题的答案，我的关注者，专栏的文章，等等。

这些数据在知乎的 API 获取的时候是间断的，比如，每次获取 20 个，在手机 APP
上就体现为继续上划加载更多。这些数据处理的逻辑类似，数据的格式也类似，
只是最后列表项中的对象不同。

常见的多页数据的 JSON 如下：

..  code-block:: python

    {
        'paging': {
            'previous': 'previous page url' ,
            'next': 'next page url',
            'is_end': False, # or True
        },
        'data': [
            {
                'type': 'answer',
                'id': 'xxxx',
                'created_time': '14xxxxx'
                # many attr
            },
            {
                # like last one
            },
            # many many objects
        ],
    }

为了 DYR，这些逻辑被抽象成 :any:`BaseGenerator` 基类，其他类通过继承基类，
来实现创建不同对象的功能。

效果见：:ref:`intro_generator_attr`

Base class - 基类
-----------------

..  autoclass:: zhihu_oauth.zhcls.generator.BaseGenerator
    :members:
    :undoc-members:
    :private-members:
    :special-members: __init__, __getitem__, __next__, __iter__

Childs - 子类
---------------

:any:`BaseGenerator` 的子类才是真正可以使用的类。它们重载了 ``_build_obj`` 方法。
因其他结构无变化，故文档省略。

..  automodule:: zhihu_oauth.zhcls.generator
    :members:
    :exclude-members: BaseGenerator
    :undoc-members:
    :private-members:
    :special-members: __init__
