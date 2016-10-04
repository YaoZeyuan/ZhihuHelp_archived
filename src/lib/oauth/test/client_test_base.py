import os
import unittest

from zhihu_oauth import ZhihuClient


class ZhihuClientClassTest(unittest.TestCase):
    def setUp(self):
        super(ZhihuClientClassTest, self).setUp()

        if not os.path.isdir('test') and os.path.isfile('token.pkl'):
            os.chdir('..')

        if not os.path.isfile('test/token.pkl'):
            print('\nno token file, skip all tests.')
            self.skipTest('no token file.')

        self.client = ZhihuClient()

        try:
            self.client.load_token('test/token.pkl')
        except ValueError:
            print(
                '\ntoken version not math python version, skip all tests.')
            self.skipTest('token version not math python version.')
