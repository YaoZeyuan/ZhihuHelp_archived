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
from codes.setting import *


test = Setting()