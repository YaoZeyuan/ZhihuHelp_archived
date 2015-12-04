# -*- coding: utf-8 -*-
import os


class Path(object):
    base_path = os.path.abspath('./')  # 初始地址,不含分隔符
    html_pool_path = base_path + u'/知乎电子书临时资源库/知乎网页池'
    image_pool_path = base_path + u'/知乎电子书临时资源库/知乎图片池'

    @staticmethod
    def reset_path():
        Path.change_dir(Path.base_path)
        return

    @staticmethod
    def pwd():
        print os.path.realpath('.')
        return

    @staticmethod
    def mkdir(path):
        try:
            os.mkdir(path)
        except OSError:
            print u'指定目录已存在'
        return

    @staticmethod
    def chdir(path):
        try:
            os.chdir(path)
        except OSError:
            print u'指定目录不存在，自动创建之'
            Path.mkdir(path)
            os.chdir(path)
        return

    @staticmethod
    def init_path():
        Path.reset_path()
        Path.mkdir(u'./知乎助手生成的电子书')
        Path.mkdir(u'./知乎电子书临时资源库')
        Path.chdir(u'./知乎电子书临时资源库')
        Path.mkdir(u'./知乎网页池')
        Path.mkdir(u'./知乎图片池')
        Path.reset_path()
        return
