# -*- coding: utf-8 -*-


u"""
基础的测试用函数
"""

__author__ = 'yao'

import datetime



def getYesterday():
        today=datetime.date.today()
        oneday=datetime.timedelta(days=1)
        yesterday=today-oneday
        return yesterday

def getToday():
    return datetime.date.today()

TODAY = getToday().isoformat()
YESTERDAY = getYesterday().isoformat()


