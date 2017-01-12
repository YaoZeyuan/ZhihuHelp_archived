# -*- coding: utf-8 -*-
from random import random


class Type(object):
    #   未知类型
    unknown = 'unknown'

    answer = 'answer'
    question = 'question'
    topic = 'topic'
    collection = 'collection'
    author = 'author'
    column = 'column'
    article = 'article'

    pass


class ImgQuality(object):
    raw = 2  # 原图
    big = 1  # 普通
    none = 0  # 无图

    @staticmethod
    def add_random_download_address_header_for_img_filename(file_uri):
        """
        随机补充一个前缀作为图片下载地址
        :param file_uri:
        :return:
        """
        img_site_list = [
            'https://pic1.zhimg.com/',
            'https://pic2.zhimg.com/',
            'https://pic3.zhimg.com/',
            'https://pic4.zhimg.com/',
        ]
        url = img_site_list[0] + file_uri
        return url
