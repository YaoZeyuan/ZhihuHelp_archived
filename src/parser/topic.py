# -*- coding: utf-8 -*-
from src.parser.author import AuthorParser
from src.parser.info.topic import TopicInfo


class TopicParser(AuthorParser):
    def get_question_dom_list(self):
        return self.dom.select('div.content')[:-1]

    def get_answer_dom_list(self):
        return self.dom.select('div.content')[:-1]

    def get_extra_info(self):
        topic = TopicInfo(self.dom)
        return topic.get_info()
