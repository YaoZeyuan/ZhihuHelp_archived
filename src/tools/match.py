# -*- coding: utf-8 -*-
import re

from src.tools.type import ImgQuality


class Match(object):
    @staticmethod
    def xsrf(content=''):
        xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', content)
        if xsrf:
            return '_xsrf=' + xsrf.group(0)
        return ''

    @staticmethod
    def answer(content=''):
        return re.search(r'(?<=zhihu\.com/)question/(?P<question_id>\d{8})/answer/(?P<answer_id>\d{8})', content)

    @staticmethod
    def question(content=''):
        return re.search(r'(?<=zhihu\.com/)question/(?P<question_id>\d{8})', content)

    @staticmethod
    def author(content=''):
        return re.search(r'(?<=zhihu\.com/)people/(?P<author_id>[^/\n\r]*)', content)

    @staticmethod
    def collection(content=''):
        return re.search(r'(?<=zhihu\.com/)collection/(?P<collection_id>\d*)', content)

    @staticmethod
    def topic(content=''):
        return re.search(r'(?<=zhihu\.com/)topic/(?P<topic_id>\d*)', content)

    @staticmethod
    def article(content=''):
        return re.search(r'(?<=zhuanlan\.zhihu\.com/)(?P<column_id>[^/]*)/(?P<article_id>\d{8})', content)

    @staticmethod
    def column(content=''):
        return re.search(r'(?<=zhuanlan\.zhihu\.com/)(?P<column_id>[^/\n\r]*)', content)

    @staticmethod
    def html_body(content=''):
        return re.search('(?<=<body>).*(?=</body>)', content, re.S).group(0)

    @staticmethod
    def fix_html(content=''):
        content = content.replace('</br>', '').replace('</img>', '')
        content = content.replace('<br>', '<br/>')
        content = content.replace('href="//link.zhihu.com', 'href="https://link.zhihu.com')  # 修复跳转链接
        for item in re.findall(r'\<noscript\>.*?\</noscript\>', content, re.S):
            content = content.replace(item, '')
        return content

    @staticmethod
    def fix_filename(filename):
        illegal = {
            '\\': '＼',
            '/': '',
            ':': '：',
            '*': '＊',
            '?': '？',
            '<': '《',
            '>': '》',
            '|': '｜',
            '"': '〃',
            '!': '！',
            '\n': '',
            '\r': '',
            '&': 'and',
        }
        for key, value in illegal.items():
            filename = filename.replace(key, value)
        return unicode(filename[:80])

    @staticmethod
    def parse_img(avatar_url):
        """
        从图片地址中提取出统一的图片文件名
        格式: [图片名].[图片后缀名]
        例: abc.png
        :type avatar_url str
        :rtype: str
        """
        result = re.search(r'(?<=\.zhimg\.com/)(?P<name>[^_]*)_(?P<size>[^.]*)\.(?P<ext>.*)', avatar_url)
        filename = 'da8e974dc'  # 匿名用户默认头像
        ext = 'jpg'
        if not result:
            return filename + '.' + ext

        filename = result.group('name')
        ext = result.group('ext')
        return filename + '.' + ext

    @staticmethod
    def parse_column_img(avatar_url):
        """
        从专栏图片地址中提取出统一的图片文件名
        格式: [图片名].[图片后缀名]
        例: abc.png
        :type avatar_url str
        :rtype: str
        """
        result = re.search(r'(?<=\.zhimg\.com/50/)(?P<name>[^_]*)_(?P<size>[^.]*)\.(?P<ext>.*)', avatar_url)
        filename = 'da8e974dc'  # 匿名用户默认头像
        ext = 'jpg'
        if not result:
            return filename + '.' + ext

        filename = result.group('name')
        ext = result.group('ext')
        return filename + '.' + ext

    @staticmethod
    def generate_img_url(avatar_url, img_quality=ImgQuality.big):
        result = re.search(r'(?P<name>[^_]*)\.(?P<ext>.*)', avatar_url)
        filename = 'da8e974dc'  # 匿名用户默认头像
        ext = 'jpg'
        file_uri = filename + '.' + ext
        if not result:
            return ImgQuality.generate_img_download_url(file_uri)

        filename = result.group('name')
        ext = result.group('ext')

        if img_quality == ImgQuality.raw:
            file_uri = filename + '.' + ext
        elif img_quality == ImgQuality.big:
            file_uri = filename + '_g.' + ext
        elif img_quality == ImgQuality.none:
            return ''

        return ImgQuality.generate_img_download_url(file_uri)
