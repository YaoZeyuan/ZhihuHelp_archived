# -*- coding: utf-8 -*-
# 放置于首位
import sys  # 修改默认编码
import os  # 添加系统路径

base_path = unicode(os.path.abspath('.').decode(sys.stdout.encoding))
sys.path.append(base_path + u'/src/lib')  # 添加基础库路径
sys.path.append(base_path + u'/src/lib/oauth')  # zhihu oauth 类需要作为默认类导入，否则无法运行 - -

reload(sys)
sys.setdefaultencoding('utf-8')

#  执行主程序
from src.main import ZhihuHelp

helper = ZhihuHelp()
helper.start()
