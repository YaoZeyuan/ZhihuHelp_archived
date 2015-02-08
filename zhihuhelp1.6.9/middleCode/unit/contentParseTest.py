# -*- coding: utf-8 -*-
import re
import os

from testScript.contentParse import *
from testScript.helper import *

import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 

#Question Test
#targetFileList = ['simpleQuestionContent1.txt']
#for filePath in targetFileList:
#    content = open('./htmlFile/' + filePath).read()
#    questionObject = ParseQuestion(content)
#    questionInfoDict, answerDictList = questionObject.getInfoDict()
#    print ">>>>>>>>>>>>>>>>>>>>>"
#    #print u'问题信息：'
#    #printDict(questionInfoDict)
#    print "====================="
#    print u'答案内容:'
#    for answer in answerDictList:
#        printDict(answer)
#        print "====================="
#    print "<<<<<<<<<<<<<<<<<<<<<"

#Answer Test
#targetFileList = ['simpleAnswerContent1.txt']
#for filePath in targetFileList:
#    content = open('./htmlFile/' + filePath).read()
#    questionObject = ParseAnswer(content)
#    questionInfoDict, answerDictList = questionObject.getInfoDict()
#    print ">>>>>>>>>>>>>>>>>>>>>"
#    print u'问题信息：'
#    printDict(questionInfoDict)
#    print "====================="
#    print u'答案内容:'
#    for answer in answerDictList:
#        printDict(answer)
#        print "====================="
#        print "<<<<<<<<<<<<<<<<<<<<<"
    
#Author Test
targetFileList = ['simpleAuthorContent1.txt']
for filePath in targetFileList:
    content = open('./htmlFile/' + filePath).read()
    questionObject = ParseAuthor(content)
    questionDictList, answerDictList = questionObject.getInfoDict()
    print u'问题信息：'
    for questionInfoDict in questionDictList:
        printDict(questionInfoDict)
        print "====================="
    print ">>>>>>>>>>>>>>>>>>>>>"
    print u'答案内容:'
    for answer in answerDictList:
        pass
        #printDict(answer)
        #print "====================="
    print "<<<<<<<<<<<<<<<<<<<<<"
