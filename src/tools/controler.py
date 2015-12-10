# -*- coding: utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool  # 多线程并行库

from src.tools.config import Config


class Control(object):
    thread_pool = ThreadPool(Config.max_thread)

    @staticmethod
    def control_center(argv, test_flag):
        max_try = Config.max_try
        for time in range(max_try):
            if test_flag:
                # try:
                Control.thread_pool.map(**argv)
                # except Exception:
                #    Debug.logger.info(u'多线程控制器出现异常，稍后重试')
        return
