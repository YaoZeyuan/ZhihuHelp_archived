# -*- coding: utf-8 -*-

import json  # 用于JsonWorker
import random

import time

from src.lib.oauth.zhihu_oauth import ZhihuClient
from src.lib.wechat_parser.wechat import WechatColumnParser, WechatArticleParser
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
        :type task src.container.task.Task | src.container.task.AnswerTask | src.container.task.QuestionTask | src.container.task.TopicTask| src.container.task.CollectionTask | src.container.task.AuthorTask | src.container.task.ColumnTask | src.container.task.ArticleTask | src.container.task.WechatTask
        :return:
        """
        if task.get_task_type() == Type.author:
            AuthorWorker.catch(task.author_page_id)
        elif task.get_task_type() == Type.question:
            QuestionWorker.catch(task.question_id)
        elif task.get_task_type() == Type.answer:
            AnswerWorker.catch(task.answer_id)
        elif task.get_task_type() == Type.collection:
            CollectionWorker.catch(task.collection_id)
        elif task.get_task_type() == Type.topic:
            TopicWorker.catch(task.topic_id)
        elif task.get_task_type() == Type.column:
            ColumnWorker.catch(task.column_id)
        elif task.get_task_type() == Type.article:
            ColumnWorker.catch(task.column_id)
        elif task.get_task_type() == Type.wechat:
            WechatWorker.catch(task.account_id)
        else:
            Debug.logger.info(u"任务类别无法识别")
            Debug.logger.info(u"当前类别为" + task.get_task_type())
        return

    @staticmethod
    def format_raw_answer(raw_answer):
        """
        在zhihu-oauth库的Answer对象中获取信息
        :type raw_answer: src.lib.oauth.zhihu_oauth.Answer
        :return: dict
        """
        raw_answer_dict = raw_answer.pure_data.get(u'data', None)
        if not raw_answer_dict:
            # 数据为空说明其数据应在cache字段中
            raw_answer_dict = raw_answer.pure_data.get(u'cache', {})

        answer = {}
        #   有些数据只能从类属性中获取，直接取数据的话取不到(懒加载)，很坑，只能这样了= =
        answer[u'comment_count'] = raw_answer.comment_count
        answer[u'content'] = raw_answer.content
        answer[u'created_time'] = raw_answer.created_time
        answer[u'updated_time'] = raw_answer.updated_time
        answer[u'is_copyable'] = raw_answer.is_copyable
        answer[u'thanks_count'] = raw_answer.thanks_count
        answer[u'voteup_count'] = raw_answer.voteup_count

        # 特殊key
        answer[u"author_id"] = raw_answer_dict[u'author'][u'id']
        answer[u"author_name"] = raw_answer_dict[u'author'][u'name']
        answer[u"author_headline"] = raw_answer_dict[u'author'][u'headline']
        answer[u"author_avatar_url"] = raw_answer_dict[u'author'][u'avatar_url']
        answer[u"author_gender"] = raw_answer_dict[u'author'].get(u'gender', 0)

        answer[u"answer_id"] = raw_answer_dict[u'id']
        answer[u"question_id"] = raw_answer_dict[u'question'][u'id']

        question_key_list = [
            u"title",
            u"detail",
            u"answer_count",
            u"comment_count",
            u"follower_count",
            u"updated_time",
        ]
        question = {}
        for question_key in question_key_list :
            question[question_key] = getattr(raw_answer.question, question_key, u'')
        #   这个要单取。。。
        question[u"question_id"] = getattr(raw_answer.question, u'_id', '')
        return answer, question

    @staticmethod
    def format_article(column_id, raw_article):
        article_key_list = [
            u"title",  # 标题
            u"updated_time",  # 更新时间戳
            u"voteup_count",  # 赞同数
            u"image_url",  # 创建时间戳
            u"content",  # 内容(html，巨长)
            u"comment_count",  # 评论数
        ]
        article = {}
        for key in article_key_list:
            article[key] = getattr(raw_article, key, u'')
        article[u'column_id'] = column_id
        article[u'article_id'] = getattr(raw_article, u'id', u'')

        raw_article_dict = raw_article.pure_data.get(u'data', None)
        if not raw_article_dict:
            # 数据为空说明其数据应在cache字段中
            raw_article_dict = raw_article.pure_data.get(u'cache', {})

        article[u'author_id'] = raw_article_dict[u'author'][u'id']
        article[u'author_name'] = raw_article_dict[u'author'][u'name']
        article[u'author_headline'] = raw_article_dict[u'author'][u'headline']
        article[u'author_avatar_url'] = raw_article_dict[u'author'][u'avatar_url']
        article[u'author_gender'] = raw_article_dict[u'author'][u'gender']

        return article

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
        question_info = QuestionWorker.format_question(question)
        Worker.save_record_list(u'Question', [question_info])

        counter = 0
        answer_list = []
        for raw_answer in question.answers:
            counter += 1
            Debug.logger.info(u'正在抓取第{}个回答'.format(counter))
            try:
                answer, question = Worker.format_raw_answer(raw_answer)
            except Exception as e:
                #   问题/答案不存在，自动跳过
                continue
            answer_list.append(answer)
        Worker.save_record_list(u'Answer', answer_list)
        return

    @staticmethod
    def format_question(question_info):
        item_key_list = [
            u'answer_count',
            u'comment_count',
            u'follower_count',
            u'title',
            u'detail',
            u'updated_time',
        ]
        info = {}
        for key in item_key_list:
            info[key] = getattr(question_info, key, u'')

        info[u'question_id'] = getattr(question_info, u'_id', u'')

        return info

class AnswerWorker(object):
    @staticmethod
    def catch(answer_id):
        raw_answer = Worker.zhihu_client.answer(answer_id)
        try:
            answer, question = Worker.format_raw_answer(raw_answer)
        except Exception as e:
            #   问题/答案不存在，自动跳过
            return
        Worker.save_record_list(u'Question', [question])
        Worker.save_record_list(u'Answer', [answer])
        return



class AuthorWorker(object):
    @staticmethod
    def catch(author_page_id):
        author = Worker.zhihu_client.people(author_page_id)
        author_info = AuthorWorker.format_author(author, author_page_id)
        Worker.save_record_list(u'Author', [author_info])

        answer_list = []
        question_list = []
        counter = 0
        for raw_answer in author.answers:
            counter += 1
            Debug.logger.info(u'正在抓取第{}个回答'.format(counter))
            try:
                answer, question = Worker.format_raw_answer(raw_answer)
            except Exception as e:
                #   问题/答案不存在，自动跳过
                continue
            answer_list.append(answer)
            question_list.append(question)
        Worker.save_record_list(u'Answer', answer_list)
        Worker.save_record_list(u'Question', question_list)
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
            u"answer_count",
            u"articles_count",
            u"avatar_url",
            u"columns_count",
            u"description",
            u"favorite_count",
            u"favorited_count",
            u"follower_count",
            u"following_columns_count",
            u"following_count",
            u"following_question_count",
            u"following_topic_count",
            u"gender",
            u"headline",
            u"name",
            u"question_count",
            u"shared_count",
            u"is_bind_sina",
            u"thanked_count",
            u"sina_weibo_name",
            u"sina_weibo_url",
            u"voteup_count",
        ]
        info = {}
        for key in item_key_list:
            info[key] = getattr(raw_author_info,key, u'')
        info[u'author_id'] = getattr(raw_author_info, u'id', u'')

        # 特殊映射关系
        info[u"author_page_id"] = author_page_id  # 用户页面id，随时会更换
        return info


class CollectionWorker(object):
    @staticmethod
    def catch(collection_id):
        collection = Worker.zhihu_client.collection(collection_id)

        answer_id_list = []

        answer_list = []
        question_list = []
        counter = 0
        for raw_answer in collection.answers:
            counter += 1
            Debug.logger.info(u'正在抓取第{}个回答'.format(counter))
            try:
                answer, question = Worker.format_raw_answer(raw_answer)
            except Exception as e:
                #   问题/答案不存在，自动跳过
                continue
            answer_id = str(answer[u'answer_id'])
            answer_id_list.append(answer_id)

            answer_list.append(answer)
            question_list.append(question)
        Worker.save_record_list(u'Answer', answer_list)
        Worker.save_record_list(u'Question', question_list)

        collected_answer_id_list = ','.join(answer_id_list)
        collection_info = CollectionWorker.format_collection(collection, collected_answer_id_list)
        Worker.save_record_list(u'Collection', [collection_info])
        return

    @staticmethod
    def format_collection(collection, collected_answer_id_list=''):
        u"""

        :param collection: src.lib.oauth.zhihu_oauth.Collection
        :param collected_answer_id_list:
        :return:
        """
        info = {}
        info[u'answer_count'] = collection.answer_count
        info[u'comment_count'] = collection.comment_count
        info[u'created_time'] = collection.created_time
        info[u'description'] = collection.description
        info[u'follower_count'] = collection.follower_count
        info[u'title'] = collection.title
        info[u'updated_time'] = collection.updated_time

        # 特殊映射关系
        info[u'collection_id'] = collection.id
        info[u'creator_id'] = collection.creator.id
        info[u'creator_name'] = collection.creator.name
        info[u'creator_headline'] = collection.creator.headline
        info[u'creator_avatar_url'] = collection.creator.avatar_url

        info[u"collected_answer_id_list"] = collected_answer_id_list
        return info


class TopicWorker(object):
    @staticmethod
    def catch(topic_id):
        topic = Worker.zhihu_client.topic(topic_id)
        answer_id_list = []

        answer_list = []
        question_list = []
        counter = 0
        for raw_answer in topic.best_answers:
            counter += 1
            Debug.logger.info(u'正在抓取第{}个回答'.format(counter))
            try:
                answer, question = Worker.format_raw_answer(raw_answer)
            except Exception as e:
                #   问题/答案不存在，自动跳过
                continue

            answer_id = str(answer[u'answer_id'])
            answer_id_list.append(answer_id)

            answer_list.append(answer)
            question_list.append(question)
        Worker.save_record_list(u'Answer', answer_list)
        Worker.save_record_list(u'Question', question_list)

        answer_id_list = ','.join(answer_id_list)
        topic_info = TopicWorker.format_topic(topic, answer_id_list)
        Worker.save_record_list(u'Topic', [topic_info])
        return

    @staticmethod
    def format_topic(topic_info, best_answer_id_list=''):
        item_key_list = [
            u'best_answerers_count',
            u'best_answers_count',
            u'excerpt',
            u'followers_count',
            u'introduction',
            u'name',
            u'questions_count',
            u'unanswered_count',
            u'avatar_url'
        ]
        info = {}
        for item_key in item_key_list:
            info[item_key] = getattr(topic_info, item_key, '')

        info[u'topic_id'] = topic_info._id
        info[u"best_answer_id_list"] = best_answer_id_list
        return info


class ColumnWorker(object):
    @staticmethod
    def catch(column_id):
        column = Worker.zhihu_client.column(column_id)
        column_info = ColumnWorker.format_column(column)
        Worker.save_record_list(u'Column', [column_info])

        article_list = []
        counter = 0
        for raw_article in column.articles:
            counter += 1
            Debug.logger.info(u'正在抓取第{}篇文章'.format(counter))
            article = Worker.format_article(column_id, raw_article)
            article_list.append(article)

        Worker.save_record_list(u'Article', article_list)
        return

    @staticmethod
    def format_column(raw_column):
        u"""

        :param raw_column: src.lib.oauth.zhihu_oauth.zhcls.Column
        :return:
        """
        column_key_list = [
            u'title',
            u'article_count',
            u'description',
            u'follower_count',
            u'image_url',
        ]
        column_info = {}
        for key in column_key_list:
            column_info[key] = getattr(raw_column, key, u'')

        column_info[u'column_id'] = raw_column._id

        return column_info


class WechatWorker(object):
    @staticmethod
    def catch(account_id):
        # 关键就在这里了

        article_url_index_list = []

        #   获取最大页码
        url = 'http://chuansong.me/account/{}'.format(account_id)
        front_page_content = Http.get_content(url)
        max_page =WechatWorker.parse_max_page(front_page_content)
        #   分析网页内容，存到数据库里
        column_info = WechatColumnParser(front_page_content).get_column_info()
        column_info[u'column_id'] = account_id
        Worker.save_record_list(u'Column', [column_info])

        Debug.logger.info(u"最大页数抓取完毕，共{max_page}页".format(max_page=max_page))
        #   获取每一页中文章的地址的地址
        for raw_front_page_index in range(0, max_page):
            front_page_index = raw_front_page_index * 12
            request_url = url + '?start={}'.format(front_page_index)
            Debug.logger.info(
                u"开始抓取第{raw_front_page_index}页中的文章链接，共{max_page}页".format(raw_front_page_index=raw_front_page_index, max_page=max_page))
            request_url_content = Http.get_content(request_url)
            if len(request_url_content) == 0:
                continue
            article_url_index_list += Match.wechat_article_index(content=request_url_content)
            random_sleep_time = 1 + random.randrange(0, 100) / 100.0
            Debug.logger.info(u"随机休眠{}秒".format(random_sleep_time))
            time.sleep(random_sleep_time)

        article_count = len(article_url_index_list)
        Debug.logger.info(u"文章链接抓取完毕，共{article_count}篇文章待抓取".format(article_count=article_count))

        counter = 0
        for article_url_index in article_url_index_list:
            counter += 1
            request_url = 'http://chuansong.me/n/{}'.format(article_url_index)
            Debug.logger.info(u"开始抓取第{countert}篇文章，共{article_count}页".format(countert=counter,
                                                                             article_count=article_count))
            request_url_content = Http.get_content(request_url)


            article_info = WechatArticleParser(request_url_content).get_article_info()
            article_info['article_id'] = article_url_index
            article_info['column_id'] = account_id
            Worker.save_record_list(u'Article', [article_info])

            random_sleep_time = 1 + random.randint(0, 100) / 100.0
            Debug.logger.info(u"随机休眠{}秒".format(random_sleep_time))
            time.sleep(random_sleep_time)




        column = Worker.zhihu_client.column(account_id)
        column_info = ColumnWorker.format_column(column)
        Worker.save_record_list(u'Column', [column_info])

        article_list = []
        counter = 0
        for raw_article in column.articles:
            counter += 1
            Debug.logger.info(u'正在抓取第{}篇文章'.format(counter))
            article = Worker.format_article(account_id, raw_article)
            article_list.append(article)

        Worker.save_record_list(u'Article', article_list)
        return

    @staticmethod
    def format_column(raw_column):
        u"""

        :param raw_column: src.lib.oauth.zhihu_oauth.zhcls.Column
        :return:
        """
        column_key_list = [
            u'title',
            u'article_count',
            u'description',
            u'follower_count',
            u'image_url',
        ]
        column_info = {}
        for key in column_key_list:
            column_info[key] = getattr(raw_column, key, u'')

        column_info[u'column_id'] = raw_column._id

        return column_info


    @staticmethod
    def parse_max_page(content):
        max_page = 1
        try:
            floor = content.index('style="float: right">下一页</a>')
            floor = content.rfind('</a>', 0, floor)
            cell = content.rfind('>', 0, floor)
            max_page = int(content[cell + 1:floor])
            Debug.logger.info(u'答案列表共计{}页'.format(max_page))
        except:
            Debug.logger.info(u'答案列表共计1页')
        finally:
            return max_page


