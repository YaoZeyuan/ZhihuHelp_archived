# -*- coding: utf-8 -*-

import json  # 用于JsonWorker

from src.lib.oauth.zhihu_oauth import ZhihuClient
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match


class Worker(object):
    """
    :type zhihu_client src.lib.oauth.zhihu_oauth.ZhihuClient
    """
    zhihu_client = None

    @staticmethod
    def set_zhihu_client(zhihu_client):
        """
        :type zhihu_client src.lib.oauth.zhihu_oauth.ZhihuClient
        :return: None
        """
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
    def catch(author_page_id):
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


class CollectionWorker(object):
    @staticmethod
    def catch(collection_id):
        collection = Worker.zhihu_client.collection(collection_id)
        raw_collection_info = collection.pure_data

        answer_id_list = []

        answer_list = []
        question_list = []
        for raw_answer in collection.answers:
            answer, question = Worker.format_answer(raw_answer)

            answer_id = str(answer['answer_id'])
            answer_id_list.append(answer_id)

            answer_list.append(answer)
            question_list.append(question)
        Worker.save_record_list('Answer', answer_list)
        Worker.save_record_list('Question', question_list)

        collected_answer_id_list = ','.join(answer_id_list)
        collection_info = CollectionWorker.format_collection(raw_collection_info, collected_answer_id_list)
        Worker.save_record_list('Collection', [collection_info])
        return

    @staticmethod
    def format_collection(raw_collection_info, collected_answer_id_list=''):
        item_key_list = [
            'id',
            'answer_count',
            'comment_count',
            'created_time',
            'description',
            'follower_count',
            'title',
            'updated_time',

        ]
        info = {}
        for key in item_key_list:
            info[key] = raw_collection_info[key]

        # 特殊映射关系
        info['creator_id'] = raw_collection_info['creator']['id']
        info['creator_name'] = raw_collection_info['creator']['name']
        info['creator_headline'] = raw_collection_info['creator']['headline']
        info['creator_avatar_url'] = raw_collection_info['creator']['avatar_url']

        info["collected_answer_id_list"] = collected_answer_id_list
        return info


class TopicWorker(object):
    @staticmethod
    def catch(topic_id):
        topic = Worker.zhihu_client.topic(topic_id)
        raw_topic_info = topic.pure_data

        answer_id_list = []

        answer_list = []
        question_list = []
        for raw_answer in topic.best_answers:
            answer, question = Worker.format_answer(raw_answer)

            answer_id = str(answer['answer_id'])
            answer_id_list.append(answer_id)

            answer_list.append(answer)
            question_list.append(question)
        Worker.save_record_list('Answer', answer_list)
        Worker.save_record_list('Question', question_list)

        answer_id_list = ','.join(answer_id_list)
        topic_info = TopicWorker.format_topic(raw_topic_info, answer_id_list)
        Worker.save_record_list('Topic', [topic_info])
        return

    @staticmethod
    def format_topic(raw_topic_info, best_answer_id_list=''):
        item_key_list = [
            'id',
            'avatar_url',
            'best_answerers_count',
            'best_answers_count',
            'excerpt',
            'followers_count',
            'introduction',
            'name',
            'questions_count',
            'unanswered_count',
        ]
        info = {}
        for key in item_key_list:
            info[key] = raw_topic_info[key]

        info["best_answer_id_list"] = best_answer_id_list
        return info


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
