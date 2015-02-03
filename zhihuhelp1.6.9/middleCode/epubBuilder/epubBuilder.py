# -*- coding: utf-8 -*-
import os
import re

from epub import *
from htmlTemplate import *
class Zhihu2Epub():
    u'''
    初版只提供将Question-Answer格式的数据转换为电子书的功能
    预计1.7.3版本之后再提供将专栏文章转换为电子书的功能
    '''
    def __init__(self, contentList = []):
        self.contentList = sorted(contentList, key=lambda x:x['agreeCount'], reverse=True)
        self.frontPage = u''
        self.indexList = [] 
        self.indexNo   = 0 
        self.mananger()
        return

    def mananger(self):
        basePath = u'./知乎助手1.7.0小试牛刀版/'
        self.mkdir(basePath)
        for content in self.contentList:
            self.worker(content, basePath)
        return

    def worker(self, content, basePath):
        questionInfo  = content['questionInfo']
        buf = {
            'index'   : self.indexNo,
            'title'   : questionInfo['questionTitle'],      
            'desc'    : questionInfo['questionDesc'],      
            'comment' : questionInfo['commentCount'],      
        }
        question2Html = questionContentTemplate(buf)       
        
        answer2Html   = ''
        for answerContent in content['answerList']:
            buf = {
                        'authorLogo'    : answerContent['authorLogo'],
                        'authorLink'    : 'http://www.zhihu.com/people/' + answerContent['authorID'],
                        'authorName'    : answerContent['authorName'],
                        'authorSign'    : answerContent['authorSign'],
                        'answerContent' : answerContent['answerContent'],
                        'answerAgree'   : answerContent['answerAgreeCount'],
                        'answerComment' : answerContent['answerCommentCount'],
                        'answerDate'    : answerContent['updateDate'].strftime('%Y-%m-%d'),
                    }
            answer2Html += answerContentTemplate(buf)
        
        buf = {
                    'QuestionContent' : question2Html,
                    'AnswerContent'   : answer2Html,
                }
        content2Html = contentTemplate(buf)
            
        buf = {
                  'PageTitle' : questionInfo['questionTitle'],
                  'Guide'     : '',
                  'Index'     : '',
                  'Content'   : content2Html,
              }
        html = baseTemplate(buf)
        htmlFile = open(basePath + str(self.indexNo) + '.html', 'wb')
        htmlFile.write(html)
        htmlFile.close()
        self.indexNo += 1
        return

    def mkdir(self, path):
        try:
            os.mkdir(path)
        except OSError:
            print u'指定目录已存在'
        return 
    
    def chdir(self, path):
        try:
            os.chdir(path)
        except OSError:
            print u'指定目录不存在，自动创建之'
            mkdir(path)
            os.chdir(path)
        return
