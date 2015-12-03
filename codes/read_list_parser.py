# -*- coding: utf-8 -*-
import re

from baseClass import BaseClass, TypeClass
from task_info import TaskInfo, Task


class ReadListParser():
    u"""
    通过Parser类，生成任务列表以及查询列表，统一存放于urlInfo中
    task结构
    *   work_list
        *   'answer', 'question', 'author', 'collection', 'topic', 'article', 'column'
            *   按kind分类
            *   分类后为一列表，其内是同类目下所有待抓取的网页链接
            *   抓取时不用考虑抓取顺序，所以可以按类别归并后一块抓取
    *   book_list
        *   'answer', 'question', 'author', 'collection', 'topic', 'article', 'column'
            *   按kind分类
            *   列表中为book信息，每一个book对应一本单独的电子书
            *   应该将同一book_list里的所有book输出到同一本电子书内，这样才符合当时的本意
            *   那就按章节进行区分吧，由RawBook负责进行生成处理
    """
    # url模式
    pattern = dict()
    pattern['answer'] = r'(?<=zhihu\.com/)question/(?P<question_id>\d{8})/answer/(?P<answer_id>\d{8})'
    pattern['question'] = r'(?<=zhihu\.com/)question/(?P<question_id>\d{8})'
    pattern['author'] = r'(?<=zhihu\.com/)people/(?P<author_id>[^/\n\r]*)'
    pattern['collection'] = r'(?<=zhihu\.com/)collection/(?P<collection_id>\d*)'
    pattern['topic'] = r'(?<=zhihu\.com/)topic/(?P<topic_id>\d*)'
    pattern['article'] = r'(?<=zhuanlan\.zhihu\.com/)(?P<column_id>[^/]*)/(?P<article_id>\d{8})'
    pattern['column'] = r'(?<=zhuanlan\.zhihu\.com/)(?P<column_id>[^/\n\r]*)'

    @staticmethod
    def get_task(command):
        u"""
        对外接口，
        用于分析指令
        """

        def split_command(command):
            return command.split('$')

        def remove_comment(command):
            return command.split('#')[0]

        command = remove_comment(command)
        command_list = split_command(command)

        raw_task_list = []
        for command in command_list:
            raw_task = ReadListParser.parse_command(command)
            if not raw_task:
                continue
            raw_task_list.append(raw_task)

        task = ReadListParser.merge_task_list(raw_task_list)
        return task

    @staticmethod
    def parse_command(raw_command=''):
        u"""
        分析单条命令并返回待完成的task
        task格式
        *   kind
            *   字符串，见TypeClass.type_list
        *   spider
            *   href
                *   网址原始链接，例http://www.zhihu.com/question/33578941
                *   末尾没有『/』
        *   book
            *   kind
            *   info
            *   question
            *   answer
        """

        def detect(command):
            for command_type in TypeClass.type_list:
                result = re.search(ReadListParser.pattern[command_type], command)
                if result:
                    return command_type
            return 'unknown'

        def parse_question(command):
            result = re.search(ReadListParser.pattern['question'], command)
            question_id = result.group('question_id')
            task = TaskInfo()
            task.kind = 'question'

            task.spider.href = 'http://www.zhihu.com/question/{}'.format(question_id)
            task.book.kind = 'question'
            task.book.info = ''
            task.book.question = 'question_id = "{}"'.format(question_id)
            task.book.answer = 'question_id = "{}"'.format(question_id)
            return task

        def parse_answer(command):
            result = re.search(ReadListParser.pattern['answer'], command)
            question_id = result.group('question_id')
            answer_id = result.group('answer_id')
            task = TaskInfo()
            task.kind = 'answer'
            task.spider.href = 'http://www.zhihu.com/question/{}/answer/{}'.format(question_id, answer_id)

            task.book.kind = 'answer'
            task.book.info = ''
            task.book.question = 'question_id = "{}"'.format(question_id)
            task.book.answer = 'question_id = "{}" and answer_id = "{}"'.format(question_id, answer_id)
            return task

        def parse_author(command):
            result = re.search(ReadListParser.pattern['author'], command)
            author_id = result.group('author_id')
            task = TaskInfo()
            task.kind = 'author'
            task.spider.href = 'http://www.zhihu.com/people/{}'.format(author_id)
            task.book.kind = 'author'
            task.book.info = 'select * from AuthorInfo where author_id = "{}"'.format(author_id)
            task.book.question = 'select * from Question where question_id in (select question_id from Answer where author_id = "{}")'.format(
                author_id)
            task.book.answer = 'select * from Answer where author_id = "{}"'.format(author_id)
            return task

        def parse_collection(command):
            result = re.search(ReadListParser.pattern['collection'], command)
            collection_id = result.group('collection_id')
            task = TaskInfo()
            task.kind = 'collection'
            task.spider.href = 'http://www.zhihu.com/collection/{}'.format(collection_id)
            task.book.kind = 'collection'
            task.book.info = 'select * from CollectionInfo where collection_id = "{}"'.format(collection_id)
            task.book.question = 'select * from Question where question_id in (select question_id from Answer where href in (select href from CollectionIndex where collection_id = "{}"))'.format(
                collection_id)
            task.book.answer = 'select * from Answer where href in (select href from CollectionIndex where collection_id = "{}")'.format(
                collection_id)
            return task

        def parse_topic(command):
            result = re.search(ReadListParser.pattern['topic'], command)
            topic_id = result.group('topic_id')
            task = TaskInfo()
            task.kind = 'topic'
            task.spider.href = 'http://www.zhihu.com/topic/{}'.format(topic_id)
            task.book.kind = 'topic'
            task.book.info = 'select * from TopicInfo where topic_id = "{}"'.format(topic_id)
            task.book.question = 'select * from Question where question_id in (select question_id from Answer where href in (select href from TopicIndex where topic_id = "{}"))'.format(
                topic_id)
            task.book.answer = 'select * from Answer where href in (select href from TopicIndex where topic_id = "{}")'.format(
                topic_id)
            return task

        def parse_article(command):
            result = re.search(ReadListParser.pattern['article'], command)
            column_id = result.group('column_id')
            article_id = result.group('article_id')
            task = TaskInfo()
            task.kind = 'article'
            task.spider.href = 'http://zhuanlan.zhihu.com/{}/{}'.format(column_id, article_id)
            task.book.kind = 'article'
            task.book.info = 'select * from ColumnInfo where column_id = "{}" '.format(column_id)
            task.book.question = ''
            task.book.answer = ' column_id = {} and article_id = {} '.format(column_id, article_id)
            return task

        def parse_column(command):
            result = re.search(ReadListParser.pattern['column'], command)
            column_id = result.group('column_id')
            task = TaskInfo()
            task.kind = 'article'
            task.spider.href = 'http://zhuanlan.zhihu.com/{}'.format(column_id)
            task.book.kind = 'column'
            task.book.info = 'select * from ColumnInfo where column_id = "{}" '.format(column_id)
            task.book.question = ''
            task.book.answer = 'select * from Article where column_id = "{}" '.format(column_id)
            return task

        def parse_error(command):
            BaseClass.logger.info(u"""匹配失败，未知readList类型。\n失败命令:{}""".format(command))
            return

        parser = {'answer': parse_answer, 'question': parse_question, 'author': parse_author,
                  'collection': parse_collection, 'topic': parse_topic, 'article': parse_article,
                  'column': parse_column, 'unknown': parse_error, }
        kind = detect(raw_command)
        return parser[kind](raw_command)

    @staticmethod
    def merge_task_list(task_list):
        task = Task()
        for item in task_list:
            task.add_task(item)
        return task.get_task()
