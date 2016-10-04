Comment - 评论
==============

..  topic:: 注意

    请先查看 :doc:`说明 <intro>` 了解一下知乎相关类的文档的阅读方法。
    否则你会看不懂下面的东西的…………

..  topic:: 评论的获取方法

    评论类是不支持用评论 ID 来构造对象的，因为知乎并没有相关接口（或者是我没发现）

    目前只能通过其他类的 ``comments`` 属性（比如
    :any:`Answer.comments`，:any:`Question.comments`） 得到评论对象的迭代器。

..  automodule:: zhihu_oauth.zhcls.comment
    :members:
    :undoc-members:
