# -*- coding: utf-8 -*-
import os
from ..zhihuhelp_tools.path import Path

class EpubPath(object):
    try:
        file_path = os.path.realpath(__file__)
        base_path = os.path.dirname(file_path)
        base_path = unicode(os.path.dirname(base_path).decode('gbk'))  # 库文件位置
    except:
        base_path = os.path.abspath('.')  # 对于Mac和Linux用户，使用gbk解码反而会造成崩溃，故添加一个try-except

    work_path = base_path  # 默认以库位置作为初始工作地址
    output_path = os.path.dirname(work_path)  # 默认以工作目录的上一级为输出目录
    meta_inf_path = work_path + u'/META-INF'
    oebps_path = work_path + u'/OEBPS'
    image_path = work_path + u'/image'
    html_path = oebps_path + u'/html'
    style_path = oebps_path + u'/style'

    @staticmethod
    def set_work_path(work_path):
        EpubPath.work_path = work_path
        EpubPath.meta_inf_path = EpubPath.work_path + u'/META-INF'
        EpubPath.oebps_path = EpubPath.work_path + u'/OEBPS'
        EpubPath.image_path = EpubPath.oebps_path + u'/images'
        EpubPath.html_path = EpubPath.oebps_path + u'/html'
        EpubPath.style_path = EpubPath.oebps_path + u'/style'
        return

    @staticmethod
    def set_output_path(output_path):
        EpubPath.output_path = output_path
        return

    @staticmethod
    def init_epub_path(work_path):
        """
        设置工作地址，根据该路径进行创建文件夹，生成epub，压缩等操作
        """
        EpubPath.set_work_path(work_path)
        Path.mkdir(EpubPath.meta_inf_path)
        Path.mkdir(EpubPath.oebps_path)
        Path.chdir(EpubPath.oebps_path)
        Path.mkdir(EpubPath.html_path)
        Path.mkdir(EpubPath.image_path)
        Path.mkdir(EpubPath.style_path)
        return

    @staticmethod
    def reset_path():
        Path.chdir(EpubPath.work_path)
        return
