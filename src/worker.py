# -*- coding: utf-8 -*-

import json  # 用于JsonWorker

from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match


class Worker(object):
    zhihu_client = None

    @staticmethod
    def set_zhihu_client(zhihu_client):
        Worker.zhihu_client = zhihu_client
        return

    @staticmethod
    def distribute(task):
        """
        将外界传入的任务分发给各个抓取类
        :type task src.container.task
        :return:
        """

        return

    @staticmethod
    def format_answer(raw_answer):
        """
        :type raw_answer: dict
        :return: dict
        """
        answer_key_list = [
            "comment_count",
            "content",
            "created_time",
            "updated_time",
            "is_copyable",
            "thanks_count",
            "voteup_count",
            "suggest_edit_status",
            "suggest_edit_reason",
        ]
        answer = {}
        for answer_key in answer_key_list:
            answer[answer_key] = raw_answer.get(answer_key, '')

        # 特殊key
        answer["author_id"] = raw_answer['author']['id']
        answer["author_name"] = raw_answer['author']['name']
        answer["author_headline"] = raw_answer['author']['headline']
        answer["author_avatar_url"] = raw_answer['author']['avatar_url']
        answer["author_gender"] = raw_answer['author']['gender']

        answer["answer_id"] = raw_answer['id']
        answer["question_id"] = raw_answer['question']['id']

        question_key_list = [
            "id",
            "title",
        ]
        question = {}
        for question_key in question_key_list:
            question[question_key] = raw_answer['question'][question_key]

        return answer, question

    @staticmethod
    def save_record_list(table_name, record_list):
        """
        将数据保存到数据库中
        :return:
        """
        for record in record_list:
            DB.save(record, table_name)
        DB.commit()
        return


class AuthorWorker(object):
    @staticmethod
    def start(author_page_id):
        author = Worker.zhihu_client.people(author_page_id)
        raw_author_info = author.pure_data
        author_info = AuthorWorker.format_author(raw_author_info, author_page_id)
        Worker.save_record_list('Author', [author_info])

        answer_list = []
        question_list = []
        for raw_answer in author.answers:
            answer, question = Worker.format_answer(raw_answer)
            answer_list.append(answer)
            question_list.append(question)
        Worker.save_record_list('Answer', answer_list)
        Worker.save_record_list('Question', question_list)
        return

    @staticmethod
    def format_author(raw_author_info, author_page_id=u''):
        """
        格式化用户信息，方便存入
        :type raw_author_info: dict
        :type author_page_id: str 用户主页id，由于接口中未返回，只能钦定了←_←
        :return: dict
        """
        item_key_list = [
            "id",  # 唯一hash_id
            "answer_count",
            "articles_count",
            "avatar_url",
            "columns_count",
            "description",
            "favorite_count",
            "favorited_count",
            "follower_count",
            "following_columns_count",
            "following_count",
            "following_question_count",
            "following_topic_count",
            "gender",
            "headline",
            "name",
            "question_count",
            "shared_count",
            "is_bind_sina",
            "thanked_count",
            "sina_weibo_name",
            "sina_weibo_url",
            "voteup_count",
        ]
        info = {}
        for key in item_key_list:
            info[key] = raw_author_info[key]

        # 特殊映射关系
        info["author_page_id"] = author_page_id  # 用户页面id，随时会更换
        return info


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
        self.column_id = result.group('column_id')
        content = Http.get_content('https://zhuanlan.zhihu.com/api/columns/' + self.column_id)
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
        detect_url = 'https://zhuanlan.zhihu.com/api/columns/{}/posts?limit=10&offset='.format(self.column_id)
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

            article['column_id'] = self.column_id  # info['slug']
            article['name'] = info['title']
            article['article_id'] = info['slug']
            url = info['url']
            article['href'] = u'https://zhuanlan.zhihu.com' + url
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


def worker_factory(zhihu_api_client, task):
    """

    :type zhihu_api_client: src.lib.oauth.zhihu_oauth.ZhihuClient
    :type task dict of src.container.task.SingleTask
    :return:
    """
    type_list = {'author': AuthorWorker}
    for key in task:
        worker = type_list[key](zhihu_api_client, task[key])
        worker.start()
    return
