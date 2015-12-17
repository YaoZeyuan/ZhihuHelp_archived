# -*- coding: utf-8 -*-
from src.lib.zhihu_parser.tools.parser_tools import ParserTools
from src.tools.debug import Debug


class CollectionInfo(ParserTools):
    u"""
    只解析收藏夹相关信息，暂时不解析创建者相关的信息
    """

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
        self.parse_collection_id()
        self.parse_follower()
        self.parse_description()
        self.parse_comment_count()
        return self.info

    def parse_title(self):
        title = self.dom.select('h2#zh-fav-head-title')
        if not title:
            Debug.logger.debug(u'收藏夹标题未找到')
            return
        self.info['title'] = title[0].get_text()
        return

    def parse_collection_id(self):
        topic = self.dom.select('meta[http-equiv="mobile-agent"]')
        if not topic:
            Debug.logger.debug(u'收藏夹id未找到')
            return
        href = self.get_attr(topic[0], 'content')
        self.info['collection_id'] = self.match_collection_id(href)
        return

    def parse_follower(self):
        follower = self.dom.select(
            'div.zm-side-section div.zm-side-section-inner div.zg-gray-normal a[href*="followers"]')
        if not follower:
            Debug.logger.debug(u'收藏夹关注人数未找到')
            return
        self.info['follower'] = follower[0].get_text()
        return

    def parse_description(self):
        description = self.dom.select('#zh-fav-head-description-source')
        if not description:
            Debug.logger.debug(u'收藏夹描述未找到')
            return
        self.info['description'] = self.get_tag_content(description[0])
        return

    def parse_comment_count(self):
        comment = self.dom.select('#zh-list-meta-wrap  a[name="addcomment"]')
        if not comment:
            Debug.logger.debug(u'收藏夹评论数未找到')
            return
        self.info['comment'] = self.match_int(comment[0].get_text())
        return
