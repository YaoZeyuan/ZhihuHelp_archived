# -*- coding: utf-8 -*-
from src.lib.zhihu_parser.tools.parser_tools import ParserTools
from src.tools.debug import Debug


class SimpleQuestion(ParserTools):
    def __init__(self, dom=None):
        self.set_dom(dom)
        return

    def set_dom(self, dom):
        self.info = {}
        if dom:
            self.dom = dom
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        self.parse_question_id()
        self.parse_title()
        return self.info

    def parse_question_id(self):
        question = self.dom.select('h2 a.question_link')
        if not question:
            question = self.dom.select('h2.zm-item-title a[target="_blank"]')  # 在收藏夹中需要使用这种选择器
        if not question:
            Debug.logger.debug(u'问题信息_id未找到')
            return
        href = self.get_attr(question[0], 'href')
        self.info['question_id'] = self.match_question_id(href)
        return

    def parse_title(self):
        question = self.dom.select('h2 a.question_link')
        if not question:
            question = self.dom.select('h2.zm-item-title a[target="_blank"]')  # 在收藏夹中需要使用这种选择器
        if not question:
            Debug.logger.debug(u'问题信息_title未找到')
            return
        self.info['title'] = question[0].get_text()
        return
