# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools

class WechatColumnParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')

    def get_column_info(self):
        data = {}
        title_dom = self.dom.select('div.topic_name_editor h1.inline span')[0]
        data['title'] = title_dom.get_text()

        data['article_count'] = 0
        data['follower_count'] = 0
        data['description'] = ''
        data['image_url'] = ''

        return data

class WechatArticleParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')

    def get_article_info(self):
        data = {}
        try:
            title =  self.dom.select('div#page-content h2.rich_media_title')
            if len(title) == 0:
                return []
            data['title'] = title[0].get_text()
            content_dom = self.dom.select('div#page-content div.rich_media_content')[0]
            data['content'] = self.get_tag_content(content_dom)

            data['updated_time'] = 0
            data['voteup_count'] = 0
            data['image_url'] = ''
            data['comment_count'] = 0
            data['author_id'] = 'meng-qing-xue-81'
            data['author_name'] = '知乎助手'
            data['author_headline'] = '微信魔改版'
            data['author_avatar_url'] = 'https://pic4.zhimg.com/v2-38a89e42b40baa7d26d99cab9a451623_xl.jpg'
            data['author_gender'] = '0'
        except Exception:
            return []

        return data
