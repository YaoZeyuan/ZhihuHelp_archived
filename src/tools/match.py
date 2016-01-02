# -*- coding: utf-8 -*-
import re


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
            '\r': ''
        }
        for key, value in illegal.items():
            filename = filename.replace(key, value)
        return unicode(filename[:80])
