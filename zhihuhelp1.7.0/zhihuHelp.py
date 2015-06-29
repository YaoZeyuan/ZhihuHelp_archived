# -*- coding: utf-8 -*-
# 放置于首位
import sys  # 修改默认编码
reload(sys)
sys.setdefaultencoding('utf-8')
# 将./codes添加至库目录中
extendLibPath = r"./codes"
sys.path.append(extendLibPath)

from codes.main import *

mainClass = ZhihuHelp()
mainClass.helperStart()
