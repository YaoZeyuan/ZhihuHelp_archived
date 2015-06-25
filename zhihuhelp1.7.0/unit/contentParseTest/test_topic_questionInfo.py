# -*- coding: utf-8 -*-
__author__ = 'yao'


u"""
对话题_问题信息进行测试
"""


import os
import  sys#修改默认编码#放置于首位

reload(sys)
sys.setdefaultencoding('utf-8')
rootPath = os.path.abspath('../../')
sys.path.append(rootPath)
from codes import contentParse   #可以利用这个方法导入上级目录中的库

from correct_topic_questionInfo import checkList

import unittest

class MyTestCase(unittest.TestCase):
    u"""
    先检测questionInfoDict
    """
    def setUp(self):
        content = open("../htmlFile/topicContent/topic1.html", "r").read()
        parseResult = contentParse.ParseTopic(content)
        self.questionInfoDictList, self.answerDictList = parseResult.getInfoDict()

    def failedTips(self, testedKey, index = 0):
        u"""
        当测试失败时，输出提示语句
        :param testedkey:
        :param correctValue:
        :return tipString:
        """
        testedKey    = testedKey.encode("utf-8")
        correctValue = checkList[index][testedKey]
        tipString = u"""\n
        {testedKey} parse error
        self.questionInfoDictList[{index}]['{testedKey}'] should equal {correctValue}
        but the self.questionInfoDictList[{index}]['{testedKey}'] = {errorValue}
                    """.encode("utf-8").format(testedKey=testedKey,index=index,
                    correctValue=correctValue, errorValue=self.questionInfoDictList[index][testedKey])
        return tipString

    """

    def test_questionAnswerCount(self):
        index = 0
        for questionInfo in self.questionInfoDictList:
            self.assertEqual(questionInfo["questionAnswerCount"],
                             checkList[index]["questionAnswerCount"],
                             self.failedTips("questionAnswerCount", index)
                             )
            index += 1

    def test_questionCommentCount(self):
        index = 0
        for questionInfo in self.questionInfoDictList:
            self.assertEqual(questionInfo["questionCommentCount"],
                             checkList[index]["questionCommentCount"],
                             self.failedTips("questionCommentCount", index)
                             )
            index += 1

    def test_questionDesc(self):
        index = 0
        for questionInfo in self.questionInfoDictList:
            self.assertEqual(questionInfo["questionDesc"],
                             checkList[index]["questionDesc"],
                             self.failedTips("questionDesc", index)
                             )
            index += 1

    def test_questionFollowCount(self):
        index = 0
        for questionInfo in self.questionInfoDictList:
            self.assertEqual(questionInfo["questionFollowCount"],
                             checkList[index]["questionFollowCount"],
                             self.failedTips("questionFollowCount", index)
                             )
            index += 1

    def test_questionViewCount(self):
        index = 0
        for questionInfo in self.questionInfoDictList:
            self.assertEqual(questionInfo["questionViewCount"],
                             checkList[index]["questionViewCount"],
                             self.failedTips("questionViewCount", index)
                             )
            index += 1
    """

    def test_questionIDinQuestionDesc(self):
        index = 0
        for questionInfo in self.questionInfoDictList:
            self.assertEqual(questionInfo["questionIDinQuestionDesc"],
                             checkList[index]["questionIDinQuestionDesc"],
                             self.failedTips("questionIDinQuestionDesc", index)
                             )
            index += 1

    def test_questionTitle(self):
        index = 0
        for questionInfo in self.questionInfoDictList:
            self.assertEqual(questionInfo["questionTitle"],
                             checkList[index]["questionTitle"],
                             self.failedTips("questionTitle", index)
                             )
            index += 1

if __name__ == '__main__':
    unittest.main()
