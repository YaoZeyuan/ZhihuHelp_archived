# -*- coding: utf-8 -*-
__author__ = 'yao'

import sys

reload(sys)
sys.setdefaultencoding('utf8')


# 添加库路径
currentPath = sys.path[0].replace('parse_unit', '')
sys.path.append(currentPath)
sys.setrecursionlimit(1000000)  # 为了适应知乎上的长答案，需要专门设下递归深度限制。。。

from codes.baseClass import *
from codes.contentParse import *
