from __future__ import unicode_literals

from zhihu_oauth import (Answer, Article, Collection, Column, People, Question,
                         Topic)

from .client_test_base import ZhihuClientClassTest


class TestZhihuClientFromURL(ZhihuClientClassTest):
    def test_correct_answer_url(self):
        url_list = [
            # normal url
            'https://www.zhihu.com/question/42248369/answer/94150403',
            # with http scheme
            'http://www.zhihu.com/question/42248369/answer/94150403',
            # with a slash at end
            'https://www.zhihu.com/question/42248369/answer/94150403/',
            # with http and slash
            'http://www.zhihu.com/question/42248369/answer/94150403/',
            # without scheme
            'www.zhihu.com/question/42248369/answer/94150403',
            # without scheme but has slash
            'www.zhihu.com/question/42248369/answer/94150403/'
        ]
        for url in url_list:
            obj = self.client.from_url(url)
            self.assertIsInstance(obj, Answer)
            self.assertEqual(obj.id, 94150403)

    def test_error_answer_url(self):
        url_list = [
            # no www
            'https://zhihu.com/question/42248369/answer/94150403',
            # no answer part
            'https://www.zhihu.com/question/42248369',
            # just a num
            '94150403',
            # answer id not int
            'https://www.zhihu.com/question/42248369/answer/error',
            # question id not int
            'https://www.zhihu.com/question/error/answer/94150403',
            # question spelling error
            'https://www.zhihu.com/question_er/42248369/answer/94150403',
            # answer spelling error
            'https://www.zhihu.com/question/42248369/answer_er/94150403',
            # more than a invalid url
            'some text https://zhihu.com/question/42248369/answer/94150403',
            # more than a invalid url
            'https://www.zhihu.com/question/error/answer/94150403 some text',
        ]

        for url in url_list:
            with self.assertRaises(ValueError):
                obj = self.client.from_url(url)
                if not isinstance(obj, Answer):
                    raise ValueError

    def test_correct_article_url(self):
        url_list = [
            # normal url
            'http://zhuanlan.zhihu.com/p/20597723',
            # with https scheme
            'https://zhuanlan.zhihu.com/p/20597723',
            # with a slash at end
            'http://zhuanlan.zhihu.com/p/20597723/',
            # with http and slash
            'https://zhuanlan.zhihu.com/p/20597723/',
            # without scheme
            'zhuanlan.zhihu.com/p/20597723',
            # without scheme but has slash
            'zhuanlan.zhihu.com/p/20597723/'
        ]
        for url in url_list:
            obj = self.client.from_url(url)
            self.assertIsInstance(obj, Article)
            self.assertEqual(obj.id, 20597723)

    def test_error_article_url(self):
        url_list = [
            # no p - become a column url
            'http://zhuanlan.zhihu.com/20597723',
            # just a num
            '20597723',
            # article id not int
            'http://zhuanlan.zhihu.com/p/error',
            # p spelling errors
            'http://zhuanlan.zhihu.com/p_er/20597723',
            # more than a invalid url
            'some text http://zhuanlan.zhihu.com/p/20597723',
            # more than a invalid url
            'http://zhuanlan.zhihu.com/p/20597723 some text',
        ]

        for url in url_list:
            with self.assertRaises(ValueError):
                obj = self.client.from_url(url)
                if not isinstance(obj, Article):
                    raise ValueError

    def test_correct_collection_url(self):
        url_list = [
            # normal url
            'https://www.zhihu.com/collection/28698204',
            # with http scheme
            'http://www.zhihu.com/collection/28698204',
            # with a slash at end
            'https://www.zhihu.com/collection/28698204/',
            # with http and slash
            'http://www.zhihu.com/collection/28698204/',
            # without scheme
            'www.zhihu.com/collection/28698204',
            # without scheme but has slash
            'www.zhihu.com/collection/28698204/'
        ]
        for url in url_list:
            obj = self.client.from_url(url)
            self.assertIsInstance(obj, Collection)
            self.assertEqual(obj.id, 28698204)

    def test_error_collection_url(self):
        url_list = [
            # just a num
            '28698204',
            # collection id not int
            'https://www.zhihu.com/collection/error',
            # collection spellling error
            'https://www.zhihu.com/collection_er/28698204',
            # more than a invalid url
            'some text https://www.zhihu.com/collection/28698204',
            # more than a invalid url
            'https://www.zhihu.com/collection/28698204 some text',
        ]

        for url in url_list:
            with self.assertRaises(ValueError):
                self.client.from_url(url)

    def test_correct_column_url(self):
        url_list = [
            # normal url
            'http://zhuanlan.zhihu.com/o0v0o',
            # with https scheme
            'https://zhuanlan.zhihu.com/o0v0o',
            # with a slash at end
            'http://zhuanlan.zhihu.com/o0v0o/',
            # with https and slash
            'https://zhuanlan.zhihu.com/o0v0o/',
            # without scheme
            'zhuanlan.zhihu.com/o0v0o',
            # without scheme but has slash
            'zhuanlan.zhihu.com/o0v0o/'
        ]
        for url in url_list:
            obj = self.client.from_url(url)
            self.assertIsInstance(obj, Column)
            self.assertEqual(obj.id, 'o0v0o')

    def test_error_column_url(self):
        url_list = [
            # just a id
            'o0v0o',
            # id has slash
            'http://zhuanlan.zhihu.com/o0v/0o',
            # more than a invalid url
            'some text http://zhuanlan.zhihu.com/o0v0o',
            # more than a invalid url
            'http://zhuanlan.zhihu.com/o0v0o some text',
        ]

        for url in url_list:
            with self.assertRaises(ValueError):
                self.client.from_url(url)

    def test_correct_people_url(self):
        url_list = [
            # normal url
            'https://www.zhihu.com/people/7sdream',
            # with http scheme
            'http://www.zhihu.com/people/7sdream',
            # with a slash at end
            'https://www.zhihu.com/people/7sdream/',
            # with http and slash
            'http://www.zhihu.com/people/7sdream/',
            # without scheme
            'www.zhihu.com/people/7sdream',
            # without scheme but has slash
            'www.zhihu.com/people/7sdream/'
        ]

        for url in url_list:
            obj = self.client.from_url(url)
            self.assertIsInstance(obj, People)
            self.assertEqual(obj.id, '7sdream')

    def test_error_people_url(self):
        url_list = [
            # just a id
            '7sdream',
            # id has slash
            'https://www.zhihu.com/people/7sdr/eam',
            # spelling error
            'https://www.zhihu.com/people_er/7sdream',
            # more than a invalid url
            'some text https://www.zhihu.com/people/7sdream',
            # more than a invalid url
            'https://www.zhihu.com/people/7sdream some text',
        ]

        for url in url_list:
            with self.assertRaises(ValueError):
                self.client.from_url(url)

    def test_correct_question_url(self):
        url_list = [
            # normal url
            'https://www.zhihu.com/question/42248369',
            # with http scheme
            'http://www.zhihu.com/question/42248369',
            # with a slash at end
            'https://www.zhihu.com/question/42248369/',
            # with http and slash
            'http://www.zhihu.com/question/42248369/',
            # without scheme
            'www.zhihu.com/question/42248369',
            # without scheme but has slash
            'www.zhihu.com/question/42248369/'
        ]

        for url in url_list:
            obj = self.client.from_url(url)
            self.assertIsInstance(obj, Question)
            self.assertEqual(obj.id, 42248369)

    def test_error_question_url(self):
        url_list = [
            # just a id
            '42248369',
            # id not int
            'https://www.zhihu.com/question/error',
            # spelling error
            'https://www.zhihu.com/question_er/42248369',
            # has answer part - become an answer
            'https://www.zhihu.com/question/42248369/answer/123456',
            # more than a invalid url
            'some text https://www.zhihu.com/question/42248369',
            # more than a invalid url
            'https://www.zhihu.com/question/42248369 some text',
        ]

        for url in url_list:
            with self.assertRaises(ValueError):
                obj = self.client.from_url(url)
                if not isinstance(obj, Question):
                    raise ValueError

    def test_correct_topic_url(self):
        url_list = [
            # normal url
            'https://www.zhihu.com/topic/19550434',
            # with http scheme
            'http://www.zhihu.com/topic/19550434',
            # with a slash at end
            'https://www.zhihu.com/topic/19550434/',
            # with http and slash
            'https://www.zhihu.com/topic/19550434/',
            # without scheme
            'www.zhihu.com/topic/19550434',
            # without scheme but has slash
            'www.zhihu.com/topic/19550434/'
        ]

        for url in url_list:
            obj = self.client.from_url(url)
            self.assertIsInstance(obj, Topic)
            self.assertEqual(obj.id, 19550434)

    def test_error_topic_url(self):
        url_list = [
            # just a id
            '19550434',
            # id not int
            'https://www.zhihu.com/topic/error',
            # spelling error
            'https://www.zhihu.com/topic_er/19550434',
            # more than a invalid url
            'some text https://www.zhihu.com/topic/19550434',
            # more than a invalid url
            'https://www.zhihu.com/topic/19550434 some text',
        ]

        for url in url_list:
            with self.assertRaises(ValueError):
                obj = self.client.from_url(url)
                if not isinstance(obj, Topic):
                    raise ValueError
