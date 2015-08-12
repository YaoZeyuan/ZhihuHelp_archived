# -*- coding: utf-8 -*-

import sys
reload(sys)  
sys.setdefaultencoding('utf8')

# 添加库路径
currentPath = sys.path[0]
currentPath = currentPath.replace('unit', '')
print currentPath
sys.path.append(currentPath)
print sys.path

from codes.baseClass import *
from codes.contentParse import *


questionFile = open('./unit_html/question.html', 'r').read()
parse = ParseQuestion(questionFile)


questionInfoDictList, answerDictList = parse.getInfoDict()
BaseClass.printDict(questionInfoDictList)
print '=========================='
BaseClass.printDict(answerDictList)
