# -*- coding: utf-8 -*-
class Filter(object):
    def __init__(self, cursor = None, filterDict = {}):
        self.cursor = cursor
        self.filterDict = filterDict
        self.sql = ''
        return

    def bufferInit(self):
        self.QuestionFilterList_Max   = ['maxFollow']
        self.QuestionFilterList_Min   = []
        self.AnswerFilterList_Max     = ['maxAgree', 'maxLength', 'maxDate', 'maxAnswerCommentCount']
        self.AnswerFilterList_Min     = ['minAgree', 'minLength', 'minDate', 'minAnswerCommentCount']
        self.TopicFilterList_Max      = []
        self.TopicFilterList_Min      = []
        self.CollectionFilterList_Max = []
        self.CollectionFilterList_Min = []
        self.TableFilterList_Max      = []
        self.TableFilterList_Min      = []
        self.AuthorFilterList_Max     = []
        self.AuthorFilterList_Min     = []

    
    def createSQL4Question(self):
        u'''利用这个函数查询出questionID, 然后在AnswerContent里取查询对应的答案数据'''
        AnswerList = 'select * from AnswerContent where questionID = ? '
        return
    
    def createSQL4Answer(self):
        return
    
    def createSQL4Topic(self):
        return

    def createSQL4Collection(self):
        return
    
    def createSQL4Table(self):
        return
    
    def createSQL4Author(self):
        return
    
    def createSQL4UserDefine(self):
        return
    
    def createSQL4Question(self):
        return
