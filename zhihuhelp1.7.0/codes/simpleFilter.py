# -*- coding: utf-8 -*-
from baseClass import *
from contentPackage import *

import datetime
import re


class BaseFilter(BaseClass):
    '''
    Filter只负责查询出所有数据
    由Package负责数据保存
    由其他中间件负责将保存下来的数据转换成HTML代码
    '''
    def __init__(self, cursor = None, urlInfo = {}):
        self.imgBasePath = '../image/'
        self.cursor      = cursor
        self.urlInfo     = urlInfo
        self.picQuality  = urlInfo['baseSetting']['picQuality']
        self.package     = ContentPackage()
        self.addProperty()
        return

    def addProperty(self):
        return
    
    def authorLogoFix(self, imgHref = ''):
        #头像一律使用大图
        imgHref = re.sub(r'_..jpg', '', imgHref, 1) 
        if imgHref:
            imgHref += '_b.jpg'
        return u'<div class="duokan-image-single"><img src="{}" alt=""/></div>'.format(imgHref)

    def contentImgFix(self, content = '', imgQuarty = 1):
        if imgQuarty == 0:
            content = self.removeTag(content, ['img', 'noscript'])
        else:
            #首先，将writedot.jpg替换为正常图片
            content = self.removeTag(content, ['noscript'])
            for imgTag in re.findall(r'<img.*?>', content):
                try:
                    imgTag.index('misc/whitedot.jpg')
                except:
                    imgContent = imgTag.replace('data-rawwidth', 'width')
                    imgContent = self.removeTagAttribute(imgContent, ['class'])
                    content = content.replace(imgTag, imgContent) 
                else:
                    content = content.replace(imgTag, '')

            #然后,抽取它的src属性，直接手工新写一个img标签
            if imgQuarty == 1:
                for imgTag in re.findall(r'<img.*?>', content):
                    imgContent = self.trimImg(imgTag)
                    content = content.replace(imgTag, self.fixPic(imgContent))
            else:
                for imgTag in re.findall(r'<img.*?>', content):
                    try :
                        imgTag.index('data-original')
                    except ValueError:
                        #所考虑的这种情况存在吗？存疑
                        content = content.replace(imgTag, self.fixPic(self.trimImg(imgTag)))
                    else :
                        #将data-original替换为src即为原图
                        imgContent = self.removeTagAttribute(imgTag, ['src']).replace('data-original', 'src')
                        imgContent = self.trimImg(imgContent)
                        content = content.replace(imgTag, self.fixPic(imgContent))
        return content

    def trimImg(self, imgContent = ''):
        src = re.search(r'(?<=src=").*?(?=")', imgContent)
        if src != None:
            src = src.group(0)
            if src.replace(' ', '') != '':
                    return '<img src="{}" alt="">'.format(src)
        return ''

    def fixPic(self, imgTagContent = ''):
        #return imgTagContent
        return '\n<div class="duokan-image-single">\n{}\n</div>\n'.format(imgTagContent)

    def removeTagAttribute(self, tagContent = '', removeAttrList = []):
        for attr in removeAttrList:
            for attrStr in re.findall(r'\s' + attr + '[^\s>]*', tagContent):
                tagContent = tagContent.replace(attrStr, '')
        return tagContent
    
    def removeTag(self, text='', tagname=[]):
        for tag in tagname:
            text = text.replace('</'+tag+'>', '')
            text = re.sub(r"<" + tag + r'.*?>', '', text)
        return text

    def getFileName(self, imgHref = ''):
        return imgHref.split('/')[-1]

    def str2Date(self, date = ''):
        return datetime.datetime.strptime(date, '%Y-%m-%d') 

class QuestionFilter(BaseFilter):
    u'每运行一次filter就相当于生成了一本电子书，所以在这个里面也应当为之加上封面，最后输出时大不了再跳过封面输出就好了，电子书应当每个章节都有自己的封面，同时也要有一个总封面'
    def addProperty(self):
        self.questionID = self.urlInfo['questionID']
        return
    
    def initQuestionPackage(self, questionID = ''):
        sql = '''select 
                questionIDinQuestionDesc         as questionID, 
                questionCommentCount             as commentCount, 
                questionFollowCount              as followCount,
                questionAnswerCount              as answerCount,       
                questionViewCount                as viewCount,
                questionTitle                    as questionTitle,
                questionDesc                     as questionDesc
                from QuestionInfo where questionIDinQuestionDesc = ? '''
        bufDict = self.cursor.execute(sql, [questionID,]).fetchone()

        questionInfo = {}
        questionInfo['kind']          = 'question'
        questionInfo['questionID']    = bufDict[0]
        questionInfo['commentCount']  = bufDict[1]
        questionInfo['followerCount'] = bufDict[2]
        questionInfo['answerCount']   = bufDict[3]
        questionInfo['viewCount']     = bufDict[4]
        questionInfo['title']         = bufDict[5]
        questionInfo['description']   = self.contentImgFix(bufDict[6], self.picQuality)

        package = QuestionPackage()
        package.setPackage(questionInfo)
        return package

    def addAnswerTo(self, questionPackage, answerHref = ''):
        questionID = questionPackage['questionID']
        baseSql    = '''select 
                            authorID,
                            authorSign,
                            authorLogo,
                            authorName,
                            answerAgreeCount,
                            answerContent,
                            questionID,
                            answerID,
                            commitDate,
                            updateDate,
                            answerCommentCount,
                            noRecordFlag,
                            answerHref
                        from AnswerContent where noRecordFlag = 0 '''
        if answerHref :
            sql = baseSql + '''and answerHref = ?'''
            bufList = self.cursor.execute(sql, [answerHref]).fetchall()
        else:
            sql = baseSql + '''and questionID = ? and answerAgreeCount > 5'''
            bufList = self.cursor.execute(sql, [questionID,]).fetchall()
        
        for answer in bufList:
            package = AnswerPackage()
            answerDict = {}
            answerDict['authorID']           = answer[0]
            answerDict['authorSign']         = answer[1]
            answerDict['authorLogo']         = self.authorLogoFix(answer[2])
            answerDict['authorName']         = answer[3]
            answerDict['agreeCount']         = int(answer[4])
            answerDict['content']            = self.contentImgFix(answer[5], self.picQuality)
            answerDict['questionID']         = answer[6]
            answerDict['answerID']           = answer[7]
            answerDict['updateDate']         = self.str2Date(answer[9])
            answerDict['commentCount']       = int(answer[10])

            package.setPackage(answerDict)
            questionPackage.addAnswer(package)
        
        return questionPackage

    def addInfo(self):
        u'''
        问题信息
        '''
        sql = '''select 
                questionIDinQuestionDesc as questionID, 
                questionCommentCount     as commentCount, 
                questionFollowCount      as followCount,
                questionAnswerCount      as answerCount,       
                questionViewCount        as viewCount,
                questionTitle            as questionTitle,
                questionDesc             as questionDesc
                from QuestionInfo where questionIDinQuestionDesc = ? '''
        result   = self.cursor.execute(sql, [self.questionID,]).fetchone()
        infoDict = {}
        infoDict['ID']             = self.questionID
        infoDict['kind']           = 'question'
        infoDict['title']          = result[5]
        infoDict['description']    = result[6]
        infoDict['followerCount'] = result[2]
        infoDict['commentCount']   = result[1]
        
        self.package.setPackage(infoDict)
        return 

    def getResult(self):
        questionPackage = self.initQuestionPackage(self.questionID)
        questionPackage = self.addAnswerTo(questionPackage)

        self.package.addQuestion(questionPackage)
        self.addInfo()
        return self.package
        
class AnswerFilter(QuestionFilter):
    def addProperty(self):
        self.questionID = self.urlInfo['questionID']
        self.answerID   = self.urlInfo['answerID']
        return
    
    def createAnswerHref(self, questionID, answerID):
        return 'http://www.zhihu.com/question/{0}/answer/{1}'.format(questionID, answerID)

    def getResult(self):
        questionPackage = self.initQuestionPackage(self.questionID)
        answerHref      = self.createAnswerHref(self.questionID, self.answerID)
        questionPackage = self.addAnswerTo(questionPackage, answerHref)

        self.package.addQuestion(questionPackage)
        self.addInfo()
        return self.package

class AuthorFilter(AnswerFilter):
    def addProperty(self):
        self.authorID   = self.urlInfo['authorID']
        return

    def getIndexList(self):
        sql = '''select questionID, answerID from AnswerContent where authorID = ? and noRecordFlag = 0 '''
        resultList = self.cursor.execute(sql, [self.authorID, ]).fetchall()
        indexList  = []
        for questionID, answerID in resultList:
            indexList.append((questionID, self.createAnswerHref(questionID, answerID)))
        return indexList

    def addInfo(self):
        u'''
            添加用户信息
        '''
        sql = '''select authorID          
                        ,sign              
                        ,name              
                        ,authorLogoAddress 
                        ,desc              
                        ,follower          
                        ,answer            
                from AuthorInfo where authorID = ? '''
        result   = self.cursor.execute(sql, [self.authorID,]).fetchone()
        infoDict = {}
        infoDict['creatorID']     = result[0] 
        infoDict['creatorSign']   = result[1]   
        infoDict['creatorName']   = result[2]   
        infoDict['creatorLogo']   = result[3]   
        infoDict['ID']            = result[0]
        infoDict['kind']          = 'author'
        infoDict['title']         = result[2]
        infoDict['logo']          = result[3]
        infoDict['description']   = result[4]   
        infoDict['followerCount'] = result[5]     
        
        self.package.setPackage(infoDict)
        return 

    def getResult(self):
        resultList = self.getIndexList()
        for result in resultList:
            (questionID, answerHref) = result
            questionPackage = self.initQuestionPackage(questionID)
            questionPackage = self.addAnswerTo(questionPackage, answerHref)
            self.package.addQuestion(questionPackage)

        self.addInfo()
        return self.package


class CollectionFilter(AuthorFilter):
    def addProperty(self):
        self.collectionID = self.urlInfo['collectionID']
        return

    def getIndexList(self):
        sql = 'select answerHref from CollectionIndex where collectionID = ? '
        indexTuple = self.cursor.execute(sql, [self.collectionID,]).fetchall()
        indexList  = []
        for index in indexTuple:
            answerHref = index[0]
            questionID = answerHref.split('/')[-3]
            indexList.append((questionID, answerHref))
        return indexList

    def addInfo(self):
        u'''
        之前图省事，没抓取创建者的头像，以后要加上
        今天时间比较紧张了已经，所以，就先不加新功能了
        '''
        sql = 'select authorID, authorName, authorSign, title, description, followerCount, commentCount  from CollectionInfo where collectionID = ? '
        result = self.cursor.execute(sql, [self.collectionID,]).fetchone()
        infoDict = {}
        infoDict['creatorID']      = result[0]
        infoDict['creatorName']    = result[1]
        infoDict['creatorSign']    = result[2]
        infoDict['ID']             = self.collectionID
        infoDict['kind']           = 'collection'
        infoDict['title']          = result[3]
        infoDict['description']    = result[4]
        infoDict['followerCount'] = result[5]
        infoDict['commentCount']   = result[6]
        
        self.package.setPackage(infoDict)
        return 

    def getResult(self):
        resultList = self.getIndexList()
        for result in resultList:
            (questionID, answerHref) = result
            questionPackage = self.initQuestionPackage(questionID)
            questionPackage = self.addAnswerTo(questionPackage, answerHref)
            self.package.addQuestion(questionPackage)

        self.addInfo()
        return self.package

class TopicFilter(CollectionFilter):
    def addProperty(self):
        self.topicID = self.urlInfo['topicID']
        return

    def getIndexList(self):
        sql = 'select answerHref from TopicIndex where topicID = ? '
        indexTuple = self.cursor.execute(sql, [self.topicID, ]).fetchall()
        indexList  = []
        for index in indexTuple:
            answerHref = index[0]
            questionID = answerHref.split('/')[-3]
            indexList.append((questionID, answerHref))
        return indexList
            
    def addInfo(self):
        sql = 'select title, logoAddress, description, followerCount from TopicInfo where topicID = ? '
        result = self.cursor.execute(sql, [self.topicID,]).fetchone()

        infoDict = {}
        infoDict['ID']            = self.topicID
        infoDict['kind']          = 'topic'
        infoDict['title']         = result[0]
        infoDict['logo']          = result[1]
        infoDict['description']   = result[2]
        infoDict['followerCount'] = result[3]
        self.package.setPackage(infoDict)
        return 

class ColumnFilter(BaseFilter):
    u''' '''
    def addProperty(self):
        self.columnID = self.urlInfo['columnID']
        return
    
    def initArticlePackage(self, columnID = '', articleID = ''):
        '''
        对问题信息和问题内容的收集可以一次解决
        '''
        baseSql = '''select authorID        
                            ,authorSign      
                            ,authorLogo      
                            ,authorName      

                            ,columnID        
                            ,columnName      
                            ,articleID       
                            ,articleHref     
                            ,title           
                            ,titleImage      
                            ,articleContent  
                            ,commentCount    
                            ,likeCount      
                            ,publishedTime
                    from ArticleContent where '''
        if articleID:
            sql        = baseSql + 'columnID = ? and articleID = ?'
            resultList = self.cursor.execute(sql, [columnID, articleID]).fetchall()
        else:
            sql        = baseSql + 'columnID = ?'
            resultList = self.cursor.execute(sql, [columnID,]).fetchall()

        for result in resultList:
            titlePackage  = QuestionPackage() 
            contentPackage = AnswerPackage()
            titleInfo = {}
            titleInfo['questionID'] = '{columnID}_{articleID}'.format(columnID=result[4], articleID=result[6]) 
            titleInfo['kind']       = 'article' 
            titleInfo['title']      = result[8] 
            titleInfo['titleLogo']  = result[9]
            titlePackage.setPackage(titleInfo)

            contentInfo = {}
            contentInfo['authorID']     = result[0]  
            contentInfo['authorSign']   = result[1] 
            contentInfo['authorLogo']   = self.authorLogoFix(result[2])
            contentInfo['authorName']   = result[3] 
            contentInfo['questionID']   = titleInfo['questionID']
            contentInfo['answerID']     = result[6] 
            contentInfo['content']      = self.contentImgFix(result[10], self.picQuality)
            contentInfo['updateDate']   = self.str2Date(result[13])
            contentInfo['agreeCount']   = result[12] 
            contentInfo['commentCount'] = result[11] 
            contentPackage.setPackage(contentInfo)

            titlePackage.addAnswer(contentPackage)
            self.package.addQuestion(titlePackage)
        return

    def getResult(self):
        self.initArticlePackage(self.columnID)
        self.addInfo()
        return self.package

    def addInfo(self):
        sql = '''select creatorID, creatorSign, creatorName, creatorLogo, columnName, columnLogo, description, followerCount from ColumnInfo where columnID = ? '''
        result = self.cursor.execute(sql, [self.columnID,]).fetchone()
        infoDict = {}
        infoDict['creatorID']     = result[0]   
        infoDict['creatorSign']   = result[1]   
        infoDict['creatorName']   = result[2]   
        infoDict['creatorLogo']   = result[3]   
        infoDict['ID']            = self.columnID   
        infoDict['kind']          = 'column'
        infoDict['title']         = result[4]   
        infoDict['logo']          = result[5]   
        infoDict['description']   = result[6]   
        infoDict['followerCount'] = result[7]
        self.package.setPackage(infoDict)
        return 

class ArticleFilter(ColumnFilter):
    def addProperty(self):
        self.columnID  = self.urlInfo['columnID']
        self.articleID = self.urlInfo['articleID']
        return

    def getResult(self):
        self.initArticlePackage(self.columnID, self.articleID)
        self.addInfo()
        return self.package
