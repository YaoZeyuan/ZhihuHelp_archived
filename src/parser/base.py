# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.parser.content.simple_answer import SimpleAnswer
from src.parser.content.simple_question import SimpleQuestion
from src.parser.tools.parser_tools import ParserTools


class BaseParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')
        self.answer_parser = SimpleAnswer()

    def get_answer_dom_list(self):
        return self.dom.select('.zm-item-answer')

    def get_answer_list(self):
        answer_list = []
        for dom in self.get_answer_dom_list():
            self.answer_parser.set_dom(dom)
            answer_list.append(self.answer_parser.get_info())
        return answer_list

    def get_question_dom_list(self):
        return self.dom.select('div.zm-item')

    def get_question_info_list(self):
        question_info_list = []
        parser = SimpleQuestion()
        for dom in self.get_question_dom_list():
            parser.set_dom(dom)
            question_info_list.append(parser.get_info())
        return question_info_list

    def get_extra_info(self):
        """
        扩展功能：获取扩展信息
        需重载
        """
        return
