# -*- coding: utf-8 -*-

__author__ = 'yao'

if __name__ == '__main__':
    u"""
    导入基础模块
    """

    import os
    import sys # 修改默认编码 # 放置于首位

    reload(sys)
    sys.setdefaultencoding('utf-8')
    rootPath = os.path.abspath('../../')
    sys.path.append(rootPath)

    from codes import contentParse   #  可以利用这个方法导入上级目录中的库


def createCorrectData():
    u"""
    使用该函数，生成json格式的正确数据，利用json解析功能可直接转换为标准python数据代码
    """
    targetFile = "../htmlFile/answerContent/answer1.html"
    content = open(targetFile, "r").read()
    testQuestion = contentParse.ParseAnswer(content)
    questionInfoDictList, answerDictList = testQuestion.getInfoDict()
    import json

    a = json.dumps(answerDictList)
    print a  # 在此处打断点

    return

if __name__ == '__main__':
    createCorrectData()