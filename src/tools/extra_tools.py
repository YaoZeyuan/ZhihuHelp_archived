# -*- coding: utf-8 -*-
import hashlib
import time


class ExtraTools(object):
    encrypt = hashlib.md5()

    @staticmethod
    def get_time():
        return str(time.time()).split('.')[0]

    @staticmethod
    def md5(content):
        ExtraTools.encrypt.update(str(content))
        return ExtraTools.encrypt.hexdigest()
