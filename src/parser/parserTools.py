# -*- coding: utf-8 -*-

import re
import datetime  # 简单处理时间

from bs4 import BeautifulSoup
import copy #用于复制对象（仅用了一次）
from src.tools.debug import Debug
from src.tools.extra_tools import ExtraTools






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

class AuthorParser(BaseParser):
    def get_extra_info(self):
        author = AuthorInfo(self.dom)
        return author.get_info()

class TopicParser(AuthorParser):
    def get_question_dom_list(self):
        return self.dom.select('div.content')[:-1]

    def get_answer_dom_list(self):
        return self.dom.select('div.content')[:-1]

    def get_extra_info(self):
        topic = TopicInfo(self.dom)
        return topic.get_info()

class CollectionParser(AuthorParser):
    def get_answer_dom_list(self):
        return self.dom.select('div.zm-item')

    def get_extra_info(self):
        collection = CollectionInfo(self.dom)
        return collection.get_info()

class QuestionParser(BaseParser):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')
        self.answer_parser = Answer()

    def get_question_info_list(self):
        parser = QuestionInfo()
        parser.set_dom(self.dom)
        return [parser.get_info()]