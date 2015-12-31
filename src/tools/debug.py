# -*- coding: utf-8 -*-
import logging
import logging.handlers
import sys

from src.tools.config import Config


class Debug(object):
    u"""
    打印日志
    """
    logger = logging.getLogger('main')  # 获取名为main的logger
    if Config.debug:
        logger.setLevel(logging.DEBUG)  # debug模式
    else:
        logger.setLevel(logging.INFO)  # 发布时关闭log输出

    # 辅助函数
    @staticmethod
    def print_in_single_line(text=''):
        try:
            sys.stdout.write("\r" + " " * 60 + '\r')
            sys.stdout.flush()
            sys.stdout.write(text)
            sys.stdout.flush()
        except:
            pass
        return

    @staticmethod
    def print_dict(data={}, key='', prefix=''):
        try:
            if isinstance(data, dict):
                for key in data:
                    Debug.print_dict(data[key], key, prefix + '   ')
            else:
                if isinstance(data, basestring):
                    print prefix + unicode(key) + ' => ' + data
                else:
                    print prefix + unicode(key) + ' => ' + unicode(data)
        except UnicodeEncodeError as error:
            Debug.logger.info(u'编码异常')
            Debug.logger.info(u'系统默认编码为：' + sys.getdefaultencoding())
            # raise error
        return

    @staticmethod
    def print_config():
        Config._sync()
        Debug.print_dict(Config._config_store)
        return
