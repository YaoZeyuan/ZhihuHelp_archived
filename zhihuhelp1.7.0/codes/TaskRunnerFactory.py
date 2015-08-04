# -*- coding: utf-8 -*-
import re
from worker import *

__author__ = 'yao'

u"""
利用工厂函数，将对不同任务的处理分散到多个类中去
使用托管模式
"""


from baseClass import *

class TaskRunner(BaseClass):
    u"""
    Task基础类，用于分线程执行抓取任务
    """
    def __init__(self, taskList):
        self.taskList = taskList
        self.maxThread = SettingClass.MAXTHREAD;
        self.initProperty()
        return

    def initProperty(self):
        u"""
        初始化各种属性
        """
        self.maxThread = 1
        return

    def urlInfoFactory(self, task):
        u"""
        依于此对每个task创建对应urlInfo，以便执行
        """
        urlInfo = {}
        return urlInfo

    def run(self):
        return

    def getResult(self):
        return

class AnswerTaskRunner(TaskRunner):
    def initProperty(self):
        u"""
        置空则按预设的最大线程数MAXTHREAD并发执行
        """
        return

    def urlInfoFactory(self, baseUrl):
        urlInfo = {}
        urlInfo['questionID']   = re.search(r'(?<=zhihu\.com/question/)\d{8}', baseUrl).group(0)
        urlInfo['answerID']     = re.search(r'(?<=zhihu\.com/question/\d{8}/answer/)\d{8}', baseUrl).group(0)
        urlInfo['guide']        = u'成功匹配到答案地址{}，开始执行抓取任务'.format(baseUrl)
        urlInfo['worker']       = AnswerWorker(conn = self.conn, urlInfo = urlInfo)
        urlInfo['filter']       = AnswerFilter(self.cursor, urlInfo)
        urlInfo['infoUrl']      = ''
        return urlInfo


class TaskRunnerFactory(BaseClass):
    def __init__(self, taskList, taskKind, MaxThread):
        return

    def getResultList(self):
        return