# -*- coding: utf-8 -*-
import os
import re

from htmlTemplate import *
class Zhihu2Epub():
    u'''
    初版只提供将Question-Answer格式的数据转换为电子书的功能
    预计1.7.3版本之后再提供将专栏文章转换为电子书的功能
    '''
    def __init__(self, resultDict = {}, infoList = []):
        self.infoList   = infoList 
        self.resultList = self.fixResultList(resultDict)
        self.frontPage  = u''
        self.indexList  = [] 
        self.indexNo    = 0 
        self.trans2OneFile()
        return
    
    def fixResultList(self, resultDict):
        contentList = []
        for questionID in resultDict:
            contentDict = resultDict[questionID]
            agreeCount  = 0
            for answerID in contentDict['answerListDict']:
                agreeCount += contentDict['answerListDict'][answerID]['answerAgreeCount']
            contentDict['agreeCount'] = agreeCount
            contentList.append(contentDict)
        
        return sorted(contentList, key=lambda contentDict: contentDict['agreeCount'], reverse=True)

    def trans2OneFile(self):
        u'''
        将电子书内容转换为一页html文件
        '''
        indexHtml   = self.createIndexHtml(self.resultList)
        contentHtml = ''
        for contentDict in self.resultList:
            contentHtml += self.contentDict2Html(contentDict, False)
            self.indexNo += 1
        
        htmlDict = {
                  'PageTitle' : 'HTML生成测试',
                  'Guide'     : '',
                  'Index'     : indexHtml,
                  'Content'   : contentHtml,
        }
        basePath = u'./知乎助手1.7.0小试牛刀版/'
        self.mkdir(basePath)
        finalHtml = baseTemplate(htmlDict)
        fileIndex = basePath + 'HTML生成测试' + '.html'
        htmlFile = open(fileIndex, 'wb')
        htmlFile.write(finalHtml)
        htmlFile.close()
        return
    
    def trans2Tree(self):
        u'''
        将电子书内容转换为一系列文件夹+html网页
        '''
        return

    def createIndexHtml(self, contentList = []):
        indexHtml = ''
        indexNo   = self.indexNo
        for contentDict in contentList:
            indexDict = {
                'title' : contentDict['questionInfo']['questionTitle'],
                'index' : indexNo,
            }
            indexHtml += indexTemplate(indexDict)
            indexNo   += 1
        return indexHtml

    def contentDict2Html(self, contentDict = {}, treeFlag = True):
        u'''
        将一个问题--答案字典转化为html代码
            *   内容列表，其内为questionID => 答案内容的映射
            *   数据结构
                *   questionID
                    *   核心key值
                    *   questionInfo
                        *   问题信息
                    *   answerListDict
                        *   答案列表,其内为 answerID => 答案内容 的映射   
                        *   answerID
                            *   核心key值
                            *   其内为正常取出的答案
        '''
        questionInfo = contentDict['questionInfo']
        if treeFlag == True:
            questionInfoDict = {
                'index'   : self.indexNo,
                'title'   : questionInfo['questionTitle'],      
                'desc'    : questionInfo['questionDesc'],      
                'comment' : questionInfo['commentCount'],      
            }
        else:   
            questionInfoDict = {
                'index'   : self.indexNo,
                'title'   : questionInfo['questionTitle'],      
                'desc'    : '',
                'comment' : questionInfo['commentCount'],      
            }
        question2Html = questionContentTemplate(questionInfoDict)       

        contentList = []
        for answerID in contentDict['answerListDict']:
            contentList.append(contentDict['answerListDict'][answerID])

        contentList = sorted(contentList, key=lambda answerDict: answerDict['answerAgreeCount'], reverse=True)

        answer2Html = ''
        for answerContent in contentList:
            answerDict = {
                        'authorLogo'    : answerContent['authorLogo'],
                        'authorLink'    : 'http://www.zhihu.com/people/' + answerContent['authorID'],
                        'authorName'    : answerContent['authorName'],
                        'authorSign'    : answerContent['authorSign'],
                        'answerContent' : answerContent['answerContent'],
                        'answerAgree'   : answerContent['answerAgreeCount'],
                        'answerComment' : answerContent['answerCommentCount'],
                        'answerDate'    : answerContent['updateDate'].strftime('%Y-%m-%d'),
            }
            answer2Html += answerContentTemplate(answerDict)
        
        contentDict = {
                    'QuestionContent' : question2Html,
                    'AnswerContent'   : answer2Html,
        }
        contentHtml = contentTemplate(contentDict)
        return contentHtml
    
    def mananger(self):
        basePath = u'./知乎助手1.7.0小试牛刀版/'
        self.mkdir(basePath)
        for contentDict in self.contentList:
            for content in contentDict['contentList']:
                self.worker(content, basePath)
        return

    def worker(self, content, basePath):
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
