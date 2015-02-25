# -*- coding: utf-8 -*-
from baseClass import *

import datetime
import re

class BaseFilter(BaseClass):
    '''
    先查出来所有的答案数据
    然后根据种类去查对应的辅助数据(比如问题信息)
    然后进行处理(图片下载，地址转换等)
    制成html文件使用epubBuilder生成电子书
    '''
    def __init__(self, cursor = None, urlInfo = {}):
        self.imgSet      = set()
        self.imgBasePath = '../image/'
        self.cursor      = cursor
        self.urlInfo     = urlInfo
        self.picQuality  = urlInfo['baseSetting']['picQuality']
        self.addProperty()
        return

    def addProperty(self):
        return
    
    def authorLogoFix(self, imgHref = ''):
        self.imgSet.add(imgHref)
        return u'<div class="duokan-image-single"><img src="{}" alt="知乎图片"/></div>'.format(imgHref)

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
                    return '<img src="{}" alt="知乎图片">'.format(src)
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
    
    def getQuestionInfoDict(self):
        sql = '''select 
                questionIDinQuestionDesc         as questionID, 
                questionCommentCount             as commentCount, 
                questionFollowCount              as followCount,
                questionAnswerCount              as answerCount,       
                questionViewCount                as viewCount,
                questionTitle                    as questionTitle,
                questionDesc                     as questionDesc
                from QuestionInfo where questionIDinQuestionDesc = ?'''
        bufDict = self.cursor.execute(sql, [self.questionID,]).fetchone()
        questionInfo = {}
        questionInfo['questionID']    = bufDict[0]
        questionInfo['commentCount']  = bufDict[1]
        questionInfo['followCount']   = bufDict[2]
        questionInfo['answerCount']   = bufDict[3]
        questionInfo['viewCount']     = bufDict[4]
        questionInfo['questionTitle'] = bufDict[5]
        questionInfo['questionDesc']  = self.contentImgFix(bufDict[6], self.picQuality)
        self.questionInfo = questionInfo
        return questionInfo

    def getAnswerContentDictList(self):
        sql = '''select 
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
                from AnswerContent where questionID = ? and noRecordFlag = 0 and answerAgreeCount > 5'''
        bufList = self.cursor.execute(sql, [self.questionID,]).fetchall()
        answerListDict = {}
        for answer in bufList:
            answerDict = {}
            answerDict['authorID']           = answer[0]
            answerDict['authorSign']         = answer[1]
            answerDict['authorLogo']         = self.authorLogoFix(answer[2])
            answerDict['authorName']         = answer[3]
            answerDict['answerAgreeCount']   = int(answer[4])
            answerDict['answerContent']      = self.contentImgFix(answer[5], self.picQuality)
            answerDict['questionID']         = answer[6]
            answerDict['answerID']           = answer[7]
            answerDict['commitDate']         = self.str2Date(answer[8])
            answerDict['updateDate']         = self.str2Date(answer[9])
            answerDict['answerCommentCount'] = int(answer[10])
            answerDict['noRecordFlag']       = bool(answer[11])
            answerDict['answerHref']         = answer[12]
            answerListDict[answerDict['answerID']] = answerDict

        self.answerListDict = answerListDict
        return answerListDict

    def getResult(self):
        u'''
        self.result格式
        *   contentListDict
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
        self.getQuestionInfoDict()
        self.getAnswerContentDictList()


        self.result = {}
        result = {
                'questionInfo'   : self.questionInfo,
                'answerListDict' : self.answerListDict
                }
        self.result[result['questionInfo']['questionID']] = result
        return self.result
    
    def getInfoDict(self):
        infoDict = {}
        return infoDict

        
class AnswerFilter(QuestionFilter):
    def addProperty(self):
        self.questionID = self.urlInfo['questionID']
        self.answerID   = self.urlInfo['answerID']
        return

    def getAnswerContentDictList(self):
        sql = '''select 
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
                from AnswerContent where questionID = ? and answerID = ? and noRecordFlag = 0'''
        bufList = self.cursor.execute(sql, [self.questionID, self.answerID, ]).fetchall()
        answerListDict = {}
        for answer in bufList:
            answerDict = {}
            answerDict['authorID']           = answer[0]
            answerDict['authorSign']         = answer[1]
            answerDict['authorLogo']         = self.authorLogoFix(answer[2])
            answerDict['authorName']         = answer[3]
            answerDict['answerAgreeCount']   = int(answer[4])
            answerDict['answerContent']      = self.contentImgFix(answer[5], self.picQuality)
            answerDict['questionID']         = answer[6]
            answerDict['answerID']           = answer[7]
            answerDict['commitDate']         = self.str2Date(answer[8])
            answerDict['updateDate']         = self.str2Date(answer[9])
            answerDict['answerCommentCount'] = int(answer[10])
            answerDict['noRecordFlag']       = bool(answer[11])
            answerDict['answerHref']         = answer[12]
            answerListDict[answerDict['answerID']] = answerDict

        self.answerListDict = answerListDict
        return answerListDict

class AuthorFilter(QuestionFilter):
    def addProperty(self):
        self.authorID   = self.urlInfo['authorID']
        return

    def getQuestionInfoDict(self, questionID = ''):
        sql = '''select 
                questionIDinQuestionDesc         as questionID, 
                questionCommentCount             as commentCount, 
                questionFollowCount              as followCount,
                questionAnswerCount              as answerCount,       
                questionViewCount                as viewCount,
                questionTitle                    as questionTitle,
                questionDesc                     as questionDesc
                from QuestionInfo where questionIDinQuestionDesc = ?'''
        bufDict = self.cursor.execute(sql, [questionID,]).fetchone()
        questionInfo = {}
        questionInfo['questionID']    = bufDict[0]
        questionInfo['commentCount']  = bufDict[1]
        questionInfo['followCount']   = bufDict[2]
        questionInfo['answerCount']   = bufDict[3]
        questionInfo['viewCount']     = bufDict[4]
        questionInfo['questionTitle'] = bufDict[5]
        questionInfo['questionDesc']  = self.contentImgFix(bufDict[6], self.picQuality)
        self.questionInfo = questionInfo
        return questionInfo

    def getAnswerContentDictList(self):
        sql = '''select 
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
                from AnswerContent where authorID = ? and noRecordFlag = 0'''
        bufList = self.cursor.execute(sql, [self.authorID, ]).fetchall()
        answerListDict = {}
        for answer in bufList:
            answerDict = {}
            answerDict['authorID']           = answer[0]
            answerDict['authorSign']         = answer[1]
            answerDict['authorLogo']         = self.authorLogoFix(answer[2])
            answerDict['authorName']         = answer[3]
            answerDict['answerAgreeCount']   = int(answer[4])
            answerDict['answerContent']      = self.contentImgFix(answer[5], self.picQuality)
            answerDict['questionID']         = answer[6]
            answerDict['answerID']           = answer[7]
            answerDict['commitDate']         = self.str2Date(answer[8])
            answerDict['updateDate']         = self.str2Date(answer[9])
            answerDict['answerCommentCount'] = int(answer[10])
            answerDict['noRecordFlag']       = bool(answer[11])
            answerDict['answerHref']         = answer[12]
            answerListDict[answerDict['answerID']] = answerDict

        self.answerListDict = answerListDict
        return answerListDict

    def getResult(self):
        self.getAnswerContentDictList()
        self.result = {}
        for answerID in self.answerListDict:
            answerDict = self.answerListDict[answerID]
            if answerDict['questionID'] in self.result:
                self.result[answerDict['questionID']]['answerListDict'][answerDict['answerID']] = answerDict
            else:
                self.result[answerDict['questionID']] = {}
                self.result[answerDict['questionID']]['answerListDict'] = {}
                self.result[answerDict['questionID']]['answerListDict'][answerDict['answerID']] = answerDict
                self.result[answerDict['questionID']]['questionInfo'] = self.getQuestionInfoDict(answerDict['questionID'])

        return self.result

    def getInfoDict(self):
        infoDict = {}
        sql = 'select authorID, name from AuthorInfo where authorID = ?'
        authorID, name = self.cursor.execute(sql, [self.authorID,]).fetchone()
        infoDict['title'] = name
        infoDict['ID']    = authorID
        infoDict['href']  = 'http://www.zhihu.com/people/' + authorID
        return infoDict

class CollectionFilter(AuthorFilter):
    def addProperty(self):
        self.collectionID = self.urlInfo['collectionID']
        return

    def getIndexList(self):
        sql = 'select answerHref from CollectionIndex where collectionID = ?'
        indexTuple = self.cursor.execute(sql, [self.collectionID,]).fetchall()
        indexList  = []
        for index in indexTuple:
            indexList.append(index[0])
        return indexList

    def getAnswerContentDictList(self):
        indexList = self.getIndexList()
        sql = '''select 
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
                from AnswerContent where answerHref = ? and noRecordFlag = 0'''
        bufList = []
        for answerHref in indexList:
            buf = self.cursor.execute(sql, [answerHref, ]).fetchone()
            if buf == None :
                #noRecordFlag == True
                continue
            bufList.append(buf)
        answerListDict = {}
        for answer in bufList:
            answerDict = {}
            answerDict['authorID']           = answer[0]
            answerDict['authorSign']         = answer[1]
            answerDict['authorLogo']         = self.authorLogoFix(answer[2])
            answerDict['authorName']         = answer[3]
            answerDict['answerAgreeCount']   = int(answer[4])
            answerDict['answerContent']      = self.contentImgFix(answer[5], self.picQuality)
            answerDict['questionID']         = answer[6]
            answerDict['answerID']           = answer[7]
            answerDict['commitDate']         = self.str2Date(answer[8])
            answerDict['updateDate']         = self.str2Date(answer[9])
            answerDict['answerCommentCount'] = int(answer[10])
            answerDict['noRecordFlag']       = bool(answer[11])
            answerDict['answerHref']         = answer[12]
            answerListDict[answerDict['answerID']] = answerDict

        self.answerListDict = answerListDict
        return answerListDict

    def getInfoDict(self):
        infoDict = {}
        sql = 'select collectionID, title from CollectionInfo where collectionID = ?'
        collectionID, title = self.cursor.execute(sql, [self.collectionID,]).fetchone()
        infoDict['title'] = u'收藏夹_' + title
        infoDict['ID']    = collectionID
        infoDict['href']  = 'http://www.zhihu.com/collection/' + collectionID
        return infoDict

class TopicFilter(CollectionFilter):
    def addProperty(self):
        self.topicID = self.urlInfo['topicID']
        return

    def getIndexList(self):
        sql = 'select answerHref from TopicIndex where topicID = ?'
        indexTuple = self.cursor.execute(sql, [self.topicID, ]).fetchall()
        indexList  = []
        for index in indexTuple:
            indexList.append(index[0])
        return indexList

    def getInfoDict(self):
        infoDict = {}
        sql = 'select topicID, title from TopicInfo where topicID = ?'
        topicID, title = self.cursor.execute(sql, [self.topicID,]).fetchone()
        infoDict['title'] = '话题_' + title
        infoDict['ID']    = topicID
        infoDict['href']  = 'http://www.zhihu.com/topic/' + topicID
        return infoDict
