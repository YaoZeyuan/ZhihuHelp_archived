# -*- coding: utf-8 -*-
# 放置于首位
import sys  # 修改默认编码
import os  # 添加系统路径
import traceback

base_path = unicode(os.path.abspath('.').decode(sys.stdout.encoding))
sys.path.insert(0, base_path + u'/src/lib')  # 添加基础库路径 使用insert方式，确保优先启用项目自带源码包
sys.path.insert(0, base_path + u'/src/lib/oauth')  # zhihu oauth 类需要作为默认类导入，否则无法运行 - -

reload(sys)
sys.setdefaultencoding('utf-8')

#  执行主程序
from src.main import ZhihuHelp

try:
    helper = ZhihuHelp()
    helper.start()
except Exception:
    traceback.print_exc()
    print u"助手发生异常，点击任意键退出"
    raw_input()
pass
