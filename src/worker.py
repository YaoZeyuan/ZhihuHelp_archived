# -*- coding: utf-8 -*-

import json  # 用于JsonWorker
from multiprocessing.dummy import Pool as ThreadPool #多线程并行库
from src.tools.config import Config
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http


class PageWorker(object):
    def __init__(self, task_list):
        self.task_set = set(task_list)
        self.work_set = set() # 待抓取网址池
        self.answer_list = []
        self.question_list = []
        self.thread_pool = ThreadPool(Config.max_thread)

        self.info_list = []
        self.extra_index_list = []
        self.info_url_set = self.task_set.copy()

        self.add_property() # 添加扩展属性
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

    @staticmethod
    def control_center(func, argv, test_flag):
        max_try = Config.max_try
        for time in range(max_try):
            if test_flag:
                func(**argv)
        return

    def create_save_config(self):
        config = {
            'Answer' : self.answer_list,
            'Question': self.question_list,
        }
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
        content = Http.get_content(target_url)
        if not content:
            return
        self.task_set.discard(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}?nr=1&sort=created&page={}'.format(target_url, page)
            self.work_set.add(url)
        return

    def clear_work_set(self):
        self.work_set = set()
        return

    def start_create_work_list(self):
        self.clear_work_set()
        argv = {
            'func':self.create_work_set,
            'iterable':self.task_set,
        }
        self.control_center(self.thread_pool.map, argv, self.task_set)
        return

    def worker(self, target_url):
        content = Http.get_content(target_url)
        if not content:
            return
        self.work_set.discard(target_url)
        self.parse_content(content)
        return

    def parse_content(self,content):
        parser = QuestionParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()
        return

    def start_worker(self):
        argv = {
            'func':self.worker, #所有待存入数据库中的数据都应当是list
            'iterable':self.work_set,
        }
        self.control_center(self.thread_pool.map, argv, self.work_set)
        return

    def catch_info(self, target_url):
        return

    def start_catch_info(self):
        argv = {
            'func':self.catch_info,
            'iterable':self.info_url_set,
        }
        self.control_center(self.thread_pool.map, argv, self.info_url_set)
        return


class QuestionWorker(PageWorker):
    def parse_content(self,content):
        parser = QuestionParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()
        return

class AuthorWorker(PageWorker):
    def parse_content(self,content):
        parser = AuthorParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()
        return

    def create_work_set(self, target_url):
        content = Http.get_content(target_url + '/answers?order_by=vote_num')
        if not content:
            return
        self.task_set.discard(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}/answers?order_by=vote_num&page={}'.format(target_url, page)
            self.work_set.add(url)
        return

    def catch_info(self, target_url):
        content = Http.get_content(target_url + '/about')
        if not content:
            return
        self.info_url_set.discard(target_url)
        parser = AuthorParser(content)
        self.info_list.append(parser.get_extra_info())
        return

    def create_save_config(self):
        config = {
            'Answer' : self.answer_list,
            'Question': self.question_list,
            'AuthorInfo':self.info_list,
        }
        return config


class CollectionWorker(PageWorker):
    def add_property(self):
        self.collection_index_list = []
        return

    def create_work_set(self, target_url):
        content = Http.get_content(target_url)
        if not content:
            return
        self.task_set.discard(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}?page={}'.format(target_url, page)
            self.work_set.add(url)
        return

    def catch_info(self, target_url):
        content = Http.get_content(target_url)
        if not content:
            return
        self.info_url_set.discard(target_url)
        parser = CollectionParser(content)
        self.info_list.append(parser.get_extra_info())
        return

    def parse_content(self,content):
        parser = CollectionParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()

        collection_info = parser.get_extra_info()
        self.add_collection_index(collection_info['collection_id'], parser.get_answer_list())

        return

    def add_collection_index(self, collection_id, answer_list):
        for answer in answer_list:
            data = {
                'href' : answer['href'],
                'collection_id':collection_id,
            }
            self.collection_index_list.append(data)
        return

    def create_save_config(self):
        config = {
            'Answer' : self.answer_list,
            'Question': self.question_list,
            'CollectionInfo':self.info_list,
            'CollectionIndex':self.collection_index_list,
        }
        return config

class TopicWorker(PageWorker):
    def add_property(self):
        self.topic_index_list = []
        return

    def create_work_set(self, target_url):
        content = Http.get_content(target_url + '/top-answers')
        if not content:
            return
        self.task_set.discard(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}/top-answers?page={}'.format(target_url, page)
            self.work_set.add(url)
        return

    def catch_info(self, target_url):
        content = Http.get_content(target_url + '/top-answers')
        if not content:
            return
        self.info_url_set.discard(target_url)
        parser = TopicParser(content)
        self.info_list.append(parser.get_extra_info())
        return

    def parse_content(self,content):
        parser = TopicParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()

        topic_info = parser.get_extra_info()
        self.add_topic_index(topic_info['topic_id'], parser.get_answer_list())

        return

    def add_topic_index(self, topic_id, answer_list):
        for answer in answer_list:
            data = {
                'href' : answer['href'],
                'topic_id':topic_id,
            }
            self.topic_index_list.append(data)
        return

    def create_save_config(self):
        config = {
            'Answer' : self.answer_list,
            'Question': self.question_list,
            'TopicInfo':self.info_list,
            'TopicIndex':self.topic_index_list,
        }
        return config

    def clear_index(self):
        topic_id_tuple = tuple(set(x['topic_id'] for x in self.topic_index_list))
        sql = 'DELETE  from TopicIndex where topic_id in ({})'.format((' ?,' * len(topic_id_tuple))[:-1])
        DB.cursor.execute(sql, topic_id_tuple)
        DB.commit()
        return

def worker_factory(task):
    type_list ={
        'answer': QuestionWorker,
        'question':QuestionWorker,
        'author':AuthorWorker,
        'collection':CollectionWorker,
        'topic':TopicWorker,
        'column':TopicWorker,
        'article':TopicWorker,
    }
    for key in task:
        worker = type_list[key](task[key])
        worker.start()
    return