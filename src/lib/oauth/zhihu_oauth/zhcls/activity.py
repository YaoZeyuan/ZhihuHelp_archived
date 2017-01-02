# coding=utf-8

from __future__ import unicode_literals

import importlib

from .normal import normal_attr
from .streaming import StreamingJSON
from .utils import SimpleEnum
from ..exception import UnimplementedException

_verb_to_type_map = {
    'ANSWER_CREATE': 'CREATE_ANSWER',
    'ANSWER_VOTE_UP': 'VOTEUP_ANSWER',
    'EBOOK_VOTE_UP': 'VOTEUP_EBOOK',
    'LIVE_JOIN': 'JOIN_LIVE',
    'LIVE_PUBLISH': 'PUBLISH_LIVE',
    'MEMBER_COLLECT_ANSWER': 'COLLECT_ANSWER',
    'MEMBER_COLLECT_ARTICLE': 'COLLECT_ARTICLE',
    'MEMBER_CREATE_ARTICLE': 'CREATE_ARTICLE',
    'MEMBER_CREATE_PIN': 'CREATE_PIN',
    'MEMBER_FOLLOW_COLLECTION': 'FOLLOW_COLLECTION',
    'MEMBER_FOLLOW_COLUMN': 'FOLLOW_COLUMN',
    'MEMBER_FOLLOW_ROUNDTABLE': 'FOLLOW_ROUNDTABLE',
    'MEMBER_FOLLOW_TOPIC': 'FOLLOW_TOPIC',
    'MEMBER_LIKE_PIN': 'LIKE_PIN',
    'MEMBER_VOTEUP_ARTICLE': 'VOTEUP_ARTICLE',
    'QUESTION_CREATE': 'CREATE_QUESTION',
    'QUESTION_FOLLOW': 'FOLLOW_QUESTION',
    'TOPIC_FOLLOW': 'FOLLOW_TOPIC',
}

ActType = SimpleEnum(_verb_to_type_map.values())
"""
ActType 是用于表示用户动态类型的枚举类，可供使用的常量有：

================= ================ ======================
常量名              说明              `target` 属性类型
================= ================ ======================
COLLECT_ANSWER     收藏答案          比较特殊，见下文
COLLECT_ARTICLE    收藏文章          比较特殊，见下文
CREATE_ANSWER      回答问题          :any:`Answer`
CREATE_ARTICLE     发表文章          :any:`Article`
CREATE_PIN         发表分享          :any:`StreamingJSON`
CREATE_QUESTION    提出问题          :any:`Question`
FOLLOW_COLLECTION  关注收藏夹        :any:`Collection`
FOLLOW_COLUMN      关注专栏          :any:`Column`
FOLLOW_QUESTION    关注问题          :any:`Question`
FOLLOW_ROUNDTABLE  关注圆桌          :any:`StreamingJSON`
FOLLOW_TOPIC       关注话题          :any:`Topic`
LIKE_PIN           赞了分享          :any:`StreamingJSON`
JOIN_LIVE          参加 Live         :any:`Live`
PUBLISH_LIVE       举办 Live         :any:`Live`
VOTEUP_ANSWER      赞同回答          :any:`Answer`
VOTEUP_ARTICLE     赞同文章          :any:`Article`
VOTEUP_EBOOK       赞了电子书         :any:`StreamingJSON`
================= ================ ======================

收藏答案和收藏文章的 Target 属性是一个 dict，结构如下：

..  code-block:: javascript

    {
        'answer/article': <Answer object> or <Article object>,
        'collection': <Collection object>,
    }

``answer/article`` 表示被收藏的答案/文章，``collection`` 表示被收藏进的收藏夹，因为只有这两个动作有两个
操作对象，所以特殊处理了一下。

"""


def _verb_to_type(verb):
    type_str = _verb_to_type_map.get(verb, None)
    if type_str is None:
        raise UnimplementedException(
            'Unknown activity type: {0}. '
            'Please send this error message to '
            'developer to get help.'.format(verb))
    return getattr(ActType, _verb_to_type_map[verb])


class Activity(object):
    def __new__(cls, data, session):
        if data['verb'] == 'MEMBER_FOLLOW_ROUNDTABLE':
            data['type'] = ActType.FOLLOW_ROUNDTABLE
            return StreamingJSON(data)
        elif data['verb'] == 'MEMBER_LIKE_PIN':
            data['type'] = ActType.LIKE_PIN
            return StreamingJSON(data)
        elif data['verb'] == 'MEMBER_CREATE_PIN':
            data['type'] = ActType.CREATE_PIN
            return StreamingJSON(data)
        elif data['verb'] == 'EBOOK_VOTE_UP':
            data['type'] = ActType.VOTEUP_EBOOK
            return StreamingJSON(data)
        else:
            return super(Activity, cls).__new__(cls)

    def __init__(self, data, session):
        """
        表示用户的一条动态。

        :any:`type <Activity.type>` 属性标识了动态的类型，其取值及意义请参见
        :any:`ActType`。

        :any:`target <Activity.target>` 属性表示这次动态操作的目标，根据
        `type` 的不同，这个属性的类型也不同。但是基本都是
        `type` 的最后一个单词表示的类型，请看下面的例子。

        ..  note:: 举例

            ..  code-block:: python

                from zhihu_oauth import ZhihuClient, ActType # 记得要导入 ActType

                client = ZhihuClient()

                # Client 登录过程省略

                me = client.me()

                for act in me.activities:
                    if act.type == ActType.CREATE_ANSWER:
                        print(act.target.question.title)

            上面这段代码只处理类型是创建答案的动态，此时 `act.target` 就是
            :any:`Answer` 类型，和 `CREATE_ANSWER` 的 `ANSWER` 对应。
        """
        self._data = data
        self._type = _verb_to_type(data['verb'])
        self._session = session
        self._get_target()

    @property
    @normal_attr()
    def action_text(self):
        return None

    @property
    @normal_attr()
    def created_time(self):
        """
        用户动态的时间戳。
        """
        return None

    @property
    def type(self):
        """
        动态的类型。

        ..  seealso:: :any:`ActType`
        """
        return self._type

    @property
    def target(self):
        """
        动态的操作目标。

        ..  seealso:: :any:`Activity.__init__`, :any:`ActType`
        """
        return self._target

    def _get_target(self):
        pos = self._type.rfind('_')
        if pos == -1:
            raise UnimplementedException('Unable to get class from type name')
        filename = self._type[pos + 1:].lower()
        class_name = filename.capitalize()
        module = importlib.import_module('.' + filename, 'zhihu_oauth.zhcls')
        cls = getattr(module, class_name)
        self._target = cls(self._data['target']['id'], self._data['target'],
                           self._session)

        # 对收藏答案类型的特殊处理
        if self._type in {ActType.COLLECT_ANSWER, ActType.COLLECT_ARTICLE}:
            from .collection import Collection
            obj = self._target
            collection = Collection(
                self._data['target']['collection']['id'],
                self._data['target']['collection'],
                self._session
            )
            self._target = {
                'collection': collection,
                class_name.lower(): obj,
            }
