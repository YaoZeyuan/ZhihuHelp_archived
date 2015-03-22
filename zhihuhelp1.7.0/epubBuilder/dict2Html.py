# -*- coding: utf-8 -*-
import re

from htmlTemplate import *

class dict2Html():
    def __init__(self, contentPackage):
        self.trans = 
        if contentPackage['kind'] == 'column':
            self.trans = updateDateTransfer(contentPackage)
        else:
            self.trans = AgreeCountTransfer(contentPackage)
        return

    def getResult(self):
        return self.trans.getResult()

class Transfer():
    u'''
    基本的转换类，提供通用的字典转Html方法
    '''
    def __init__(self, contentPackage):
        self.package  = contentPackage
        self.ingSet   = set()
        self.htmlList = []
        return

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

    def authorLink(self, authorName, authorID):
        return "<a href='http://www.zhihu.com/people/{0}'>{1}</a>".format(authorID, authorName)

class updateDateTransfer(Transfer):
    def initQuestionList(self):
        self.questionList = self.package.format_sortBy_updateDate_asc()
        return

    def contentTrans(self):
        self.contentList  = []
        for question in self.questionList:
            contentHeader = {}
            contentHeader['titleName']  = question['title']
            if question['kind'] != 'article':
                contentHeader['titleImage'] = question['titleLogo']
            else:
                contentHeader['titleDesc']         = question['description']
                contentHeader['titleCommentCount'] = question['commentCount']

            
            content                  = {}
            content['contentHeader'] = contentHeaderTemplate(contentHeader)
            content['contentBody']   = ''
            content['contentFooter'] = ''

            for answer in question['answerList']: 
                contentBody = {}
                contentBody['authorLogo']   = self.imgFix(answer['authorLogo'])
                contentBody['authorName']   = self.authorLink(author['name'], answer['authorID'] )
                contentBody['authorSign']   = answer['authorSign']
                contentBody['content']      = self.imgFix(answer['content'])
                contentBody['agreeCount']   = answer['agreeCount']
                contentBody['commentCount'] = answer['commentCount']
                contentBody['updateDate']   = answer['updateDate'].isoformat()
                
                content['contentBody']      += contentBodyTemplate(contentBody)
            
            htmlContent = contentTemplate(content)
            htmlContent = structTemplate({'leftColumn' : '', 'middleColumn' : htmlContent, 'rightColumn' : ''})     
            htmlContent = baseTemplate({
                              'Title'  : question['title'],
                              'Header' : '',
                              'Body'   : htmlContent,
                              'Footer' : '',
                          })
            self.contentList.append(htmlContent)
        return self.contentList

    def infoPageTrans(self):
        u'''
        写了一天，没灵感了，临时凑活一下，下星期再做吧
        '''
        content = {}
        content['title']     = self.package['title']
        content['copyRight'] = u'此处应有版权声明。。。但作者实在想不出该写点啥了。。。今天已经连续写了十五个小时，作者表示下个版本再加版权声明。。。见谅则个XD'
        htmlContent = infoPageTemplate(content)
        htmlContent = structTemplate({'leftColumn' : '', 'middleColumn' : htmlContent, 'rightColumn' : ''})     
        htmlContent = baseTemplate({
                          'Title'  : self.package['title'],
                          'Header' : '',
                          'Body'   : htmlContent,
                          'Footer' : '',
                      })
        self.contentList.insert(0, htmlContent)
        return self.contentList

    def getResult(self):
        self.initQuestionList()
        self.infoPageTrans()
        self.contentTrans()
        return self.contentList

class AgreeCountTransfer(columnTrans):
    def initQuestionList(self):
        self.questionList = self.package.format_sortBy_agree_desc()
    
