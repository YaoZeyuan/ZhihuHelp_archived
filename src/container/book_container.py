# -*- coding: utf-8 -*-

class BookContainer(object):
    u"""
    生成书籍的容器
    负责完成:
    1.  数据规约
    2.  书籍分卷
    """

    def __init__(self):
        self.task_container_list = []
        return