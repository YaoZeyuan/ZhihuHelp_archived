# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools

class WechatParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')

    def get_article_list(self):
        return

    def get_question_dom_list(self):
        return self.dom.select('div.content')[:-1]

    def get_answer_dom_list(self):
        return self.dom.select('div.content')[:-1]
