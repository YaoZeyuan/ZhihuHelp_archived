Intro - 知乎类文档阅读说明
==========================

Usage - 使用方法
----------------

所有知乎类都不建议手动构建，而应该使用 :any:`ZhihuClient` 提供的相应的
生成方法来创建。

如想得到一个答案对象，请使用 :any:`ZhihuClient.answer` 方法，其余类似。

每个类所需要的 ID 参数如何获取请参考 :any:`ZhihuClient` 类对应方法的文档。

..  seealso::

    :any:`ZhihuClient`

..  _intro_normal_attr:

Normal attr - 常规属性
----------------------

如果一个属性没有说明，则表示：

- 它的名称已经把自己描述的足够清楚了。
- 如果它是个单数，表示直接通过 ``.`` 操作符，
  能直接获取到基本类型 ``(str, int, float, bool)`` 的数据，或另一个知乎对象。

..  note:: 举例

    - :any:`Answer.voteup_count` 表示一个答案获得的赞同数（很明显是个 ``int``）。
    - :any:`Answer.author` 表示答案的作者（很明显应该是 :class:`.People` 类）。

..  _intro_streaming_json:

Streaming JSON attr - 流式 JSON 属性
------------------------------------

如果我说明了一个属性的常见返回值，则表示

- 它返回的是一个 :any:`StreamingJSON` 对象，可以想像成一个 JS Object。
- 它的属性可通过 ``.`` 和 ``[]`` 操作符进行遍历。

..  note:: 举例

    :any:`Answer.suggest_edit` 的常见返回值是

    ..  code-block:: python

        {
            'status': True,
            'title': '为什么回答会被建议修改',
            'tip': '作者修改内容通过后，回答会重新显示。如果一周内未得到有效修改，回答会自动折叠',
            'reason': '回答被建议修改：\\n不宜公开讨论的政治内容',
            'url': 'zhihu://questions/24752645'
        }

    表示我们可以

    - 通过 ``answer.suggest_edit.status`` 取到 ``True``
    - 通过 ``answer.suggest_edit.reason`` 取到 ``'回答被建议修改：\n不宜公开讨论的政治内容'``

..  note:: 再举例

    :any:`People.locations` 的常见返回值是

    ..  code-block:: python

        [
            {
                'introduction': '天津，简称津，地处华北平原，balabala,
                'url': 'https://api.zhihu.com/topics/19577238',
                'avatar_url': 'http://pic4.zhimg.com/acad405e7_s.jpg',
                'excerpt': '天津，简称津，地处华北平原 balabalabala',
                'type': 'topic',
                'name': '天津',
                'id': '19577238',
            },
        ],

    最外面是一个列表表示我们可以迭代它：

    ..  code-block:: python

        for location in people.locations:
            print(location.name, location.excerpt)

..  _tips-for-conflict-with-keyword:

..  note:: 提示

    如果某个属性和 Python 的关键字冲突，请在属性名后面加上下划线 ``_`` 即可。

对了，如果你不喜欢用 ``.`` 操作符，而偏爱标准dict和list的操作模式，你可以使用
:any:`raw_data` 方法获取到内部数据。

.. _intro_generator_attr:

Generator attr - 生成器属性
---------------------------

如果一个属性名是复数，又没有给出常见返回值，那么它是生成器属性。

这表示直接通过 ``.`` 操作符，能获取到一个生成器，生成它所表示的知乎对象列表。

..  note:: 举例

    - :any:`Answer.voters` 表示答案的所有点赞者（:any:`People` 对象的生成器）。
    - :any:`People.answers` 表示用户的所有答案（:any:`Answer` 对象的生成器）。

可以通过 ``for in loop`` 对它们进行迭代：

..  code-block:: python

    for answer in me.answers:
        print(answer.question.name, answer.voteup_count

某些属性可以通过 order_by 来指定排序，但是一般用不到。

目前发现的的用法见：:any:`BaseGenerator.order_by`。

Specification & Compatible - 规范 & 兼容
----------------------------------------

这个库遵循以下原则：

- 点赞一律用 vote，点赞者用 voter
- 收藏夹用 collection，收藏用 collect
- 某某某的数量一律用 ``xxx_count``，``xxx`` 使用单数形式
- 某某某的生成器一律用 ``xxxs``，即 ``xxx`` 的复数形式

例： :any:`Column.article_count` 专栏的文章数

例： :any:`Column.articles` 专栏所有文章的生成器

知乎返回的 JSON 大部分都很统一，比如用词的单复数，
用 vote 还是 like 表示点赞，等等这些。

但是就是有那么几个不合群。

如果你看到某个类有两个差不多的属性，他们的差别只是

- 某一个属性多了个 s
  （比如 :any:`Column.article_count` 和 :any:`Column.articles_count`）
- 两个属性意思相同
  （比如 :any:`People.favorited_count` 和 :any:`People.collected_count`）

那么：

- 有 s 的版本是我为了兼容知乎的原始数据加上的别名。
- 其中一个属性是我强行修改成符合我自己规范的名字。

这种做法只是为了兼容知乎原始数据，其实两个方法无任何区别（当然，除了名字）。
