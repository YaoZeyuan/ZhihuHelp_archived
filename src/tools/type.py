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
    raw = 'raw'  # 原图
    big = 'big'  # 普通
    none = 'none'  # 无图

    @staticmethod
    def generate_img_download_url(file_uri):
        """
        根据文件名，随机选择一个前缀作为图片下载地址
        :param file_uri:
        :return:
        """
        img_site_list = [
            'https://pic1.zhimg.com/'
            'https://pic2.zhimg.com/'
            'https://pic3.zhimg.com/'
            'https://pic4.zhimg.com/'
        ]
        url = random.choice(img_site_list) + file_uri
        return url
