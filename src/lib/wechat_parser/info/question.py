# -*- coding: utf-8 -*-
from src.lib.zhihu_parser.tools.parser_tools import ParserTools
from src.tools.debug import Debug


class QuestionInfo(ParserTools):
    """
        特指single_question 和 single_answer中的内容
    """

    def __init__(self, dom=None):
        self.set_dom(dom)
        return

    def set_dom(self, dom):
        self.info = {}
        if dom:
            self.dom = dom
            self.side_dom = dom.find('div', class_='zu-main-sidebar')
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        self.parse_base_info()
        self.parse_status_info()
        return self.info

    def parse_base_info(self):
        self.parse_question_id()
        self.parse_title()
        self.parse_description()
        self.parse_comment_count()
        return

    def parse_question_id(self):
        meta = self.dom.select('meta[http-equiv="mobile-agent"]')
        if not meta:
            Debug.logger.debug(u'问题ID未找到')
            return
        content = self.get_attr(meta[0], 'content', 0)
        self.info['question_id'] = self.match_question_id(content)
        return

    def parse_title(self):
        title = self.dom.select('#zh-question-title h2')
        if not title:
            Debug.logger.debug(u'问题标题未找到')
            return
        self.info['title'] = title[0].get_text()
        return

    def parse_description(self):
        description = self.dom.select('#zh-question-detail div.zm-editable-content')
        if not description:
            Debug.logger.debug(u'问题描述未找到')
            return
        self.info['description'] = self.get_tag_content(description[0])
        return

    def parse_comment_count(self):
        comment = self.dom.select('#zh-question-meta-wrap a[name="addcomment"]')
        if not comment:
            Debug.logger.debug(u'问题评论数未找到')
            return
        self.info['comment'] = self.match_int(comment[0].get_text())
        return

    def parse_status_info(self):
        self.parse_views()
        self.parse_followers_count()
        return

    def parse_followers_count(self):
        followers_count = self.side_dom.select('div.zh-question-followers-sidebar div.zg-gray-normal strong')
        if followers_count:
            self.info['followers'] = self.match_int(followers_count[0].get_text())
        return

    def parse_views(self):
        div = self.side_dom.find_all('div', class_='zm-side-section')[-1]
        views = div.find('strong')  # 在最后一个side-section中的第一个strong是问题浏览次数
        self.info['views'] = self.match_int(views.get_text())
        return

    def parse_answer_count(self):
        self.info['answers'] = 0  # 默认为0
        count = self.dom.select('#zh-answers-title a.zg-link-litblue, #zh-question-answer-num')
        if count:
            self.info['answers'] = self.match_int(count[0].get_text())
        return
