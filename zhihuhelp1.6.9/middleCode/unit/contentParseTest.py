# -*- coding: utf-8 -*-
import re
import os

from testScript.contentParse import *
from testScript.helper import *

import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 

targetFileList = ['simpleQuestionContent1.txt']
for filePath in targetFileList:
    content = open('./htmlFile/' + filePath).read()
    questionObject = ParseQuestion(content)
    questionInfoDict, answerDictList = questionObject.getInfoDict()
    print ">>>>>>>>>>>>>>>>>>>>>"
    #print u'问题信息：'
    #printDict(questionInfoDict)
    print "====================="
    print u'答案内容:'
    for answer in answerDictList:
        printDict(answer)
        print "====================="
    print "<<<<<<<<<<<<<<<<<<<<<"
