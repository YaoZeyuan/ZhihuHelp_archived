# -*- coding: utf-8 -*-
from src.lib.zhihu_parser.tools.parser_tools import ParserTools
from src.tools.debug import Debug


class TopicInfo(ParserTools):
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
        self.parse_title()
        self.parse_topic_id()
        self.parse_logo()
        self.parse_follower()
        self.parse_description()
        return self.info

    def parse_title(self):
        title = self.dom.select('#zh-topic-title h1.zm-editable-content')
        if not title:
            Debug.logger.debug(u'话题标题未找到')
            return
        self.info['title'] = title[0].get_text()
        return

    def parse_topic_id(self):
        topic = self.dom.select('link[rel="canonical"]')
        if not topic:
            Debug.logger.debug(u'话题id未找到')
            return
        href = self.get_attr(topic[0], 'href')
        self.info['topic_id'] = self.match_topic_id(href)
        return

    def parse_logo(self):
        logo = self.dom.select('img.zm-avatar-editor-preview')
        if not logo:
            Debug.logger.debug(u'话题图标未找到')
            return
        self.info['logo'] = self.get_attr(logo[0], 'src')
        return

    def parse_follower(self):
        follower = self.dom.select('div.zm-topic-side-followers-info a strong')
        if not follower:
            Debug.logger.debug(u'话题关注人数未找到')
            return
        self.info['follower'] = follower[0].get_text()
        return

    def parse_description(self):
        description = self.dom.select('#zh-topic-desc div.zm-editable-content')
        if not description:
            Debug.logger.debug(u'话题描述未找到')
            return
        self.info['description'] = self.get_tag_content(description[0])
        return
