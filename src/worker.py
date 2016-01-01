# -*- coding: utf-8 -*-

import json  # 用于JsonWorker

from src.lib.zhihu_parser.author import AuthorParser
from src.lib.zhihu_parser.collection import CollectionParser
from src.lib.zhihu_parser.question import QuestionParser
from src.lib.zhihu_parser.topic import TopicParser
from src.tools.controler import Control
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match


class PageWorker(object):
    def __init__(self, task_list):
        self.task_set = set(task_list)
        self.task_complete_set = set()
        self.work_set = set()  # 待抓取网址池
        self.work_complete_set = set()  # 已完成网址池
        self.content_list = []  # 用于存放已抓取的内容
        self.answer_list = []
        self.question_list = []

        self.info_list = []
        self.extra_index_list = []
        self.info_url_set = self.task_set.copy()
        self.info_url_complete_set = set()

        self.add_property()  # 添加扩展属性
        Http.set_cookie()

    def add_property(self):

        return

    @staticmethod
    def parse_max_page(content):
        max_page = 1
        try:
            floor = content.index('">下一页</a></span>')
            floor = content.rfind('</a>', 0, floor)
            cell = content.rfind('>', 0, floor)
            max_page = int(content[cell + 1:floor])
            Debug.logger.info(u'答案列表共计{}页'.format(max_page))
        except:
            Debug.logger.info(u'答案列表共计1页')
        finally:
            return max_page

    def create_save_config(self):
        config = {'Answer': self.answer_list, 'Question': self.question_list, }
        return config

    def clear_index(self):
        u"""
        用于在collection/topic中清除原有缓存
        """
        return

    def save(self):
        self.clear_index()
        save_config = self.create_save_config()
        for key in save_config:
            for item in save_config[key]:
                if item:
                    DB.save(item, key)
        DB.commit()
        return

    def start(self):
        self.start_catch_info()
        self.start_create_work_list()
        self.start_worker()
        self.save()
        return

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        content = Http.get_content(target_url + '?nr=1&sort=created')
        if not content:
            return
        self.task_complete_set.add(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}?nr=1&sort=created&page={}'.format(target_url, page + 1)
            self.work_set.add(url)
        return

    def clear_work_set(self):
        self.work_set = set()
        return

    def start_create_work_list(self):
        self.clear_work_set()
        argv = {'func': self.create_work_set, 'iterable': self.task_set, }
        Control.control_center(argv, self.task_set)
        return

    def worker(self, target_url):
        if target_url in self.work_complete_set:
            # 自动跳过已抓取成功的网址
            return

        Debug.logger.info(u'开始抓取{}的内容'.format(target_url))
        content = Http.get_content(target_url)
        if not content:
            return
        content = Match.fix_html(content)  # 需要修正其中的<br>标签，避免爆栈
        self.content_list.append(content)
        Debug.logger.debug(u'{}的内容抓取完成'.format(target_url))
        self.work_complete_set.add(target_url)
        return

    def parse_content(self, content):
        parser = QuestionParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()
        return

    def start_worker(self):
        a = list(self.work_set)
        a.sort()
        argv = {'func': self.worker,  # 所有待存入数据库中的数据都应当是list
                'iterable': a, }
        Control.control_center(argv, self.work_set)
        Debug.logger.info(u"所有内容抓取完毕，开始对页面进行解析")
        i = 0
        for content in self.content_list:
            i += 1
            Debug.print_in_single_line(u"正在解析第{}/{}张页面".format(i, self.content_list.__len__()))
            self.parse_content(content)
        Debug.logger.info(u"网页内容解析完毕")
        return

    def catch_info(self, target_url):
        return

    def start_catch_info(self):
        argv = {'func': self.catch_info, 'iterable': self.info_url_set, }
        Control.control_center(argv, self.info_url_set)
        return

class QuestionWorker(PageWorker):
    def parse_content(self, content):
        parser = QuestionParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()
        return


class AuthorWorker(PageWorker):
    def parse_content(self, content):
        parser = AuthorParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()
        return

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        content = Http.get_content(target_url + '/answers?order_by=vote_num')
        if not content:
            return
        self.task_complete_set.add(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}/answers?order_by=vote_num&page={}'.format(target_url, page + 1)
            self.work_set.add(url)
        return

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        content = Http.get_content(target_url + '/about')
        if not content:
            return
        self.info_url_complete_set.add(target_url)
        parser = AuthorParser(content)
        self.info_list.append(parser.get_extra_info())
        return

    def create_save_config(self):
        config = {'Answer': self.answer_list, 'Question': self.question_list, 'AuthorInfo': self.info_list, }
        return config


class CollectionWorker(PageWorker):
    def add_property(self):
        self.collection_index_list = []
        return

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        content = Http.get_content(target_url)
        if not content:
            return
        self.task_complete_set.add(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}?page={}'.format(target_url, page + 1)
            self.work_set.add(url)
        return

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        content = Http.get_content(target_url)
        if not content:
            return
        self.info_url_complete_set.add(target_url)
        parser = CollectionParser(content)
        self.info_list.append(parser.get_extra_info())
        return

    def parse_content(self, content):
        parser = CollectionParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()

        collection_info = parser.get_extra_info()
        self.add_collection_index(collection_info['collection_id'], parser.get_answer_list())

        return

    def add_collection_index(self, collection_id, answer_list):
        for answer in answer_list:
            data = {'href': answer['href'], 'collection_id': collection_id, }
            self.collection_index_list.append(data)
        return

    def create_save_config(self):
        config = {'Answer': self.answer_list, 'Question': self.question_list, 'CollectionInfo': self.info_list,
                  'CollectionIndex': self.collection_index_list, }
        return config


class TopicWorker(PageWorker):
    def add_property(self):
        self.topic_index_list = []
        return

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        content = Http.get_content(target_url + '/top-answers')
        if not content:
            return
        self.task_complete_set.add(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}/top-answers?page={}'.format(target_url, page + 1)
            self.work_set.add(url)
        return

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        content = Http.get_content(target_url + '/top-answers')
        if not content:
            return
        self.info_url_complete_set.add(target_url)
        parser = TopicParser(content)
        self.info_list.append(parser.get_extra_info())
        return

    def parse_content(self, content):
        parser = TopicParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()

        topic_info = parser.get_extra_info()
        self.add_topic_index(topic_info['topic_id'], parser.get_answer_list())

        return

    def add_topic_index(self, topic_id, answer_list):
        for answer in answer_list:
            data = {'href': answer['href'], 'topic_id': topic_id, }
            self.topic_index_list.append(data)
        return

    def create_save_config(self):
        config = {'Answer': self.answer_list, 'Question': self.question_list, 'TopicInfo': self.info_list,
                  'TopicIndex': self.topic_index_list, }
        return config

    def clear_index(self):
        topic_id_tuple = tuple(set(x['topic_id'] for x in self.topic_index_list))
        sql = 'DELETE  from TopicIndex where topic_id in ({})'.format((' ?,' * len(topic_id_tuple))[:-1])
        DB.cursor.execute(sql, topic_id_tuple)
        DB.commit()
        return


class ColumnWorker(PageWorker):
    def catch_info(self, target_url):
        return

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        result = Match.column(target_url)
        column_id = result.group('column_id')
        content = Http.get_content('https://zhuanlan.zhihu.com/api/columns/' + column_id)
        if not content:
            return
        raw_info = json.loads(content)
        info = {}
        info['creator_id'] = raw_info['creator']['slug']
        info['creator_hash'] = raw_info['creator']['hash']
        info['creator_sign'] = raw_info['creator']['bio']
        info['creator_name'] = raw_info['creator']['name']
        info['creator_logo'] = raw_info['creator']['avatar']['template'].replace('{id}', raw_info['creator']['avatar'][
            'id']).replace('_{size}', '')

        info['column_id'] = raw_info['slug']
        info['name'] = raw_info['name']
        info['logo'] = raw_info['creator']['avatar']['template'].replace('{id}', raw_info['avatar']['id']).replace(
            '_{size}', '')
        info['article'] = raw_info['postsCount']
        info['follower'] = raw_info['followersCount']
        info['description'] = raw_info['description']
        self.info_list.append(info)
        self.task_complete_set.add(target_url)
        detect_url = 'https://zhuanlan.zhihu.com/api/columns/{}/posts?limit=10&offset='.format(column_id)
        for i in range(info['article'] / 10 + 1):
            self.work_set.add(detect_url + str(i * 10))
        return

    def parse_content(self, content):
        article_list = json.loads(content)
        for info in article_list:
            article = {}
            article['author_id'] = info['author']['slug']
            article['author_hash'] = info['author']['hash']
            article['author_sign'] = info['author']['bio']
            article['author_name'] = info['author']['name']
            article['author_logo'] = info['author']['avatar']['template'].replace('{id}', info['author']['avatar'][
                'id']).replace('_{size}', '')

            article['column_id'] = info['column']['slug']
            article['name'] = info['column']['name']
            article['article_id'] = info['slug']
            article['href'] = u'https://zhuanlan.zhihu.com/{column_id}/{article_id}'.format(**article)
            article['title'] = info['title']
            article['title_image'] = info['titleImage']
            article['content'] = info['content']
            article['comment'] = info['commentsCount']
            article['agree'] = info['likesCount']
            article['publish_date'] = info['publishedTime'][:10]
            self.answer_list.append(article)
        return

    def create_save_config(self):
        config = {'ColumnInfo': self.info_list, 'Article': self.answer_list}
        return config


def worker_factory(task):
    type_list = {'answer': QuestionWorker, 'question': QuestionWorker, 'author': AuthorWorker,
                 'collection': CollectionWorker, 'topic': TopicWorker, 'column': ColumnWorker,
                 'article': ColumnWorker, }
    for key in task:
        worker = type_list[key](task[key])
        worker.start()
    return
