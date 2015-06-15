# -*- coding: utf-8 -*-
__author__ = 'yao'

import os
import  sys#修改默认编码#放置于首位

reload(sys)
sys.setdefaultencoding('utf-8')
rootPath = os.path.abspath('../')
sys.path.append(rootPath)
from codes import contentParse   #可以利用这个方法导入上级目录中的库

import unittest

class MyTestCase(unittest.TestCase):
    u"""
    先检测questionInfoDict
    """
    def setUp(self):
        content = open("./htmlFile/questionContent/question1.html", "r").read()
        testQuestion = contentParse.ParseQuestion(content)
        self.questionInfoDictList, self.answerDictList = testQuestion.getInfoDict();
        self.questionInfoDict = self.questionInfoDictList[0]

    def failedTips(self, testedKey, correctValue):
        u"""
        当测试失败时，输出提示语句
        :param testedkey:
        :param correctValue:
        :return tipString:
        """
        testedKey    = testedKey.encode("utf-8")
        correctValue = correctValue.encode("utf-8")
        tipString = u"""\n
        {testedKey} parse error
        questionInfoDict['{testedKey}'] should equal {correctValue}
        but the self.questionInfoDict['{testedKey}'] = {errorValue}
                    """.encode("utf-8").format(testedKey=testedKey,
                    correctValue=correctValue, errorValue=self.questionInfoDict[testedKey])
        return tipString

    def test_questionAnswerCount(self):
        self.assertEqual(self.questionInfoDict['questionAnswerCount'],
                         u"525".encode("utf-8"),
                         u"questionAnswerCount parse error")

    def test_questionCommentCount(self):
        self.assertEqual(self.questionInfoDict['questionCommentCount'],
                         "33".encode("utf-8"),
                         self.failedTips("questionCommentCount", u"33")
                        )

    def test_questionDesc(self):
        self.assertEqual(self.questionInfoDict['questionDesc'],
                         u"""源自《找死的兔子》，看不懂这一张，求解释。""".encode("utf-8"),
                         self.failedTips(u"questionDesc", u"源自《找死的兔子》，看不懂这一张，求解释。")
                         )

    def test_questionFollowCount(self):
        self.assertEqual(self.questionInfoDict['questionFollowCount'],
                         u"22069".encode("utf-8"),
                         self.failedTips(u"questionFollowCount", u"22069")
                         )

    def test_questionIDinQuestionDesc(self):
        self.assertEqual(self.questionInfoDict['questionIDinQuestionDesc'],
                         u"22480996".encode("utf-8"),
                         self.failedTips(u"questionIDinQuestionDesc", u"22480996")
                         )

    def test_questionTitle(self):
        self.assertEqual(self.questionInfoDict['questionTitle'],
                         u"你的家传祖业，有什么精彩的内行故事吗？ ".encode("utf-8"),
                         self.failedTips(u"questionTitle", u"你的家传祖业，有什么精彩的内行故事吗？ ")
                         )

    def test_questionViewCount(self):
        self.assertEqual(self.questionInfoDict['questionViewCount'],
                         u"4350568".encode("utf-8"),
                         self.failedTips(u"questionViewCount", u"4350568")
                         )

if __name__ == '__main__':
    unittest.main()
