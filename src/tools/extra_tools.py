# -*- coding: utf-8 -*-
import hashlib
import time
import datetime


class ExtraTools(object):
    @staticmethod
    def get_time():
        return str(time.time()).split('.')[0]

    @staticmethod
    def get_friendly_time():
        return datetime.datetime.today().isoformat().split('.')[0].replace(':', '：')

    @staticmethod
    def get_today():
        return datetime.date.today().isoformat()

    @staticmethod
    def get_yesterday():
        today = datetime.date.today()
        one = datetime.timedelta(days=1)
        yesterday = today - one
        return yesterday.isoformat()

    @staticmethod
    def md5(content):
        encrypt = hashlib.md5()
        encrypt.update(str(content))
        return encrypt.hexdigest()
