# -*- coding: utf-8 -*-
import sys

from bs4 import BeautifulSoup
from src.lib.zhihu_parser.tools.parser_tools import ParserTools

reload(sys)
sys.setdefaultencoding('utf8')

# sys.setrecursionlimit(1000000)  # 为了适应知乎上的长答案，需要专门设下递归深度限制。。。
# 添加库路径
currentPath = sys.path[0].replace('unit', '')
sys.path.append(currentPath)
sys.path.append(currentPath + r'src')
sys.path.append(currentPath + r'src\tools')
sys.path.append(currentPath + r'src\parser')

content = open(u'./content.html').read()

parser = BeautifulSoup(content, 'html.parser')
tag_content = ParserTools.get_tag_content(parser)
parser
