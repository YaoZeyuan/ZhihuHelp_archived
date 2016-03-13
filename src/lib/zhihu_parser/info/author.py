# -*- coding: utf-8 -*-
from src.lib.zhihu_parser.tools.parser_tools import ParserTools
from src.tools.debug import Debug


class AuthorInfo(ParserTools):
    u"""
    使用详情页面进行解析
    """

    def __init__(self, dom=None):
        self.set_dom(dom)
        return

    def set_dom(self, dom):
        self.info = {}
        if dom:
            self.dom = dom
            self.header_dom = dom.find('div', class_='zm-profile-header')
            self.detail_dom = dom.find('div', class_='zm-profile-details-wrap')
            self.side_dom = dom.find('div', class_='zu-main-sidebar')
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        self.parse_base_info()
        self.parse_detail_info()
        self.parse_extra_info()
        return self.info

    def parse_base_info(self):
        self.parse_author_id()
        self.parse_author_hash()
        self.parse_name()
        self.parse_sign()
        self.parse_logo()
        self.parse_description()
        self.parse_weibo()
        self.parse_gender()
        self.parse_profile_count()
        return

    def parse_name(self):
        name = self.dom.select('div.title-section a.name')
        if not name:
            Debug.logger.debug(u'用户名未找到')
            return
        self.info['name'] = name[0].get_text()
        return

    def parse_weibo(self):
        weibo = self.header_dom.select('a.zm-profile-header-user-weibo')
        if not weibo:
            Debug.logger.debug(u'用户微博未找到')
            return
        self.info['weibo'] = self.get_attr(weibo[0], 'href')
        return

    def parse_sign(self):
        sign = self.dom.select('div.title-section span[title]')
        if not sign:
            Debug.logger.debug(u'用户签名未找到')
            return
        self.info['sign'] = self.get_attr(sign[0], 'title')
        return

    def parse_logo(self):
        logo = self.header_dom.select('div.zm-profile-header-avatar-container img.avatar')
        if not logo:
            Debug.logger.debug(u'用户头像未找到')
            return
        self.info['logo'] = self.get_attr(logo[0], 'src')
        return

    def parse_gender(self):
        gender = self.header_dom.select('span.edit-wrap input[checked="checked"]')
        if not gender:
            Debug.logger.debug(u'用户性别未找到')
            return
        self.info['gender'] = self.get_attr(gender[0], 'class')[0]  # class为多值属性，返回数据为一个列表，所以需要进行特殊处理
        return

    def parse_author_id(self):
        item = self.header_dom.select('div.profile-navbar a.item')
        if not item:
            Debug.logger.debug(u'用户id未找到')
            return
        href = self.get_attr(item[0], 'href')
        self.info['author_id'] = self.match_author_id(href)
        return

    def parse_author_hash(self):
        hash = self.dom.select('script[data-name="current_people"]')
        if not hash:
            Debug.logger.debug(u'用户hash未找到')
            return
        hash = hash[0].get_text().split(',')[-1]  # 取出hash所在字符串
        self.info['hash'] = hash.split('"')[1]  # 取出hash值
        return

    def parse_profile_count(self):
        def parse_items(root=None, kind='asks'):
            node = root.select('a[href*="{}"] > span.num'.format(kind))
            if not node:
                Debug.logger.debug(u'{}未找到'.format(kind))
                return
            self.info[kind] = self.match_int(node[0].get_text())
            return

        item_list = ['asks', 'answers', 'posts', 'collections', 'logs']
        div = self.header_dom.select('div.profile-navbar')
        if not div:
            Debug.logger.debug(u'用户提问-回答-专栏数未找到')
            return
        for item in item_list:
            parse_items(div[0], item)
        return

    def parse_detail_info(self):
        detail_items = ['agree', 'thanks', 'collected', 'shared']
        detail = self.detail_dom.select('.zm-profile-module-desc span strong')
        if not detail:
            Debug.logger.debug(u'用户赞同-感谢-被收藏数未找到')
            return
        for i in range(len(detail)):
            self.info[detail_items[i]] = self.match_int(detail[i])
        return

    def parse_description(self):
        description = self.header_dom.select('.description span.content')
        if not description:
            Debug.logger.debug(u'用户详情未找到')
            return
        self.info['description'] = self.get_tag_content(description[0])
        return

    def parse_extra_info(self):
        self.parse_followee()
        self.parse_follower()
        self.parse_followed_column()
        self.parse_followed_topic()
        self.parser_views()
        return

    def parse_followee(self):
        followee = self.side_dom.select('div.zm-profile-side-following a[href*="followees"] strong')
        if not followee:
            Debug.logger.debug(u'用户关注数未找到')
            return
        self.info['followee'] = followee[0].get_text()
        return

    def parse_follower(self):
        follower = self.side_dom.select('div.zm-profile-side-following a[href*="followers"] strong')
        if not follower:
            Debug.logger.debug(u'用户粉丝数未找到')
            return
        self.info['follower'] = follower[0].get_text()
        return

    def parse_followed_column(self):
        column = self.side_dom.select('.zm-profile-side-section-title a[href*="columns"] strong')
        if not column:
            Debug.logger.debug(u'用户关注专栏数未找到')
            return
        self.info['followed_column'] = self.match_int(column[0].get_text())
        return

    def parse_followed_topic(self):
        topic = self.side_dom.select('.zm-profile-side-section-title a[href*="topics"] strong')
        if not topic:
            Debug.logger.debug(u'用户关注话题数未找到')
            return
        self.info['followed_topic'] = self.match_int(topic[0].get_text())
        return

    def parser_views(self):
        views = self.side_dom.select('.zm-profile-side-section .zm-side-section-inner span.zg-gray-normal strong')
        if not views:
            Debug.logger.debug(u'用户被浏览数未找到')
            return
        self.info['viewed'] = views[0].get_text()
        return
