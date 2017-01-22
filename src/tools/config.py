# -*- coding: utf-8 -*-
import json
import os

from src.tools.path import Path


class Config(object):
    u"""
    用于储存、获取设置值、全局变量值
    """
    # 全局变量
    update_time = '2017-01-23'  # 更新日期

    debug = False
    debug_for_create_book = False # 是否在测试电子书生成功能，在测试的话跳过网页抓取部分
    debug_for_thread = False # 是否在测试多线程功能，在测试的话改为单线程执行

    account = 'mengqingxue@yaozeyuan.online'  # 默认账号密码, 2017年更新
    password = '912714398d'  #
    remember_account = False  # 是否使用已有密码
    max_thread = 10  # 最大线程数，其实设成5就行了，但下图片的时候还是得多开几个线程，所以还是设成10好了（反正冬天，CPU满了有利于室内保温 - -）
    picture_quality = 1  # 图片质量（0/1/2，无图/标清/原图）
    max_try = 5  # 下载图片时的最大尝试次数
    max_book_size_mb = 100  # 单个文件的最大大小(MB, 兆)，超过这个数会自动分卷
    timeout_download_picture = 10  # 多给知乎服务器点时间，批量生成tex太痛苦了- -
    timeout_download_html = 5

    article_order_by = ' order by article_id asc '  # 文章排序顺序，默认：时间顺序正序
    answer_order_by = ' order by voteup_count desc '  # 答案排序顺序，默认：赞同数降序
    topic_or_collection_answer_order_by = ' '  # 话题/收藏夹中答案排序顺序，默认：按在话题/收藏夹中的顺序排列


    @staticmethod
    def init_config():
        Config.load()
        return

    @staticmethod
    def save():
        data = {}
        with open(Path.config_path, 'w') as f:
            for key in Config.__dict__:
                value = Config.__dict__[key]
                if '__' in key[:2]:
                    #   内置属性直接跳过
                    continue
                try:
                    json.dumps(value)
                except TypeError:
                    #   暴力判断是否可被序列化←_←
                    pass
                else:
                    data[key] = value
            json.dump(data, f, indent=4)
        return

    @staticmethod
    def load():
        if not os.path.isfile(Path.config_path):
            return
        with open(Path.config_path) as f:
            config = json.load(f)
            if not config.get('remember_account'):
                # 当选择不记住密码时，跳过读取，使用默认设置
                # 不考虑用户强行在配置文件中把account改成空的情况
                return
        for (key, value) in config.items():
            setattr(Config, key, value)
        return
