# -*- coding: utf-8 -*-
from src.lib.zhihu_parser.content.author import Author
from src.lib.zhihu_parser.tools.parser_tools import ParserTools
from src.tools.debug import Debug


class Answer(ParserTools):
    def __init__(self, dom=None):
        self.set_dom(dom)
        self.author_parser = Author()
        return

    @staticmethod
    def answer_is_hidden(dom):
        # 第二条是为了处理当答案已消失时，直呼仍然将问题显示出来的bug
        return dom.select('div.answer-status') or (not dom.select('textarea.content,div.zm-editable-content'))

    def set_dom(self, dom):
        self.info = {}
        if dom and not (dom.select('div.answer-status')):
            self.header = dom.find('div', class_='zm-item-vote-info')
            self.body = dom.find('div', class_='zm-editable-content')
            self.footer = dom.find('div', class_='zm-meta-panel')
            self.author_parser.set_dom(dom)
        return

    def get_info(self):
        answer_info = self.parse_info()
        author_info = self.author_parser.get_info()
        return dict(answer_info, **author_info)

    def parse_info(self):
        self.parse_header_info()
        self.parse_answer_content()
        self.parse_footer_info()
        return self.info

    def parse_header_info(self):
        self.parse_vote_count()
        return

    def parse_footer_info(self):
        self.parse_date_info()
        self.parse_comment_count()
        self.parse_no_record_flag()
        self.parse_href_info()
        return

    def parse_vote_count(self):
        if not self.header:
            Debug.logger.debug(u'答案赞同数未找到')
            return
        self.info['agree'] = self.get_attr(self.header, 'data-votecount')
        return

    def parse_answer_content(self):
        if not self.body:
            Debug.logger.debug(u'答案内容未找到')
            return
        self.info['content'] = self.get_tag_content(self.body)
        return

    def parse_date_info(self):
        data_block = self.footer.find('a', class_='answer-date-link')
        commit_date = self.get_attr(data_block, 'data-tip')
        if not data_block:
            Debug.logger.debug(u'答案更新日期未找到')
            return

        if commit_date:
            update_date = data_block.get_text()
            self.info['edit_date'] = self.parse_date(update_date)
            self.info['commit_date'] = self.parse_date(commit_date)
        else:
            commit_date = data_block.get_text()
            self.info['edit_date'] = self.info['commit_date'] = self.parse_date(commit_date)

    def parse_comment_count(self):
        # BS的属性选择器语法区分“和’！！！
        # 还好知乎所有的属性都是双引号- -
        # 看看人家这软件工程做的！
        comment = self.footer.select('a[name="addcomment"]')
        if not comment:
            Debug.logger.debug(u'评论数未找到')
            return
        self.info['comment'] = self.match_int(comment[0].get_text())
        return

    def parse_no_record_flag(self):
        no_record_flag = self.footer.find('a', class_='copyright')
        if not no_record_flag:
            Debug.logger.debug(u'禁止转载标志未找到')
            return
        self.info['no_record_flag'] = int(u'禁止转载' in no_record_flag.get_text())
        return

    def parse_href_info(self):
        href_tag = self.footer.find('a', class_='answer-date-link')
        if not href_tag:
            Debug.logger.debug(u'问题id，答案id未找到')
            return
        href = self.get_attr(href_tag, 'href')
        self.parse_question_id(href)
        self.parse_answer_id(href)
        self.info['href'] = "https://www.zhihu.com/question/{question_id}/answer/{answer_id}".format(**self.info)
        return

    def parse_question_id(self, href):
        self.info['question_id'] = self.match_question_id(href)
        return

    def parse_answer_id(self, href):
        self.info['answer_id'] = self.match_answer_id(href)
        return
