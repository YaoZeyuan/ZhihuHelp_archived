# -*- coding: utf-8 -*-
import hashlib
import os.path

from src.tools.config import Config
from src.tools.controler import Control
from src.tools.debug import Debug
from src.tools.extra_tools import ExtraTools
from src.tools.http import Http


class ImageContainer(object):
    def __init__(self, save_path=''):
        self.save_path = save_path
        self.container = {}
        self.md5 = hashlib.md5()
        return

    def set_save_path(self, save_path):
        self.save_path = save_path
        return

    def add(self, href):
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

        if os.path.isfile(self.save_path + '/' + filename):
            return
        Debug.print_in_single_line(u'开始下载图片{}'.format(href))
        content = Http.get_content(url=href, timeout=Config.timeout_download_picture)
        if not content:
            return
        with open(self.save_path + '/' + filename, 'wb') as image:
            image.write(content)
        return

    def start_download(self):
        argv = {'func': self.download,  # 所有待存入数据库中的数据都应当是list
                'iterable': self.container, }
        Control.control_center(argv, self.container)
        return

    def create_image(self, href):
        image = {'filename': self.create_filename(href), 'href': href}
        return image

    def create_filename(self, href):
        filename = ExtraTools.md5(href) + '.jpg'
        return filename
