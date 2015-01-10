# -*- coding: utf-8 -*-

class AnswerFilter():
    def __init__(self,conn):
        self.conn = conn
        self.sql  = u''
        self.queryDict = {}
        return
    
    def printSql(self):
        sql = u'select * from '
        return

    def AnswerFilter(self, answerIDList = []):
        answerFilter = u"answerID in '"
        for answerID in answerIDList:
            answerFilter += '%s, '%answerID
        self.queryDict['answerFilter'] = answerFilter.lstrip(', ') + "'"
        return 

    def AuthorFilter(self, authorIDList = []):
        authorFilter = u "authorID in '"
        for authorID in authorIDList:
            authorFilter += '%s, '%authorID
        self.queryDict['authorFilter'] = authorFilter.lstrip(', ') + "'"
        return
    
