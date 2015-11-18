# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
__author__ = 'yao'

import sys

reload(sys)
sys.setdefaultencoding('utf8')
import json

# 添加库路径
currentPath = sys.path[0].replace('parse_unit', '')
sys.path.append(currentPath)
sys.path.append(currentPath + r'codes')
sys.path.append(currentPath + r'codes\parser')
print sys.path
sys.setrecursionlimit(1000000)  # 为了适应知乎上的长答案，需要专门设下递归深度限制。。。

from baseClass import *
from parserTools import *

is_info = True

content = open('./unit_html/author_info.html', 'r').read()
parser = AuthorParser(content)

if is_info:
    BaseClass.printDict(parser.get_extra_info())
    print '----------------------'
    print '=========================='
else:


    for answer in parser.get_answer_list():
        BaseClass.printDict(answer)
        print '----------------------'
    print '=========================='

    for question in parser.get_question_list():
        BaseClass.printDict(question)
        print '----------------------'