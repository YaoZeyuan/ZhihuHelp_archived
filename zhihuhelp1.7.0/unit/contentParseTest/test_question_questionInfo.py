# -*- coding: utf-8 -*-
__author__ = 'yao'

import os
import  sys#修改默认编码#放置于首位

reload(sys)
sys.setdefaultencoding('utf-8')
rootPath = os.path.abspath('../')
sys.path.append(rootPath)
from codes import contentParse   #可以利用这个方法导入上级目录中的库

from correctAnswerDict import checkList

import unittest

class MyTestCase(unittest.TestCase):
    u"""
    先检测questionInfoDict
    """
    def setUp(self):
        content = open("./htmlFile/questionContent/question1.html", "r").read()
        testQuestion = contentParse.ParseQuestion(content)
        self.questionInfoDictList, self.answerDictList = testQuestion.getInfoDict()

    def failedTips(self, testedKey, index):
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
        self.answerDictList[{index}]['{testedKey}'] should equal {correctValue}
        but the self.answerDictList[{index}]['{testedKey}'] = {errorValue}
                    """.encode("utf-8").format(testedKey=testedKey,index=index,
                    correctValue=correctValue, errorValue=self.answerDictList[index][testedKey])
        return tipString

    def test_answer_authorSign(self):
        index = 0
        for answer in self.answerDictList:
            self.assertEqual(answer["authorSign"],
                             checkList[index]["authorSign"],
                             self.failedTips("authorSign", index)
                             )
            index += 1

if __name__ == '__main__':
    unittest.main()
