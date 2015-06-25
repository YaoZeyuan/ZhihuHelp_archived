# -*- coding: utf-8 -*-

u"""
基础的测试用函数
"""

__author__ = 'yao'

import datetime

def createCorrectData():
    u"""
    去除引号后使用
    content = open("../htmlFile/questionContent/question1.html", "r").read()
    testQuestion = contentParse.ParseQuestion(content)
    questionInfoDictList, answerDictList = testQuestion.getInfoDict()
    import json

    a = json.dumps(questionInfoDictList)
    print a
    """
    return

def getYesterday():
        today=datetime.date.today()
        oneday=datetime.timedelta(days=1)
        yesterday=today-oneday
        return yesterday

def getToday():
    return datetime.date.today()

TODAY = getToday().isoformat()
YESTERDAY = getYesterday().isoformat()


