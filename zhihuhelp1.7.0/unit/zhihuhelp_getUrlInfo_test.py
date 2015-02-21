# -*- coding: utf-8 -*-
from testScript.zhihuHelp import *
from testScript.helper    import *

unitTest = ZhihuHelp()

#getUrlInfo_test
targetList = ['answer', 'article', 'collection', 'column', 'people', 'question', 'table', 'topic']
for f in targetList:
    content = open('./addressFile/'+f, 'r')
    print u'目前正在测试的是 {} 部分'.format(f)
    for url in content:
        urlInfo = unitTest.getUrlInfo(url)
        printDict(urlInfo)
        print u'================================='
    raw_input()

