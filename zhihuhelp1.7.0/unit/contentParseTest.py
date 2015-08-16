# -*- coding: utf-8 -*-

import sys
reload(sys)  
sys.setdefaultencoding('utf8')

# 添加库路径
currentPath = sys.path[0]
currentPath = currentPath.replace('unit', '')
print currentPath
sys.path.append(currentPath)
sys.setrecursionlimit(1000000) #为了适应知乎上的长答案，需要专门设下递归深度限制。。。

from codes.baseClass import *
from codes.contentParse import *


htmlContent = open('./unit_html/error.html', 'r').read()
parse = ParseQuestion(htmlContent)
# import pprint
# infoDictList = parse.getInfoDict()
# pprint.pprint(infoDictList)
#exit()

questionInfoDictList, answerDictList = parse.getInfoDict()

for question in questionInfoDictList:
    BaseClass.printDict(question)

print '=========================='

# for answer in answerDictList:
#    BaseClass.printDict(answer)
