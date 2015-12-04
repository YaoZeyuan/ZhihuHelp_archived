# -*- coding: utf-8 -*-
class Config(object):
    u"""
    用于储存、获取设置值、全局变量值
    """
    # 全局变量
    database_filename = u'./zhihuDB_173.db'  # 默认数据库名称

    update_time = '2015-11-21'  # 更新日期

    account = 'mengqingxue2014@qq.com'  # 默认账号密码
    password = '131724qingxue'  #
    remember_account = False  # 是否使用已有密码
    max_thread = 10  # 最大线程数
    picture_quality = 1  # 图片质量（0/1/2，无图/标清/原图）
    max_question = 100  # 每本电子书中最多可以放多少个问题
    max_answer = 600  # 每本电子书中最多可以放多少个回答
    max_article = 600  # 每本电子书中最多可以放多少篇文章
    max_try = 5  # 最大尝试次数
    answer_order_by = 'agree_count'  # 答案排序原则  agree_count|update_date|char_count|
    answer_order_by_desc = True  # 答案排序顺序->是否为desc
    question_order_by = 'agree_count'  # 问题排序原则  agree_count|char_count|answer_count
    question_order_by_desc = True  # 问题排序顺序->是否为desc
    article_order_by = 'update_date'  # 文章排序原则  update_date|update_date|char_count
    article_order_by_desc = True  # 文章排序顺序->是否为desc
    show_private_answer = True
    timeout_download_picture = 10
    timeout_download_html = 5
