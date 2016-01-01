# -*- coding: utf-8 -*-
import sys

from src.lib.zhihu_parser.author import AuthorParser
from src.lib.zhihu_parser.collection import CollectionParser
from src.lib.zhihu_parser.question import QuestionParser
from src.lib.zhihu_parser.topic import TopicParser
from src.tools.debug import Debug

reload(sys)
sys.setdefaultencoding('utf8')

# 添加库路径
currentPath = sys.path[0].replace('unit', '')
sys.path.append(currentPath)
sys.path.append(currentPath + r'src')
sys.path.append(currentPath + r'src\tools')
sys.path.append(currentPath + r'src\parser')

sys.setrecursionlimit(1000000)  # 为了适应知乎上的长答案，需要专门设下递归深度限制。。。

is_info = 0
kind = 'collection'  # 直接在这里替换类别即可完成测试。可供测试的类别见字典键值
unit ={
    'answer':{
        'src_answer':'./unit_html/single_answer.html',
        'src_info':'./unit_html/single_answer.html',
        'parser':QuestionParser,
    },
    'question':{
        'src_answer':'./unit_html/single_question.html',
        'src_info':'./unit_html/single_question.html',
        'parser':QuestionParser,
    },
    'author':{
        'src_answer':'./unit_html/author.html',
        'src_info':'./unit_html/author_info.html',
        'parser':AuthorParser,
    },
    'topic':{
        'src_answer':'./unit_html/topic.html',
        'src_info':'./unit_html/topic.html',
        'parser':TopicParser,
    },
    'collection':{
        'src_answer': './unit_html/collection.html',
        'src_info': './unit_html/collection.html',
        'parser': CollectionParser,
    },
    'private_collection': {
        'src_answer':'./unit_html/private_collection.html',
        'src_info':'./unit_html/private_collection.html',
        'parser':CollectionParser,
    },
}
if is_info:
    src = unit[kind]['src_info']
else:
    src = unit[kind]['src_answer']

content = open(src, 'r').read()
parser = unit[kind]['parser'](content)


if is_info:
    Debug.print_dict(parser.get_extra_info())
    print '----------------------'
    print '=========================='
else:
    for answer in parser.get_answer_list():
        Debug.print_dict(answer)
        print '----------------------'
    print '=========================='

    for question in parser.get_question_info_list():
        Debug.print_dict(question)
        print '----------------------'
