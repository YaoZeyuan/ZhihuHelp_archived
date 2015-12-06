# -*- coding: utf-8 -*-
# 放置于首位
import sys  # 修改默认编码

reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(100000)  # 为BS解析知乎上的长答案增加递归深度限制

src_path = r"./src"
extend_lib_path = r'./src/lib'
sys.path.append(src_path)
sys.path.append(extend_lib_path)

from src.main import ZhihuHelp

helper = ZhihuHelp()
helper.start()
