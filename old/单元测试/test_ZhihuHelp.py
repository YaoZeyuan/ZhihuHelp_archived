# -*- coding: utf-8 -*-
import  unittest
import  urllib2
def MkUrlRequestForOpenUrl(url=''):
    header  =   {
'Accept'    :   '*/*'
,'Cookie':'q_c1=d55d91ee99a1484ea45c523d43ad3cc4|1399174529000|1396527477000; _xsrf=d76ccddd6631420787df7241954e0f76; c_c=ff0a1f30d3a211e3ba215254291c3363; q_c0="NTc1Mjk3OTkxMmM1NzU1N2MzZGQ5ZTMzMzRmNWVlMDR8MW9xU3hPdDF4U29BQlc4Qg==|1399218282|574021a9bbda221cd7144475ca05ca6a1b489e59";'
,'Accept-Encoding'   :'gzip,deflate,sdch'
,'Accept-Language'    :'zh,zh-CN;q=0.8,en-GB;q=0.6,en;q=0.4'
,'Connection'    :'keep-alive'
,'Host'    :'www.zhihu.com'
,'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'
}
    return urllib2.Request(headers=header,url=url)

from    ZhihuHelp   import  FetchMaxAnswerPageNum,OpenUrl,ChooseTarget

class   TestCase(unittest.TestCase):
    def setUp(self):
        self.test  =   FetchMaxAnswerPageNum()
    def tearDown(self):
        self.test  =   None
    def testFetchMaxAnswerPageNum(self):
        for t,number   in  [('http://www.zhihu.com/people/fei-ding-ci',1),#用户
                ('http://www.zhihu.com/people/mollymai-75/answers',4),
                ('http://www.zhihu.com/people/Eno-Bea/answers',5),
                ('http://www.zhihu.com/topic/19551147/top-answers',50),
                
                ('http://www.zhihu.com/topic/19563810/top-answers',1),#话题
                ('http://www.zhihu.com/topic/19587979/top-answers',4),
                ('http://www.zhihu.com/topic/19551147/top-answers',50),
                
                ('http://www.zhihu.com/collection/36677470 ',1),#收藏
                ('http://www.zhihu.com/collection/20205640',3),
                ('http://www.zhihu.com/collection/19762984',5),
                ]:
            content =   OpenUrl(MkUrlRequestForOpenUrl(t))
            value   =   FetchMaxAnswerPageNum(content)
            self.assertEqual(value,number)
    def testChooseTarget(self):
        for url,Return  in  [
        ('http://www.zhihu.com/people/yao-ze-yuan'      ,(1,'yao-ze-yuan')),
        ('http://www.zhihu.com/people/15.asd'           ,(1,'15.asd')),
        ('http://www.zhihu.com/people/-----'            ,(1,'-----')),
        ('http://www.zhihu.com/people/___/hello wperld' ,(1,'___')),
        ('http://www.zhihu.com/people/asdqe/awe'        ,(1,'asdqe')),
        ('http://www.zhihu.com/people/pkpkpk'           ,(1,'pkpkpk')),
        ('http://www.zhihu.com/people/over'             ,(1,'over')),
        ('http://www.zhihu.com/collection/192196'       ,(2,'192196')),
        ('http://www.zhihu.com/collection/192196/123213',(2,'192196')),
        ('http://www.zhihu.com/collection/192196/asd-r' ,(2,'192196')),
        ('http://www.zhihu.com/collection/192196'       ,(2,'192196')),
        ('http://www.zhihu.com/topic/192196/19dsad'     ,(4,'192196')),
        ('http://www.zhihu.com/topic/192196 '            ,(4,'192196')),
        
        
        
        ]:
            value   =   ChooseTarget(url)
            self.assertEqual(value,Return)


def suite():
    suite   =   unittest.TestSuite()
    suite.addTest(TestCase('testChooseTarget'))
    return suite
runner = unittest.TextTestRunner()
runner.run(suite())
