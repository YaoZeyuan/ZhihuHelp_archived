# -*- coding: utf-8 -*-
import datetime
class baseFilter():
    '''
    先查出来所有的答案数据
    然后根据种类去查对应的辅助数据(比如问题信息)
    然后进行处理(图片下载，地址转换等)
    制成html文件使用epubBuilder生成电子书
    '''
    def __init__(self, cursor = None, kind = {}):
        return

class questionFilter(baseFilter):
    def __init__(self, cursor = None, urlInfo = {}):
        self.cursor = cursor
        self.questionID = urlInfo['questionID']
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
        questionInfo['questionDesc']  = bufDict[6]
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
                from AnswerContent where questionID = ? and noRecordFlag = 0'''
        bufList = self.cursor.execute(sql, [self.questionID,]).fetchall()
        answerDictList = []
        for answer in bufList:
            answerDict = {}
            answerDict['authorID']           = answer[0]
            answerDict['authorSign']         = answer[1]
            answerDict['authorLogo']         = answer[2]
            answerDict['authorName']         = answer[3]
            answerDict['answerAgreeCount']   = int(answer[4])
            answerDict['answerContent']      = answer[5]
            answerDict['questionID']         = answer[6]
            answerDict['answerID']           = answer[7]
            answerDict['commitDate']         = self.str2Date(answer[8])
            answerDict['updateDate']         = self.str2Date(answer[9])
            answerDict['answerCommentCount'] = int(answer[10])
            answerDict['noRecordFlag']       = bool(answer[11])
            answerDict['answerHref']         = answer[12]
            answerDictList.append(answerDict)

        self.answerDictList = answerDictList
        return answerDictList
    
    def str2Date(self, date = ''):
        return datetime.date.strptime(date, '%Y-%m-%d') 

    def getResult(self):
        self.result = {}
        self.result[self.questionInfo['questionID']] = {
                'question'   : self.questionInfo,
                'answerList' : self.answerList.sort(cmp=lambda x,y:cmp(x['answerAgreeCount'],y['answerAgreeCount']))
                }
        return self.result
