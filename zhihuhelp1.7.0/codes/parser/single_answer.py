# -*- coding: utf-8 -*-

from parserTools import BaseParser


class SingleAnswer(BaseParser):
    def get_answer_dom_list(self):
        return self.dom.find_all(_class='zm-item-answer')

    def get_answer_list(self):
        answer_list = []
        for dom in self.get_answer_dom_list():
            self.answer_parser.set_dom(dom)
            answer_list.append(self.answer_parser.get_info())
        return answer_list

    def get_question_info_list(self):
        parser = QuestionInfo()
        parser.set_dom(self.dom)
        return [parser.get_info()]


