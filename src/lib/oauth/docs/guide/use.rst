Usage - 使用方法
================

Charset - 关于字符编码
----------------------

Python 3 用户不用关心这一小节。

..  warning:: 给 Python 2 用户

    为了防止我被编码的不统一问题弄得焦头烂额，zhihu_oauth 内部统一
    使用 utf-8 编码。你可能需要自己处理 encode decode 之类乱七八糟的问题。

    如果你只是想使用 print 打印结果的话，最好导入一下 print function，
    因为 Python 2 自己的 print 会将 unicode 以 ``u'\uxxxx'`` 的方式输出，
    而导入了之后就相当于使用 Python 3 的 print 方法了。

    ..  code-block:: python

        from __future__ import print_function


Generic example - 通用示例
--------------------------

不管用什么方法，登录成功之后就可以愉快的使用了。

zhihu_oauth 的使用方法很简单，用已登录 :any:`ZhihuClient` 构造想要的对象，
然后取数据就好。

这里以 :any:`ZhihuClient.me` 为例，给一些通用的用法

Normal attr - 普通属性
~~~~~~~~~~~~~~~~~~~~~~

普通属性表示哪些通过 ``.`` 操作符能够直接取到基本数据类型的数据，例子如下：

..  code-block:: python

    # import、构建 client 以及登录知乎的代码省略

    me = client.me()

    print('name', me.name)
    print('headline', me.headline)
    print('description', me.description)

    print('following topic count', me.following_topic_count)
    print('following people count', me.following_topic_count)
    print('followers count', me.follower_count)

    print('voteup count', me.voteup_count)
    print('get thanks count', me.thanked_count)

    print('answered question', me.answer_count)
    print('question asked', me.question_count)
    print('collection count', me.collection_count)
    print('article count', me.articles_count)
    print('following column count', me.following_column_count)

产生如下输出

..  code-block:: none

    name 7sDream
    headline 二次元普通居民，不入流程序员，http://0v0.link
    description 关注本AI的话，会自动给你发私信的哟！
    following topic count 35
    following people count 101
    followers count 1294
    voteup count 2493
    get thanks count 760
    answered question 258
    question asked 18
    collection count 9
    article count 7
    following column count 11

Object attr and streaming call - 对象属性和流式调用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

有些属性对应的是知乎类或者知乎类的列表（生成器）。

生成器可以通过 ``for ... in ...`` 进行迭代。

知乎类可以通过连续的 ``.`` 操作符进行流式调用，直到获取到基本属性。

..  code-block:: python

    # 获取最近 5 个回答
    for _, answer in zip(range(5), me.answers):
        print(answer.question.title, answer.voteup_count)

    print('----------')

    # 获取点赞量最高的 5 个回答
    for _, answer in zip(range(5), me.answers.order_by('votenum')):
        print(answer.question.title, answer.voteup_count)

    print('----------')

    # 获取最近提的 5 个问题
    for _, question in zip(range(5), me.questions):
        print(question.title, question.answer_count)

    print('----------')

    # 获取最近发表的 5 个文章
    for _, article in zip(range(5), me.articles):
        print(article.title, article.voteup_count)

输出：

..  code-block:: none

    如何想象诸如超立方体之类的四维空间物体？ 10
    你的第一次心动献给了 ACGN 作品中的谁？ 3
    大年初一差点把自己饿死在家里是一种怎样的体验？以及有没有什么建议来规划自己的日常生活？ 1
    有哪些歌曲色气满满？ 27
    作为程序员，自己在Github上的项目被很多人使用是什么体验？ 32
    ----------
    只是为了好玩儿，如何学编程？ 593
    计算机领域有哪些短小精悍的轮子?(仅用于教学) 268
    小明打饭的问题？ 198
    如何写个爬虫程序扒下知乎某个回答所有点赞用户名单？ 116
    被盗版泛滥毁掉的行业，是如何一步一步走向消亡的？ 95
    ----------
    用户「松阳先生」的主页出了什么问题？ 1
    C++运算符重载在头文件中应该如何定义？ 1
    亚马逊应用市场的应用都是正版的吗？ 0
    Tkinter中event_generate创建的Event如何附加数据？ 1
    用Android Studio开发对电脑配置的要求？ 7
    ----------
    你们资道吗，知乎多了个新功能哟 7
    谢谢你关注我呀！！！ 28
    【软件推荐01】Seer——给Win加上空格预览功能 13
    终于寒假惹！准备开始写东西啦~ 14
    吐槽 + 更新说明 + 寒假专栏征求意见稿 10

Streaming JSON - 流式 JSON
~~~~~~~~~~~~~~~~~~~~~~~~~~

另一种和知乎类很像的东西叫做 :any:`StreamingJSON`。你可以把它想像成一个 JS 对象。
如果你不熟悉 JS 的话，那就想像成一个 Python 字典好了，只是这个字典不用 ``[]``，
而是用 ``.`` 来取出数据。

..  code-block:: python

    me = client.me()

    locations = me.locations

    print(locations)

    for location in locations:
        print(location.name, location.avatar_url)

输出（格式化后）：

..  code-block:: none

    [
        {
            'name':'天津',
            'avatar_url':'http://pic4.zhimg.com/acad405e7_s.jpg',
            'introduction':'天津，简称津，地处华北平原，自古因漕运而兴起，明永乐二年十一月二十一日（1404年12月23日）正式筑城，是中国古代唯一有确切建城时间记录的城市。经历600余年，特别是近代百年，造就了天津中西合璧、古今兼容的独特城市风貌。\xa0',
            'excerpt':'天津，简称津，地处华北平原，自古因漕运而兴起，明永乐二年十一月二十一日（1404年12月23日）正式筑城，是中国古代唯一有确切建城时间记录的城市。经历600余年，特别是近代百年，造就了天津中西合璧、古今兼容的独特城市风貌。 ',
            'type':'topic',
            'id':'19577238',
            'url':'https://api.zhihu.com/topics/19577238'
        }
    ]

    天津 http://pic4.zhimg.com/acad405e7_s.jpg

对照代码和输出，我相信你能理解什么叫做　StreamingJSON。

..  seealso:: 详细

    有关 StreamingJSON 的更多资料请看 :ref:`intro_streaming_json`


Get other object - 获取其他对象
-------------------------------

除了 :any:`Me` 以外，还有很多类可供使用，比如 :any:`Answer` 可以通过
:any:`ZhihuClient.answer` 方法获取，并输出答案的一些资料：

..  code-block:: python

    answer = client.answer(94150403)

    print(answer.question.title)
    print(answer.author.name)
    print(answer.voteup_count)
    print(answer.thanks_count)
    print(answer.created_time)
    print(answer.updated_time)

    for voter in answer.voters:
        print(voter.name, voter.headline)

输出如下：

..  code-block:: none

    如何评价南开大学津南校区的建设质量？
    7sDream
    4
    0
    1460039289
    1460088371
    秦承平 莫做开山怪，莫做开山怪！
    CINDY Warm♥Brave
    杀马特绅少 懂礼貌的好周绅
    codefalling https://github.com/CodeFalling

所有可用的类请转到 :ref:`知乎类文档 <for_user_zhcls>` 进行查看，用法均类似。

除了以上的使用方式外，:any:`ZhihuClient` 还提供了一个通用的，通过 URL 的创建知乎类对象的方法。

比如上述代码中的

``answer = client.answer(94150403)``

可以改写成

``answer = client.from_url('https://www.zhihu.com/question/42248369/answer/94150403')``

传递不同的 URL 可以获得不同的对象以供使用。

..  seealso:: 另见

    :any:`ZhihuClient.from_url`

Backup & Save - 备份和保存
--------------------------

zhihu_oauth 还提供了简单地备份（保存）答案和文章的功能。以答案为例：

..  code-block:: python

    question = client.question(35166763)

    print(question.title)

    for answer in question.answers:
        print(answer.author.name, answer.voteup_count)
        answer.save(question.title)

输出：

..  code-block:: none

    Dota2有什么你知道的小技巧？来恶补一下！？
    呵呵 341
    赵小胖 523
    隔壁小岚哥 69
    曹凌群 51
    匿名用户 43

    # many many author name

    匿名用户 0
    托托 0

结果：

..  figure:: /images/save-answer.png

.. seealso:: 保存

    答案保存功能的详细参数参见 :any:`Answer.save`

    文章保存功能的详细参数参见 :any:`Article.save`


What's Next - 下一步
--------------------

这里只用 :any:`Me` 类作为示例，其他类的用法其实也类似。

..  seealso:: 有那些类可以使用？

    请看 :ref:`知乎相关类文档 <for_user_zhcls>`

    用 :any:`ZhihuClient` 的生成这些对象的方法请看 :doc:`这里 <../for-user/client>`
