# -*- coding: utf-8 -*-
import hashlib
import os.path

from src.tools.config import Config
from src.tools.controler import Control
from src.tools.debug import Debug
from src.tools.extra_tools import ExtraTools
from src.tools.http import Http
from src.tools.match import Match
from src.tools.path import Path


class ImageContainer(object):
    def __init__(self, save_path=''):
        if len(save_path) == 0:
            save_path = Path.image_pool_path
        self.save_path = save_path
        self.container = {}
        self.md5 = hashlib.md5()
        return

    def set_save_path(self, save_path):
        self.save_path = save_path
        return

    def add(self, href):
        """
        :param href:  图片地址
        :return:
        """
        self.container[href] = self.create_image(href)
        return self.get_filename(href)

    def delete(self, href):
        del self.container[href]
        return

    def get_filename(self, href):
        image = self.container.get(href)
        if image:
            return image['filename']
        return ''

    def get_filename_list(self):
        return self.container.values()

    def download(self, index):
        image = self.container[index]
        filename = image['filename']
        href = image['href']
        #   下载图片时自动把https换成http，以便加速图片下载过程
        href = href.replace('https://', 'http://')

        if os.path.isfile(self.save_path + '/' + filename):
            return
        Debug.print_in_single_line(u'开始下载图片{}'.format(href))
        if href:
            content = Http.get_content(url=href, timeout=Config.timeout_download_picture)
            if not content:
                Debug.logger.debug(u'图片『{}』下载失败'.format(href))
                content = ''
            else:
                Debug.print_in_single_line(u'图片{}下载完成'.format(href))
        else:
            #   当下载地址为空的时候，就没必要再去下载了
            content = ''
        with open(self.save_path + '/' + filename, 'wb') as image:
            image.write(content)
        return

    def start_download(self):
        argv = {'func': self.download,  # 所有待存入数据库中的数据都应当是list
                'iterable': self.container, }
        Control.control_center(argv, self.container)
        return

    def create_image(self, href):
        #   在这里，根据图片配置对文件类别进行统一处理
        href = self.transfer_img_href_by_config_quality(href)
        image = {'filename': self.create_filename(href), 'href': href}
        return image

    def transfer_img_href_by_config_quality(self, raw_href):
        href = Match.generate_img_src(raw_href, Config.picture_quality)
        if href is None:
            href = raw_href
        return href

    def create_filename(self, href):
        filename = ExtraTools.md5(href) + '.jpg'
        return filename
