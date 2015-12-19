# -*- coding: utf-8 -*-
from .tools.epub_config import EpubConfig
from .tools.epub_path import EpubPath

from .zhihuhelp_tools.path import Path


class INF(object):
    def __init__(self):
        return

    @staticmethod
    def add_container():
        Path.copy(EpubConfig.container_uri, EpubPath.meta_inf_path)
        return

    @staticmethod
    def add_duokan_ext():
        Path.copy(EpubConfig.duokan_container_uri, EpubPath.meta_inf_path)
        return
