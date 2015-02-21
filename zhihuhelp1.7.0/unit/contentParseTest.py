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

#Answer Test
#targetFileList = ['simpleAnswerContent1.txt']
    
#Author Test
#targetFileList = ['simpleAuthorContent1.txt']
#for filePath in targetFileList:
#    content = open('./htmlFile/' + filePath).read()
#    questionObject = ParseAuthor(content)
#    questionDictList, answerDictList = questionObject.getInfoDict()
#    print u'作者信息：'
#    printDict(authorInfoDict)
#    print "====================="
#    #print u'问题信息：'
#    #for questionInfoDict in questionDictList:
#    #    printDict(questionInfoDict)
#    #    print "====================="
#    #print ">>>>>>>>>>>>>>>>>>>>>"
#    #print u'答案内容:'
#    #for answer in answerDictList:
#    #    pass
#    #    #printDict(answer)
#    #    #print "====================="
#    print "<<<<<<<<<<<<<<<<<<<<<"

#Topic Test
#targetFileList = ['simpleTopicContent1.txt']
#for filePath in targetFileList:
#    content = open('./htmlFile/' + filePath).read()
#    questionObject = ParseTopic(content)
#    questionDictList, answerDictList = questionObject.getInfoDict()
#    print u'问题信息：'
#    for questionInfoDict in questionDictList:
#        printDict(questionInfoDict)
#        print "====================="
#    print ">>>>>>>>>>>>>>>>>>>>>"
#    print u'答案内容:'
#    for answer in answerDictList:
#        pass
#        printDict(answer)
#        print "====================="
#    print "<<<<<<<<<<<<<<<<<<<<<"

#Collection Test
#targetFileList = ['simpleCollectionContent1.txt']
#for filePath in targetFileList:
#    content = open('./htmlFile/' + filePath).read()
#    questionObject = ParseCollection(content)
#    questionDictList, answerDictList = questionObject.getInfoDict()
#    print u'问题信息：'
#    for questionInfoDict in questionDictList:
#        printDict(questionInfoDict)
#        print "====================="
#    print ">>>>>>>>>>>>>>>>>>>>>"
#    print u'答案内容:'
#    for answer in answerDictList:
#        pass
#        #printDict(answer)
#        #print "====================="
#    print "<<<<<<<<<<<<<<<<<<<<<"

#Info Test
#CollectionInfoParse Test
#targetFileList = ['collectionInfoContent1.txt']
#for filePath in targetFileList:
#    content = open('./htmlFile/' + filePath).read()
#    parse = CollectionInfoParse(content)
#    infoDict = parse.getInfoDict()
#    print u'信息字典：'
#    printDict(infoDict)
#    print "====================="

#Topic Test
targetFileList = ['topicInfoContent1.txt', 'topicInfoContent2.txt']
for filePath in targetFileList:
    content = open('./htmlFile/' + filePath).read()
    parse = TopicInfoParse(content)
    infoDict = parse.getInfoDict()
    print u'信息字典：'
    printDict(infoDict)
    print "====================="

#Author Test
#targetFileList = ['authorInfoContent1.txt']
#for filePath in targetFileList:
#    content = open('./htmlFile/' + filePath).read()
#    parse = AuthorInfoParse(content)
#    infoDict = parse.getInfoDict()
#    print u'信息字典：'
#    printDict(infoDict)
#    print "====================="
