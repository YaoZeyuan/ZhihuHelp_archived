# -*- coding: utf-8 -*-
from src.container.task import QuestionTask, AnswerTask, AuthorTask, CollectionTask, TopicTask, \
    ArticleTask, ColumnTask
from src.tools.debug import Debug
from src.tools.match import Match
from src.tools.type import Type


class CommandParser(object):
    u"""
    通过Parser类，生成任务列表,以task容器列表的形式返回回去
    """

    @staticmethod
    def get_task_list(command):
        u"""
        解析指令类型
        """
        command = command \
            .replace(' ', '') \
            .replace('\r', '') \
            .replace('\n', '') \
            .replace('\t', '') \
            .split('#')[0]
        command_list = command.split('$')

        task_list = []
        for command in command_list:
            task = CommandParser.parse_command(command)
            if not task:
                continue
            task_list.append(task)
        return task_list

    @staticmethod
    def detect(command):
        for command_type in [
            Type.answer, Type.question,
            Type.author, Type.collection, Type.topic,
            Type.article, Type.column,  # 文章必须放在专栏之前（否则检测类别的时候就一律检测为专栏了）
        ]:
            result = getattr(Match, command_type)(command)
            if result:
                return command_type
        return Type.unknown

    @staticmethod
    def parse_command(raw_command=''):
        u"""
        分析单条命令并返回待完成的task
        """
        parser = {
            Type.author: CommandParser.parse_author,
            Type.answer: CommandParser.parse_answer,
            Type.question: CommandParser.parse_question,
            Type.collection: CommandParser.parse_collection,
            Type.topic: CommandParser.parse_topic,
            Type.article: CommandParser.parse_article,
            Type.column: CommandParser.parse_column,
            Type.unknown: CommandParser.parse_error,
        }
        kind = CommandParser.detect(raw_command)
        return parser[kind](raw_command)

    @staticmethod
    def parse_question(command):
        result = Match.question(command)
        question_id = result.group(u'question_id')
        task = QuestionTask(question_id)
        return task

    @staticmethod
    def parse_answer(command):
        result = Match.answer(command)
        question_id = result.group(u'question_id')
        answer_id = result.group(u'answer_id')
        task = AnswerTask(question_id, answer_id)
        return task

    @staticmethod
    def parse_author(command):
        result = Match.author(command)
        author_page_id = result.group(u'author_page_id')
        task = AuthorTask(author_page_id)
        return task

    @staticmethod
    def parse_collection(command):
        result = Match.collection(command)
        collection_id = result.group(u'collection_id')
        task = CollectionTask(collection_id)
        return task

    @staticmethod
    def parse_topic(command):
        result = Match.topic(command)
        topic_id = result.group(u'topic_id')
        task = TopicTask(topic_id)
        return task

    @staticmethod
    def parse_article(command):
        result = Match.article(command)
        column_id = result.group(u'column_id')
        article_id = result.group(u'article_id')
        task = ArticleTask(column_id, article_id)
        return task

    @staticmethod
    def parse_column(command):
        result = Match.column(command)
        column_id = result.group(u'column_id')
        task = ColumnTask(column_id)
        return task

    @staticmethod
    def parse_error(command):
        if command:
            Debug.logger.info(u"""无法解析记录:{}所属网址类型,请检查后重试。""".format(command))
        return
