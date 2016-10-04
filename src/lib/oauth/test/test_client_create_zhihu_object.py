from __future__ import unicode_literals

from zhihu_oauth.zhcls import *
from zhihu_oauth.exception import IdMustBeIntException

from .client_test_base import ZhihuClientClassTest


class TestZhihuClientFromURL(ZhihuClientClassTest):
    def test_answer_id_must_be_int(self):
        self.assertIsInstance(self.client.answer(0), Answer)
        with self.assertRaises(IdMustBeIntException):
            self.client.answer('0')

    def test_article_id_must_be_int(self):
        self.assertIsInstance(self.client.article(0), Article)
        with self.assertRaises(IdMustBeIntException):
            self.client.article('0')

    def test_collection_id_must_be_int(self):
        self.assertIsInstance(self.client.collection(0), Collection)
        with self.assertRaises(IdMustBeIntException):
            self.client.article('0')

    def test_column_id_need_not_be_int(self):
        self.assertIsInstance(self.client.column(0), Column)
        self.assertIsInstance(self.client.column('0'), Column)

    def test_people_id_need_not_be_int(self):
        self.assertIsInstance(self.client.people(1), People)
        self.assertIsInstance(self.client.people('1'), People)

    def test_people_with_id_0_is_a_anonymous(self):
        self.assertIs(self.client.people('0'), ANONYMOUS)
        self.assertFalse(self.client.people(0) is ANONYMOUS)
        self.assertFalse(self.client.people('1') is ANONYMOUS)

    def test_question_id_must_be_int(self):
        self.assertIsInstance(self.client.question(0), Question)
        with self.assertRaises(IdMustBeIntException):
            self.client.question('0')

    def test_topic_id_must_be_int(self):
        self.assertIsInstance(self.client.topic(0), Topic)
        with self.assertRaises(IdMustBeIntException):
            self.client.topic('0')
