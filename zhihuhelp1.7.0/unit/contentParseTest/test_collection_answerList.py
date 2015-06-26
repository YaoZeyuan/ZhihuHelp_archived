# -*- coding: utf-8 -*-
__author__ = 'yao'

u"""
对收藏夹_答案列表进行测试
"""

import os
import sys # 修改默认编码 # 放置于首位

reload(sys)
sys.setdefaultencoding('utf-8')
rootPath = os.path.abspath('../../')
sys.path.append(rootPath)

from codes import contentParse   #  可以利用这个方法导入上级目录中的库

from correct_collection_answerList import checkList

import unittest

class MyTestCase(unittest.TestCase):
    u"""
    先检测questionInfoDict
    """
    def setUp(self):
        content = open("../htmlFile/collectionContent/collection1.html", "r").read()
        parseResult = contentParse.ParseCollection(content)
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


    def test_answer_questionID(self):
        index = 0
        for answer in self.answerDictList:
            self.assertEqual(answer["questionID"],
                             checkList[index]["questionID"],
                             self.failedTips("questionID", index)
                             )
            index += 1

    def test_answer_noRecordFlag(self):
        index = 0
        for answer in self.answerDictList:
            self.assertEqual(answer["noRecordFlag"],
                             checkList[index]["noRecordFlag"],
                             self.failedTips("noRecordFlag", index)
                             )
            index += 1

    def test_answer_authorLogo(self):
        index = 0
        for answer in self.answerDictList:
            self.assertEqual(answer["authorLogo"],
                             checkList[index]["authorLogo"],
                             self.failedTips("authorLogo", index)
                             )
            index += 1

    def test_answer_answerHref(self):
        index = 0
        for answer in self.answerDictList:
            self.assertEqual(answer["answerHref"],
                             checkList[index]["answerHref"],
                             self.failedTips("answerHref", index)
                             )
            index += 1

    def test_answer_authorName(self):
        index = 0
        for answer in self.answerDictList:
            self.assertEqual(answer["authorName"],
                             checkList[index]["authorName"],
                             self.failedTips("authorName", index)
                             )
            index += 1

    def test_answer_commitDate(self):
        u"""
            日期分为当天、昨天、指定日期三种
            如果没有【编辑于】,则编辑日期应当等于创建日期
        """
        index = 0
        for answer in self.answerDictList:
            self.assertEqual(answer["commitDate"],
                             checkList[index]["commitDate"],
                             self.failedTips("commitDate", index)
                             )
            index += 1

    def test_answer_authorID(self):
        index = 0
        for answer in self.answerDictList:
            self.assertEqual(answer["authorID"],
                             checkList[index]["authorID"],
                             self.failedTips("authorID", index)
                             )
            index += 1

    def test_answer_answerID(self):
        index = 0
        for answer in self.answerDictList:
            self.assertEqual(answer["answerID"],
                             checkList[index]["answerID"],
                             self.failedTips("answerID", index)
                             )
            index += 1

    def test_answer_updateDate(self):
        index = 0
        for answer in self.answerDictList:
            self.assertEqual(answer["updateDate"],
                             checkList[index]["updateDate"],
                             self.failedTips("updateDate", index)
                             )
            index += 1

    def test_answer_answerCommentCount(self):
        index = 0
        for answer in self.answerDictList:
            self.assertEqual(answer["answerCommentCount"],
                             checkList[index]["answerCommentCount"],
                             self.failedTips("answerCommentCount", index)
                             )
            index += 1

    def test_answer_answerContent(self):
        index = 0
        for answer in self.answerDictList:
            self.assertEqual(answer["answerContent"],
                             checkList[index]["answerContent"],
                             self.failedTips("answerContent", index)
                             )
            index += 1

    def test_answer_answerAgreeCount(self):
        index = 0
        for answer in self.answerDictList:
            self.assertEqual(answer["answerAgreeCount"],
                             checkList[index]["answerAgreeCount"],
                             self.failedTips("answerAgreeCount", index)
                             )
            index += 1


if __name__ == '__main__':
    unittest.main()

