# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# 添加库路径
currentPath = sys.path[0].replace('unit', '')
sys.path.append(currentPath)
sys.path.append(currentPath + r'codes')
sys.path.append(currentPath + r'codes\parser')

sys.setrecursionlimit(1000000)  # 为了适应知乎上的长答案，需要专门设下递归深度限制。。。

from baseClass import *
from login import Login
from init import Init

init = Init()
SqlClass.set_conn(init.getConn())
login = Login()
login.login()