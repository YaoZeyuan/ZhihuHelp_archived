# -*- coding: utf-8 -*-
import os
import shutil
from src.tools.path import Path


class EpubPath(object):
    try:
        base_path = unicode(os.path.abspath('.').decode('gbk'))  # 初始地址,不含分隔符
    except:
        base_path = os.path.abspath('.') #对于Mac和Linux用户，使用gbk解码反而会造成崩溃，故添加一个try-except，以防万一

    meta_inf_path = base_path + '/META-INF'
    oebps_path = base_path + '/OEBPS'
    image_path = oebps_path + '/image'
    html_path = oebps_path + '/html'
    style_path = oebps_path + '/style'


    @staticmethod
    def set_base_path(base_path):
        EpubPath.base_path = base_path
        EpubPath.meta_inf_path = EpubPath.base_path + '/META-INF'
        EpubPath.oebps_path = EpubPath.base_path + '/OEBPS'
        EpubPath.image_path = EpubPath.oebps_path + '/image'
        EpubPath.html_path = EpubPath.oebps_path + '/html'
        EpubPath.style_path = EpubPath.oebps_path + '/style'

    @staticmethod
    def init_epub_path(base_path):
        EpubPath.set_base_path(base_path)
        Path.mkdir(EpubPath.meta_inf_path)
        Path.mkdir(EpubPath.oebps_path)
        Path.chdir(EpubPath.oebps_path)
        Path.mkdir(EpubPath.html_path)
        Path.mkdir(EpubPath.image_path)
        Path.mkdir(EpubPath.style_path)

    @staticmethod
    def reset_path():
        Path.chdir(EpubPath.base_path)
        return