# -*- coding: utf-8 -*-
__author__ = 'yao'


u"""
对问题_问题信息进行测试
"""


import os
import  sys#修改默认编码#放置于首位

reload(sys)
sys.setdefaultencoding('utf-8')
rootPath = os.path.abspath('../../')
sys.path.append(rootPath)
from codes import contentParse   #可以利用这个方法导入上级目录中的库

from correct_question_questionInfo import checkList

checkData = checkList[0]  #对问题信息的测试只有一个测试项，所以可以使用checkData替代checkList

import unittest

class MyTestCase(unittest.TestCase):
    u"""
    先检测questionInfoDict
    """
    def setUp(self):
        content = open("../htmlFile/questionContent/question1.html", "r").read()
        testQuestion = contentParse.ParseQuestion(content)
        self.questionInfoDictList, self.answerDictList = testQuestion.getInfoDict()
        self.questionInfoDict = self.questionInfoDictList[0]

    def failedTips(self, testedKey):
        u"""
        当测试失败时，输出提示语句
        :param testedkey:
        :param correctValue:
        :return tipString:
        """
        testedKey    = testedKey.encode("utf-8")
        correctValue = checkData[testedKey]
        tipString = u"""\n
        {testedKey} parse error
        self.questionInfoDict['{testedKey}'] should equal {correctValue}
        but the self.questionInfoDict['{testedKey}'] = {errorValue}
                    """.encode("utf-8").format(testedKey=testedKey,
                    correctValue=correctValue, errorValue=self.questionInfoDict[testedKey])
        return tipString

    def test_questionAnswerCount(self):
        self.assertEqual(self.questionInfoDict['questionAnswerCount'],
                         checkData["questionAnswerCount"],
                         self.failedTips("questionAnswerCount")
                         )

    def test_questionCommentCount(self):
        self.assertEqual(self.questionInfoDict['questionCommentCount'],
                         checkData["questionCommentCount"],
                         self.failedTips("questionCommentCount")
                        )

    def test_questionDesc(self):
        self.assertEqual(self.questionInfoDict['questionDesc'],
                         checkData["questionDesc"],
                         self.failedTips("questionDesc")
                         )

    def test_questionFollowCount(self):
        self.assertEqual(self.questionInfoDict['questionFollowCount'],
                         checkData["questionFollowCount"],
                         self.failedTips("questionFollowCount")
                         )

    def test_questionIDinQuestionDesc(self):
        self.assertEqual(self.questionInfoDict['questionIDinQuestionDesc'],
                         checkData["questionIDinQuestionDesc"],
                         self.failedTips("questionIDinQuestionDesc")
                         )

    def test_questionTitle(self):
        self.assertEqual(self.questionInfoDict['questionTitle'],
                         checkData["questionTitle"],
                         self.failedTips("questionTitle")
                         )

    def test_questionViewCount(self):
        self.assertEqual(self.questionInfoDict['questionViewCount'],
                         checkData["questionViewCount"],
                         self.failedTips("questionViewCount")
                         )

if __name__ == '__main__':
    unittest.main()
