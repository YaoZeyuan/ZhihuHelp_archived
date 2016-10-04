Base - 基础类
=============

Base 类是所有知乎数据相关类的基类，网络请求仅在 :any:`Base` 类和
:any:`BaseGenerator` 类中实现。

:any:`Base` 类提供了可以重载的函数
函数让子类可以自定义网络请求的 URL，method，params，data 等参数。

..  inheritance-diagram:: zhihu_oauth.zhcls.base zhihu_oauth.zhcls.answer zhihu_oauth.zhcls.article zhihu_oauth.zhcls.collection zhihu_oauth.zhcls.column zhihu_oauth.zhcls.comment zhihu_oauth.zhcls.people zhihu_oauth.zhcls.me zhihu_oauth.zhcls.question zhihu_oauth.zhcls.topic
    :parts: 1

..  automodule:: zhihu_oauth.zhcls.base
    :members:
    :undoc-members:
    :special-members: __init__
    :private-members:
