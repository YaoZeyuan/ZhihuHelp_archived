# -*- coding: utf-8 -*-
# 放置于首位
import sys  # 修改默认编码
reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(100000)  # 为BS解析知乎上的长答案增加递归深度限制

# 将./codes添加至库目录中
extend_lib_path = r"./src"
sys.path.append(extend_lib_path)

from src.main import ZhihuHelp

helper = ZhihuHelp()
helper.start()
