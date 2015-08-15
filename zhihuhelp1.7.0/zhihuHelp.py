# -*- coding: utf-8 -*-
# 放置于首位
import sys  # 修改默认编码
reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(100000) #为了适应知乎上的长答案，需要专门设下递归深度限制。。。

# 将./codes添加至库目录中
extendLibPath = r"./codes"
sys.path.append(extendLibPath)

from codes.main import *

mainClass = ZhihuHelp()
mainClass.helperStart()
