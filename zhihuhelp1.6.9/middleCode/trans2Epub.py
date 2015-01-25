# -*- coding: utf-8 -*-

class AnswerFactory():
    u'用于将形似Question-Answer结构的电子书转换为html文件，储存于指定目录下，然后调用Epub模块进行生成'
    def __init__(self, resultDict = {}):
        self.baseDir = '.'
        self.filePath = {}
