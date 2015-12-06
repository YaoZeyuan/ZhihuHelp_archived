# -*- coding: utf-8 -*-


class QuestionParser(BaseParser):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')
        self.answer_parser = Answer()

    def get_question_info_list(self):
        parser = QuestionInfo()
        parser.set_dom(self.dom)
        return [parser.get_info()]
