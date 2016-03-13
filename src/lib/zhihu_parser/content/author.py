# -*- coding: utf-8 -*-
from src.lib.zhihu_parser.tools.parser_tools import ParserTools
from src.tools.debug import Debug


class Author(ParserTools):
    """
    实践一把《代码整洁之道》的做法，以后函数尽量控制在5行之内
    """

    def __init__(self, dom=None):
        self.set_dom(dom)
        return

    def set_dom(self, dom):
        self.info = {}
        if dom:
            self.dom = dom.find('div', class_='zm-item-answer-author-info')
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        if (not self.dom.find('img')) and (not self.dom.find('a', class_='author-link')):
            self.create_anonymous_info()
        else:
            self.parse_author_info()
        return self.info

    def parse_author_info(self):
        self.parse_author_id()
        self.parse_author_sign()
        self.parse_author_logo()
        self.parse_author_name()
        return

    def create_anonymous_info(self):
        self.info['author_id'] = u"coder'sGirlFriend~"
        self.info['author_sign'] = u''
        self.info['author_logo'] = u'https://pic1.zhimg.com/da8e974dc_s.jpg'
        self.info['author_name'] = u'匿名用户'
        return

    def parse_author_id(self):
        author = self.dom.find('a', class_='zm-item-link-avatar')
        if not author:
            author = self.dom.find('a', class_='author-link')  # for collection
        if not author:
            Debug.logger.debug(u'用户ID未找到')
            return
        link = self.get_attr(author, 'href')
        self.info['author_id'] = self.match_author_id(link)
        return

    def parse_author_sign(self):
        sign = self.dom.find('strong', class_='zu-question-my-bio')
        if not sign:
            sign = self.dom.find('span', class_='bio')
        if not sign:
            Debug.logger.debug(u'用户签名未找到')
            return
        self.info['author_sign'] = self.get_attr(sign, 'title')
        return

    def parse_author_logo(self):
        self.info['author_logo'] = self.get_attr(self.dom.find('img'), 'src')
        return

    def parse_author_name(self):
        name = self.dom.find('a', class_='author-link')
        if not name:
            Debug.logger.debug(u'用户名未找到')
            return
        self.info['author_name'] = name.text
        return
