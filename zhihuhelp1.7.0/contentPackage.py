# -*- coding: utf-8 -*-
from baseClass import *

class Package(BaseClass):
    u'''
    package基础类
    用于保存Filer中取出的数据
        *   extraInfo
            *   creatorID
            *   creatorSign
            *   creatorName
            *   creatorLogo
            *   ID
                *   专栏/话题/收藏夹的ID
            *   kind
                *   类别（专栏/话题/收藏夹/问题合集）
            *   title
            *   logo
            *   description
            *   followerCount
            *   commentCount
            *   contentCount
                *   文章总数/答案总数/问题总数等
            *   extraKey
                *   留作日后扩展
            *   questionDict
                *   question作为extra的扩展属性
                *   以questionID作为标记
                *   [questionID]
                    *   key值
                *   Question
                    *   questionID
                    *   kind
                        *   类别(专栏文章/知乎问题)
                    *   title
                    *   desc
                    *   updateDate
                    *   commentCount
                    *   followerCount
                    *   viewCount
                    *   answerCount
                    *   extraKey
                        *   留作日后扩展
                    *   answerDict
                        *   Answer作为Question的扩展属性
                        *   以answerID作为标记
                        *   [answerID]
                            *   key值
                        *   Answer
                            *   authorID
                            *   authorSign
                            *   authorLogo
                            *   authorName
                            *   questionID
                            *   answerID
                            *   content
                            *   updateDate
                            *   agreeCount
                            *   collectCount
                            *   extraKey
                                *   留作日后扩展
    在最外层，还可以再打一层包XD
    '''
    def __init__(self):
        self.package = {}
        self.initPackage()
        return

    def initPackage(self):
        return

    def setPackage(self, dataDict):
        for key in dataDict:
            self.package[key] = dataDict[key]
        return

    def getResult(self):
        return self.package

class ContentPackage(Package):
    u'''
    '''
    def initPackage(self):
        self.package['creatorID']     = ''
        self.package['creatorSign']   = ''
        self.package['creatorName']   = ''
        self.package['creatorLogo']   = ''
        self.package['ID']            = ''
        self.package['kind']          = ''
        self.package['title']         = ''
        self.package['logo']          = ''
        self.package['description']   = ''
        self.package['followerCount'] = 0
        self.package['commentCount']  = 0
        self.package['followerCount'] = 0
        self.package['contentCount']  = 0
        self.package['extraKey']      = {}
        self.package['questionDict']  = {}

        self.questionDict = self.package['questionDict']
    
    def addQuestion(self, questionPackage):
        questionID = questionPackage['questionID']
        if questionID in self.questionDict:
            self.questionDict[questionID].merge(questionPackage)
        else:
            self.questionDict[questionID]  = questionPackage
        return

    def merge(self, contentPackage):
        u'''
        把内容合并后再把种类改成merge即可。
        合并产生的内容没有必要再去控制它的额外属性了。
        没有意义
        最后发布前自己想一个填充上即可
        '''
        self.package['kind'] = 'merge'
        for key in contentPackage['questionDict']:
            self.addQuestion(contentPackage['questionDict']['key'])
        return

    def getResult(self):
        self.package['contentCount'] = len(self.questionDict)
        return self.package

class QuestionPackage(Package):
    u'''
    专栏文章和问题的kind要分开
    其ID命名规则为
    问题ID为"question_{questionID}".format(questionID)
    专栏ID为"{columnID}_{articleID}".format(columnID, articleID)
    其中titleLogo项专为专栏文章使用
    字典结构:
    *   Question
        *   questionID
        *   kind
        *   title
        *   titleLogo
        *   desc
        *   updateDate
        *   commentCount
        *   followerCount
        *   viewCount
        *   answerCount
        *   extraKey
            *   留作日后扩展
        *   answerDict
            *   存储答案内容，使用answerID/articleID做key
    '''
    def initPackage(self):
        self.package['questionID']    = '' 
        self.package['kind']          = '' 
        self.package['title']         = '' 
        self.package['titleLogo']     = '' 
        self.package['desc']          = '' 
        self.package['updateDate']    = '' 
        self.package['commentCount']  = 0  
        self.package['viewCount']     = 0 
        self.package['answerCount']   = 0 
        self.package['followerCount'] = 0
        self.package['extraKey']      = {}
        self.package['answerDict']    = {}

        self.answerDict = self.package['answerDict']

    def addAnswer(self, answerPackage):
        u'''
        answer中没有多少需要合并的信息，所以不对answer调用merge方法
        '''
        answerID = answerPackage['answerID']
        if not answerID in self.answerDict:
            self.answerDict[answerID] = answerPackage
        return
    
    def merge(self, questionPackage):
        if questionPackage['kind'] != self.package['kind']:
            return
        for key in ['title', 'titleLogo', 'desc', 'updateDate']:
            if questionPackage[key] != '':
                self.package[key] = questionPackage[key]

        for key in questionPackage['answerDict']:
            self.addAnswer(questionPackage['answerDict'][key])

        return

    def getResult(self):
        self.package['answerCount'] = len(self.answerDict)
        return self.package
        
class AnswerPackage(Package):
    u'''
    数据结构
    其中，对于Article而言，questionID即为columnID,answerID即为articleID
    *   Answer
        *   author
            *   authorID
            *   authorSign
            *   authorLogo
            *   authorName
        *   questionID
        *   answerID
        *   content
        *   updateDate
        *   agreeCount
        *   collectCount
        *   extraKey
            *   留作日后扩展
    '''
    def initPackage(self):
        self.package['authorID']     = ''
        self.package['authorSign']   = ''
        self.package['authorLogo']   = ''
        self.package['authorName']   = ''
        self.package['questionID']   = '' 
        self.package['answerID']     = '' 
        self.package['content']      = '' 
        self.package['updateDate']   = '' 
        self.package['agreeCount']   = 0
        self.package['collectCount'] = 0 
        self.package['extraKey']     = {} 
        return
