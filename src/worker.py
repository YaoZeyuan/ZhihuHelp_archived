# -*- coding: utf-8 -*-

import json  # 用于JsonWorker

from src.lib.oauth.zhihu_oauth import ZhihuClient
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match
from src.tools.type import Type


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
        :type task src.container.task.Task
        :return:
        """
        if task.get_task_type() == Type.author:
            AuthorWorker.catch(task.author_id)
        elif task.get_task_type() == Type.question:
            QuestionWorker.catch(task.question_id)
        elif task.get_task_type() == Type.answer:
            QuestionWorker.catch(task.question_id)
        elif task.get_task_type() == Type.collection:
            CollectionWorker.catch(task.collection_id)
        elif task.get_task_type() == Type.topic:
            TopicWorker.catch(task.topic_id)
        elif task.get_task_type() == Type.column:
            ColumnWorker.catch(task.column_id)
        elif task.get_task_type() == Type.article:
            ColumnWorker.catch(task.column_id)
        else:
            Debug.logger.info("任务类别无法识别")
            Debug.logger.info("当前类别为" + task.get_task_type())
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
        answer["author_avatar_url"] = Match.parse_img(raw_answer['author']['avatar_url'])
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
    def format_article(raw_article):
        article_key_list = [
            "title",  # 标题
            "updated",  # 更新时间戳
            "voteup_count",  # 赞同数
            "id",  # 文章id
            "created",  # 创建时间戳
            "content",  # 内容(html，巨长)
            "comment_count",  # 评论数
        ]
        article = {}
        for key in article_key_list:
            article[key] = raw_article['author'][key]
        article['image_url'] = Match.parse_column_img(raw_article['image_url'])
        article['author_id'] = raw_article['author']['id']
        article['column_id'] = raw_article['column']['id']

        author_key_list = [
            "gender",
            "headline",
            "id",  # 唯一hash_id
            "name",
        ]
        author_info = {}
        for key in author_key_list:
            author_info[key] = raw_article['author'][key]
        author_info['avatar_url'] = Match.parse_column_img(raw_article['author']['avatar_url'])

        return author_info, article

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


class QuestionWorker(object):
    @staticmethod
    def catch(question_id):
        question = Worker.zhihu_client.question(question_id)
        raw_question_info = question.pure_data
        question_info = QuestionWorker.format_question(raw_question_info)
        Worker.save_record_list('Question', [question_info])

        answer_list = []
        for raw_answer in question.answers:
            answer, question = Worker.format_answer(raw_answer)
            answer_list.append(answer)
        Worker.save_record_list('Answer', answer_list)
        return

    @staticmethod
    def format_question(raw_question_info):
        item_key_list = [
            'id',
            'answer_count',
            'comment_count',
            'follower_count',
            'title',
            'detail',
            'updated_time',
        ]
        info = {}
        for key in item_key_list:
            info[key] = raw_question_info[key]

        return info


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
        info['creator_avatar_url'] = Match.parse_img(raw_collection_info['creator']['avatar_url'])

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
        info['avatar_url'] = Match.parse_img(raw_topic_info['avatar_url'])
        info["best_answer_id_list"] = best_answer_id_list
        return info


class ColumnWorker(object):
    @staticmethod
    def catch(column_id):
        column = Worker.zhihu_client.column(column_id)
        raw_column_info = column.pure_data
        author_info, column_info = ColumnWorker.format_column(raw_column_info)
        Worker.save_record_list('Author', [author_info])
        Worker.save_record_list('Column', [column_info])

        article_list = []
        author_list = []
        for raw_article in column.articles:
            author, article = Worker.format_article(raw_article)
            article_list.append(article)
            author_list.append(author)

        Worker.save_record_list('Article', article_list)
        Worker.save_record_list('Author', author_list)
        return

    @staticmethod
    def format_column(raw_column_info):
        column_key_list = [
            'slug',
            'name',
            'postsCount',
            'description',
            'followersCount',
            'reason',
            'intro',
        ]
        column_info = {}
        for key in column_key_list:
            column_info[key] = raw_column_info[key]

        column_info['creator_id'] = raw_column_info['creator']['hash']

        author_info = {}
        author_info['headline'] = raw_column_info['creator']['bio']
        author_info['id'] = raw_column_info['creator']['hash']
        author_info['name'] = raw_column_info['creator']['name']
        author_info['author_page_id'] = raw_column_info['creator']['slug']
        author_info['description'] = raw_column_info['creator']['description']
        author_info['avatar_url'] = raw_column_info['creator']['avatar']['id'] + '.jpg'  # 强行拼接

        return author_info, column_info
