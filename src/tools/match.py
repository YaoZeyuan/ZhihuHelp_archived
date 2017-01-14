# -*- coding: utf-8 -*-
import re

from src.tools.debug import Debug
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
        return re.search(r'(?<=zhihu\.com/)people/(?P<author_page_id>[^/\n\r]*)', content)

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
        return Match.replace_danger_char_for_filesystem(filename)[:80]

    @staticmethod
    def replace_danger_char_for_filesystem(filename):
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
        return unicode(filename)

    @staticmethod
    def generate_img_src(img_file_name ='da8e974dc.jpg', img_quality=ImgQuality.big):
        """
        生成特殊的图片地址(知乎头像/专栏信息等存在于数据库中的图片)
        :param img_file_name: 图片名
        :param img_quality: 图片质量
        :return:
        """
        result = re.search(r'(?<=zhimg.com/)(?P<name>[^_]*)[^\.]*\.(?P<ext>.*)', img_file_name)
        if not result:
            # 地址不符合规范，直接返回false
            return None

        filename = result.group('name')
        ext = result.group('ext')

        if img_quality == ImgQuality.raw:
            img_file_name = filename + '.' + ext
        elif img_quality == ImgQuality.big:
            img_file_name = filename + '_b.' + ext
        elif img_quality == ImgQuality.none:
            return ''
        else:
            Debug.logger.info('警告：图片类型设置不正确！')
            return None
        url = ImgQuality.add_random_download_address_header_for_img_filename(img_file_name)
        return url

    def fix_image(self, content):
        content = Match.fix_html(content)
        for img in re.findall(r'<img[^>]*', content):
            # fix img
            if img[-1] == '/':
                img = img[:-1]
            img += '>'

            src = re.search(r'(?<=src=").*?(?=")', img)
            if not src:
                new_image = img + '</img>'
                content = content.replace(img, new_image)
                continue
            else:
                src = src.group(0)
                if src.replace(' ', '') == '':
                    new_image = img + '</img>'
                    content = content.replace(img, new_image)
                    continue
                else:
                    new_image = '<img>'

            new_image += '</img>'
            content = content.replace(img, '<div class="duokan-image-single">{}</div>'.format(new_image))

        return content

    @staticmethod
    def match_img_with_src_dict(content):
        img_src_dict = {}
        img_list = re.findall(r'<img[^>]*', content)
        for img in img_list:
            result = re.search(r'(?<=src=").*?(?=")', img)
            if not result:
                img_src_dict[img] = ''
            else:
                src = result.group(0)
                if 'zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg' in src :
                    result = re.search(r'(?<=data-original=").*?(?=")', img)
                    img_src_dict[img] = result.group(0)
                else:
                    img_src_dict[img] = src
        return img_src_dict

    @staticmethod
    def create_img_element_with_file_name(filename):
        src = Match.create_local_img_src(filename)
        return u'<div class="duokan-image-single"><img src="{}"></img></div>'.format(src)

    @staticmethod
    def create_local_img_src(filename):
        u"""
        生成本地电子书图片地址
        :param filename:
        :return:
        """
        src = '{}'.format(u'../images/' + filename)
        return src