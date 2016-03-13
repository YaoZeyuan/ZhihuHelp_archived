# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.zhihu_parser.base import BaseParser
from src.lib.zhihu_parser.content.answer import Answer
from src.lib.zhihu_parser.info.question import QuestionInfo


class QuestionParser(BaseParser):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')
        self.answer_parser = Answer()

    def get_question_info_list(self):
        parser = QuestionInfo()
        parser.set_dom(self.dom)
        return [parser.get_info()]
