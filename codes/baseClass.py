# -*- coding: utf-8 -*-
import os
import sys
import traceback
import logging
import logging.handlers


class BaseClass(object):
    u'''
    用于存放常用函数
    '''
    handler = logging.StreamHandler()  # 实例化handler
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler.setFormatter(formatter)  # 为handler添加formatter

    logger = logging.getLogger('main')  # 获取名为main的logger
    logger.addHandler(handler)  # 为logger添加handler
    #logger.setLevel(logging.INFO)  # 发布时关闭log输出
    logger.setLevel(logging.DEBUG)  # debug模式

    base_path = './'  # 初始地址

    # 辅助函数
    @staticmethod
    def printInOneLine(text=''):  # Pass
        u"""
            *   功能
                *   反复在一行内输出内容
                *   输出前会先将光标移至行首，输出完毕后不换行
            *   输入
                *   待输出字符
            *   返回
                *  无
         """
        try:
            sys.stdout.write("\r" + " " * 60 + '\r')
            sys.stdout.flush()
            sys.stdout.write(text)
            sys.stdout.flush()
        except:
            pass
        return

    @staticmethod
    def printDict(data={}, key='', prefix=''):
        try:
            if isinstance(data, dict):
                for key in data:
                    BaseClass.printDict(data[key], key, prefix + '   ')
            else:
                if isinstance(data, basestring):
                    print prefix + unicode(key) + ' => ' + data
                else:
                    print prefix + unicode(key) + ' => ' + unicode(data)
        except UnicodeEncodeError as error:
            BaseClass.logger.info(u'printDict中编码异常')
            BaseClass.logger.info(u'系统默认编码为：' + sys.getdefaultencoding())
            raise error
        return

    @staticmethod
    def reset_dir():
        BaseClass.change_dir(BaseClass.base_path)
        return

    @staticmethod
    def printCurrentDir():
        print os.path.realpath('.')
        return

    @staticmethod
    def make_dir(path):
        try:
            os.mkdir(path)
        except OSError:
            print u'指定目录已存在'
        return

    @staticmethod
    def change_dir(path):
        try:
            os.chdir(path)
        except OSError:
            print u'指定目录不存在，自动创建之'
            BaseClass.make_dir(path)
            os.chdir(path)
        return

    @staticmethod
    def init_path():
        BaseClass.reset_dir()
        BaseClass.make_dir(BaseClass.base_path + u'/知乎助手生成的电子书')
        BaseClass.make_dir(u'./知乎电子书临时资源库')
        BaseClass.change_dir(u'./知乎电子书临时资源库')
        BaseClass.make_dir(u'./知乎网页池')
        BaseClass.make_dir(u'./知乎图片池')
        BaseClass.reset_dir()
        return

    @staticmethod
    def get_time():
        return time.time()


class TypeClass(object):
    article_type = ['article', 'column', ]
    question_type = ['answer', 'question', 'author', 'collection', 'topic', ]
    type_list = question_type + article_type  # 文章必须放在专栏之前（否则检测类别的时候就一律检测为专栏了）
    info_table = {'column': 'column_info', 'author': 'author_info', 'collection': 'collection_info',
        'topic': 'topic_info', }
    pass

class SettingClass(object):
    u"""
    用于储存、获取设置值、全局变量值
    """
    # 全局变量

    # 默认数据库名称
    dataBaseFileName = u'./zhihuDB_173.db'

    UPDATETIME = '2015-11-21'  # 更新日期

    ACCOUNT = 'mengqingxue2014@qq.com'  # 默认账号密码
    PASSWORD = '131724qingxue'  #
    REMEMBERACCOUNT = False  # 是否使用已有密码
    MAXTHREAD = 10  # 最大线程数
    PICQUALITY = 1  # 图片质量（0/1/2，无图/标清/原图）
    MAXQUESTION = 100  # 每本电子书中最多可以放多少个问题
    MAXANSWER = 600  # 每本电子书中最多可以放多少个回答
    MAXARTICLE = 600  # 每本电子书中最多可以放多少篇文章
    MAXTRY = 5  # 最大尝试次数
    ANSWERORDERBY = 'agree_count'  # 答案排序原则  agree_count|update_date|char_count|
    ANSWERORDERBYDESC = True  # 答案排序顺序->是否为desc
    QUESTIONORDERBY = 'agree_count'  # 问题排序原则  agree_count|char_count|answer_count
    QUESTIONORDERBYDESC = True  # 问题排序顺序->是否为desc
    ARTICLEORDERBY = 'update_date'  # 文章排序原则  update_date|update_date|char_count
    ARTICLEORDERBYDESC = True  # 文章排序顺序->是否为desc
    THREADMODE = False  # 线程模式：为False时所有任务均在主线程上执行，用于调试错误
    PRIVATE = True
    WAITFOR_PIC = 10
    WAITFOR_HTML = 5

class SqlClass(object):
    u'''
    用于存放常用的sql代码
    '''
    cursor = None
    conn = None

    @staticmethod
    def set_conn(conn):
        SqlClass.conn = conn
        SqlClass.cursor = conn.cursor()
        return

    @staticmethod
    def save2DB(data={}, table_name=''):
        sql = "replace into {table_name} ({columns}) values ({items})".format(table_name=table_name,
                                                                              columns=','.join(data.keys()),
                                                                              items=(',?' * len(data.keys()))[1:])
        # BaseClass.logger.debug(sql)
        SqlClass.cursor.execute(sql, tuple(data.values()))
        return

    @staticmethod
    def commit():
        SqlClass.conn.commit()
        return

    @staticmethod
    def get_result_list(sql):
        BaseClass.logger.debug(sql)
        result = SqlClass.cursor.execute(sql).fetchall()
        return result

    @staticmethod
    def get_result(sql):
        result = SqlClass.cursor.execute(sql).fetchone()
        return result

    @staticmethod
    def wrap(kind, result=()):
        u"""
        将s筛选出的列表按SQL名组装为字典对象
        """
        template = {'answer': (
        'author_id', 'author_sign', 'author_logo', 'author_name', 'agree', 'content', 'question_id', 'answer_id',
        'commit_date', 'edit_date', 'comment', 'no_record_flag', 'href',),
            'question': ('question_id', 'comment', 'views', 'answers', 'followers', 'title', 'description',),
            'collection_index': ('collection_id', 'href',), 'topic_index': ('topic_id', 'href',), 'author_info': (
            'logo', 'author_id', 'hash', 'sign', 'description', 'name', 'asks', 'answers', 'posts', 'collections',
            'logs', 'agree', 'thanks', 'collected', 'shared', 'followee', 'follower', 'followed_column',
            'followed_topic', 'viewed', 'gender', 'weibo',),
            'collection_info': ('collection_id', 'title', 'description', 'follower', 'comment',),
            'topic_info': ('title', 'logo', 'description', 'topic_id', 'follower',), 'column_info': (
            'creator_id', 'creator_hash', 'creator_sign', 'creator_name', 'creator_logo', 'column_id', 'name', 'logo',
            'description', 'article', 'follower',), 'article_info': (
            'author_id', 'author_hash', 'author_sign', 'author_name', 'author_logo', 'column_id', 'name', 'article_id',
            'href', 'title', 'title_image', 'content', 'comment', 'agree', 'publish_date',), }
        return {k: v for (k, v) in zip(template[kind], result)}

import urllib2
import urllib
import socket  # 用于捕获超时错误
import zlib

import cookielib #用于生成cookie
import time


class HttpBaseClass(object):
    u'''
    用于存放常用Http函数
    '''

    @staticmethod
    def get_http_content(url='', data=None, timeout=5, extra_header={}):
        u"""获取网页内容
     
        获取网页内容, 打开网页超过设定的超时时间则报错
        
        参数:
            url         一个字符串,待打开的网址
            extraHeader 一个简单字典,需要添加的http头信息
            data        需传输的数据,默认为空
            timeout     int格式的秒数，打开网页超过这个时间将直接退出，停止等待
        返回:
            pageContent 打开成功时返回页面内容，字符串或二进制数据|失败则返回空字符串
        报错:
            IOError     当解压缩页面失败时报错
        """
        if data:
            data = urllib.urlencode(data)
        request = urllib2.Request(url=url, data=data)
        for key in extra_header:
            request.add_header(key, extra_header[key])

        response = None
        try:
            response = urllib2.urlopen(request, timeout=timeout)
        except urllib2.HTTPError as error:
            BaseClass.logger.info(u'网页打开失败')
            BaseClass.logger.info(u'错误页面:{}'.format(url))
            BaseClass.logger.info(u'失败代码:{}'.format(error.code))
            BaseClass.logger.info(u'错误原因:{}'.format(error.reason))
        except urllib2.URLError as error:
            BaseClass.logger.info(u'网络连接异常')
            BaseClass.logger.info(u'错误页面:{}'.format(url))
            BaseClass.logger.info(u'错误原因:{}'.format(error.reason))
        except socket.timeout as error:
            BaseClass.logger.info(u'打开网页超时')
            BaseClass.logger.info(u'超时页面:{}'.format(url))
        except:
            BaseClass.logger.info(u'未知错误')
            BaseClass.logger.info(u'错误页面:{}'.format(url))
            BaseClass.logger.info(u'错误堆栈信息:{}'.format(traceback.format_exc()))

        return HttpBaseClass.unpack_response(response)

    @staticmethod
    def unpack_response(response):
        if not response:
            return ''

        try:
            content = response.read()
        except socket.timeout as error:
            BaseClass.logger.info(u'打开网页超时')
            BaseClass.logger.info(u'超时页面:{}'.format())
            return ''

        decode = response.info().get(u"Content-Encoding")
        if decode and u"gzip" in decode:
            content = HttpBaseClass.ungzip(content)
        return content

    @staticmethod
    def ungzip(content):
        try:
            content = zlib.decompress(content, 16 + zlib.MAX_WBITS)
        except zlib.error as error:
            BaseClass.logger.info(u'解压出错')
            BaseClass.logger.info(u'错误信息:{}'.format(error))
            return ''
        return content

    @staticmethod
    def set_cookie(account=''):
        def load_cookie(cookieJar, cookie):
            filename = u'./theFileNameIsSoLongThatYouWontKnowWhatIsThat.txt'
            f = open(filename, 'w')
            f.write(cookie)
            f.close()
            cookieJar.load(filename)
            os.remove(filename)
            return

        jar = cookielib.LWPCookieJar()
        if account:
            result = SqlClass.cursor.execute(
                "select cookieStr, recordDate from LoginRecord order by recordDate desc where account = `{}`".format(
                    account))
        else:
            result = SqlClass.cursor.execute(
                "select cookieStr, recordDate from LoginRecord order by recordDate desc")

        result = result.fetchone()
        cookie = result[0]
        load_cookie(jar, cookie)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        urllib2.install_opener(opener)
        return

    @staticmethod
    def make_cookie(name, value, domain):
        cookie = cookielib.Cookie(version=0, name=name, value=value, port=None, port_specified=False, domain=domain,
                                  domain_specified=True, domain_initial_dot=False, path="/", path_specified=True,
                                  secure=False, expires=time.time() + 300000000, discard=False, comment=None,
                                  comment_url=None, rest={})
        return cookie


