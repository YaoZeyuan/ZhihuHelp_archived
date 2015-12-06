# -*- coding: utf-8 -*-
import hashlib
import time
import datetime


class ExtraTools(object):
    encrypt = hashlib.md5()

    @staticmethod
    def get_time():
        return str(time.time()).split('.')[0]

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
        ExtraTools.encrypt.update(str(content))
        return ExtraTools.encrypt.hexdigest()

    @staticmethod
    def fix_filename(filename):
        illegal = {
            '\\': '＼',
            '/': '',
            ':': '：',
            '*': '＊',
            '?': '？',
            '<': '《',
            '>': '》',
            '|': '｜',
            '"': '〃',
            '!': '！',
            '\n': ''
        }
        for key,value in illegal.items():
            filename = filename.replace(key, value)
        return filename

