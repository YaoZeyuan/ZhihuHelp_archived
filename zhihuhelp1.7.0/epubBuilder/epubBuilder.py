# -*- coding: utf-8 -*-
import os
import re
import time
import shutil

from htmlTemplate import *
from imgDownloader import *
from epub import *

class Zhihu2Epub():
    u'''
    初版只提供将Question-Answer格式的数据转换为电子书的功能
    预计1.7.3版本之后再提供将专栏文章转换为电子书的功能
    '''
    def __init__(self, resultDict = {}, infoList = []):
        self.resultList = self.fixResultList(resultDict)
        self.frontPage  = u''
        self.indexList  = [] 
        self.indexNo    = 0 
        self.imgSet     = set()#用于储存图片地址，便于下载

        self.infoList   = []
        for info in infoList:
            if info != {}:
                self.infoList.append(info)

        self.info2Title()
        self.initBasePath()
        self.trans2Tree()
        self.imgDownload()
        self.epubCreator()
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

    def initBasePath(self):
        basePath = u'./知乎助手临时资源库/'
        targetPath = u'./助手生成的电子书/'
        self.mkdir(targetPath)
        self.mkdir(basePath)
        self.chdir(basePath)
        self.baseImgPath = u'./知乎图片池/'
        self.mkdir(self.baseImgPath)
        self.baseContentPath = u'./{}/'.format(u'知乎网页内容缓存库')
        self.rmdir(self.baseContentPath)
        self.mkdir(self.baseContentPath)
        return

    def trans2OneFile(self):
        u'''
        将电子书内容转换为一页html文件
        '''
        indexHtml   = self.createIndexHtml(self.resultList)
        contentHtml = ''
        for contentDict in self.resultList:
            contentHtml  += self.contentDict2Html(contentDict, False)
            self.indexNo += 1
        
        htmlDict = {
                  'PageTitle' : 'HTML生成测试',
                  'Guide'     : self.guideLink,
                  'Index'     : indexHtml,
                  'Content'   : self.imgFix(contentHtml),
        }
        finalHtml = baseTemplate(htmlDict)
        fileIndex = self.baseContentPath + self.fileTitle + '.html'
        htmlFile = open(fileIndex, 'wb')
        htmlFile.write(finalHtml)
        htmlFile.close()
        return
    
    def trans2Tree(self):
        u'''
        将电子书内容转换为一系列文件夹+html网页
        '''
        indexHtml = self.createIndexHtml(self.resultList)
        indexHtml = simpleIndexTemplate(indexHtml) 
        fileIndex = self.baseContentPath + str('index') + '.html'
        htmlFile  = open(fileIndex, 'wb')
        htmlFile.write(indexHtml)
        htmlFile.close()

        for contentDict in self.resultList:
            contentHtml = self.contentDict2Html(contentDict, True)
        
            htmlDict = {
                      'PageTitle' : contentDict['questionInfo']['questionTitle'],
                      'Guide'     : '',
                      'Index'     : '',
                      'Content'   : self.imgFix(contentHtml),
            }
            finalHtml = baseTemplate(htmlDict)
            fileIndex = self.baseContentPath + str(contentDict['questionInfo']['questionID']) + '.html'
            htmlFile = open(fileIndex, 'wb')
            htmlFile.write(finalHtml)
            htmlFile.close()

        return

    def info2Title(self):
        if len(self.infoList) > 5:
            self.infoList = self.infoList[0:4]

        title = ''
        link  = ''
        for info in self.infoList:
            title = title + u'&' + info['title'] + u'({})'.format(info['ID'])
            link  = link + u'、' + u'<a href="{}">{}</a>'.format(info['href'], info['title'])
        if len(title) == 0:
            title = u'&自选问题下'
            link  = u'、自选问题下'
        self.fileTitle = title[1:] + u'的知乎回答集锦'
        self.guideLink = link[1:]  + u'的知乎回答集锦'
        return
    
    def createIndexHtml(self, contentList = [], treeFlag = True):
        if treeFlag == True:
            indexHtml = ''
            indexNo   = self.indexNo
            for contentDict in contentList:
                indexDict = {
                    'title' : contentDict['questionInfo']['questionTitle'],
                    'index' : indexNo,
                    'href'  : './{}.html'.format(contentDict['questionInfo']['questionID']),
                }
                indexHtml += treeFileIndexTemplate(indexDict)
                indexNo   += 1
        else:
            indexHtml = ''
            indexNo   = self.indexNo
            for contentDict in contentList:
                indexDict = {
                    'title' : contentDict['questionInfo']['questionTitle'],
                    'index' : indexNo,
                }
                indexHtml += oneFileIndexTemplate(indexDict)
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

    def imgFix(self, content):
        for imgTag in re.findall(r'<img.*?>', content):
            src = re.search(r'(?<=src=").*?(?=")', imgTag)
            if src == None:
                continue
            else:
                src = src.group(0)
                if src.replace(' ', '') == '':
                    continue
            self.imgSet.add(src)
            fileName = self.getFileName(src)
            content  = content.replace(src, '../images/' + fileName)
        return content
    
    def getFileName(self, imgHref = ''):
        return imgHref.split('/')[-1]

    def imgDownload(self):
        downloader  = ImgDownloader(targetDir = self.baseImgPath, imgSet = self.imgSet)
        self.imgSet = downloader.leader()
        return
    
    def epubCreator(self):
        book = Book(self.fileTitle, '27149527')
        for contentDict in self.resultList:
            htmlSrc = '../../' + self.baseContentPath + str(contentDict['questionInfo']['questionID']) + '.html'
            title   = contentDict['questionInfo']['questionTitle']
            book.addHtml(src = htmlSrc, title = title)
        for src in self.imgSet:
            imgSrc = '../../' + self.baseImgPath + src
            if src == '':
                continue
            book.addImg(imgSrc)
        #add property
        book.addLanguage('zh-cn')
        book.addCreator('ZhihuHelp1.7.0')
        book.addDesc(u'该电子书由知乎助手生成，知乎助手是姚泽源为知友制作的仅供个人使用的简易电子书制作工具，源代码遵循WTFPL，希望大家能认真领会该协议的真谛，为飞面事业做出自己的贡献 XD')
        book.addRight('WTFPL')
        book.addPublisher('ZhihuHelp')
        book.addCss(u'../../../epubResource/markdownStyle.css')
        book.addCss(u'../../../epubResource/userDefine.css')

        print u'开始制作电子书'
        book.buildingEpub()
        return

    def printCurrentDir(self):
        print os.path.realpath('.')
        return

    def mkdir(self, path):
        try:
            os.mkdir(path)
        except OSError:
            pass
        return 
    
    def chdir(self, path):
        try:
            os.chdir(path)
        except OSError:
            print u'指定目录不存在，自动创建之'
            mkdir(path)
            os.chdir(path)
        return

    def rmdir(self, path):
        shutil.rmtree(path = path, ignore_errors = True)
        return
