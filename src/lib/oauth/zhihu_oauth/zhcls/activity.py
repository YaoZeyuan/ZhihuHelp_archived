# coding=utf-8

from __future__ import unicode_literals

import importlib

from .streaming import StreamingJSON
from .utils import SimpleEnum
from ..exception import UnimplementedException

_verb_to_type_map = {
    'MEMBER_VOTEUP_ARTICLE': 'VOTEUP_ARTICLE',
    'ANSWER_VOTE_UP': 'VOTEUP_ANSWER',
    'QUESTION_FOLLOW': 'FOLLOW_QUESTION',
    'ANSWER_CREATE': 'CREATE_ANSWER',
    'QUESTION_CREATE': 'CREATE_QUESTION',
    'MEMBER_CREATE_ARTICLE': 'CREATE_ARTICLE',
    'TOPIC_FOLLOW': 'FOLLOW_TOPIC',
    'MEMBER_FOLLOW_COLUMN': 'FOLLOW_COLUMN',
    'MEMBER_FOLLOW_TOPIC': 'FOLLOW_TOPIC',
    'MEMBER_FOLLOW_COLLECTION': 'FOLLOW_COLLECTION',
    'MEMBER_FOLLOW_ROUNDTABLE': 'FOLLOW_ROUNDTABLE'
}

ActType = SimpleEnum(_verb_to_type_map.values())
"""
ActType 是用于表示用户动态类型的枚举类，可供使用的常量有：

================= ================ =====================
常量名              说明              `target` 属性类型
================= ================ =====================
CREATE_ANSWER      回答问题          :any:`Answer`
CREATE_ARTICLE     发表文章          :any:`Article`
CREATE_QUESTION    提出问题          :any:`Question`
FOLLOW_COLLECTION  关注收藏夹        :any:`Collection`
FOLLOW_COLUMN      关注专栏          :any:`Column`
FOLLOW_QUESTION    关注问题          :any:`Question`
FOLLOW_ROUNDTABLE  关注圆桌          :any:`StreamingJSON`
FOLLOW_TOPIC       关注话题          :any:`Topic`
VOTEUP_ANSWER      赞同回答          :any:`Answer`
VOTEUP_ARTICLE     赞同文章          :any:`Article`
================= ================ =====================
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
        if data['verb'].endswith('ROUNDTABLE'):
            data['type'] = ActType.FOLLOW_ROUNDTABLE
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

                for act in me.activities:
                    if act.type == ActType.CREATE_ANSWER:
                        print(act.target.question.title)

            上面这段代码判断的类型是创建答案，此时 `act.target` 就是
            :any:`Answer` 类型，和 `CREATE_ANSWER` 的 `ANSWER` 对应。
        """
        self._data = data
        self._type = _verb_to_type(data['verb'])
        self._session = session
        self._get_target()

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
