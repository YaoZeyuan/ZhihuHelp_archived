# -*- coding: utf-8 -*-

class AnswerFilter():
    def __init__(self,conn):
        self.conn = conn
        self.sql  = u''
        self.queryDict = {}
        return
    
    def printSql(self):
        print self.sql
        return

    def AnswerFilter(self, answerList = []):
        answerFilter = u"answerID in '"
        for answerID in answerList:
            answerFilter += '%s, '%answerID
        self.queryDict['answerFilter'] = answerFilter[:-1] + "'"
        return 

    def 
