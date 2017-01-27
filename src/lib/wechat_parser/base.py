# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.zhihu_parser.content.simple_answer import SimpleAnswer
from src.lib.zhihu_parser.content.simple_question import SimpleQuestion
from src.lib.wechat_parser.tools.parser_tools import ParserTools


class BaseParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')
