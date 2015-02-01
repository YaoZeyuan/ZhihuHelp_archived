# -*- coding: utf-8 -*-
import datetime
import re
class baseFilter():
    '''
    先查出来所有的答案数据
    然后根据种类去查对应的辅助数据(比如问题信息)
    然后进行处理(图片下载，地址转换等)
    制成html文件使用epubBuilder生成电子书
    '''
    def __init__(self, cursor = None, kind = {}):
        self.imgSet = set()
        self.imgBasePath = '../image/'
        return
    def getChapterFrontPage(self):
        infoDict = {
                'Title'    : '',
                'Author'   : '',
                'Desc'     : '',
                'GuideImg' : '',
                }
        return infoDict
    
    def authorLogoFix(self, imgHref = ''):
        self.imgSet.add(imgHref)
        return self.imgBasePath + self.getFileName(imgHref)

    def answerImgFix(self, answerContent = '', imgQuarty = 1):
        #只能用在Question/Answer的直接提取中，在这里面src不能直接使用，需要用data-actualsrc属性来辅助完成
        #if imgQuarty == 0:
        #    answerContent = self.removeTag(answerContent, ['img'])
        #else:
        #    if imgQuarty == 1:
        #        for imgTag in re.findall(r'<img.*?>', text):
        #            answerContent = answerContent.replace(imgTag, self.fixPic(self.removeTagAttribute(imgTag, ['data-original']).replace('data-rawheight', 'height')[:-1] + u' alt="知乎图片"/>'))
        #    else:
        #        for imgTag in re.findall(r'<img.*?>', text):
        #            try :
        #                imgTag.index('data-original')
        #            except  ValueError:
        #                #所考虑的这种情况存在吗？存疑
        #                answerContent = answerContent.replace(imgTag, self.fixPic(imgTag.replace('data-rawheight', 'height')[:-1] + u' alt="知乎图片"/>'))
        #            else:
        #                #将data-original替换为src即为原图
        #                answerContent = answerContent.replace(imgTag, self.fixPic(self.removeTagAttribute(imgTag, ['src']).replace('data-original', 'src').replace("data-rawheight", 'height')[:-1] + u' alt="知乎图片"/>'))

        if imgQuarty == 0:
            answerContent = self.removeTag(answerContent, ['img', 'noscript'])
        else:
            answerContent = self.removeTag(answerContent, ['noscript'])
            if imgQuarty == 1:
                for imgTag in re.findall(r'<img.*?>', text):
                    imgContent = self.removeTagAttribute(imgTag, ['data-original']).replace('data-actualsrc', 'src').replace('data-rawheight', 'height')[:-1] + u' alt="知乎图片"/>'
                    answerContent = answerContent.replace(imgTag, self.fixPic(imgContent))
            else:
                for imgTag in re.findall(r'<img.*?>', text):
                    try :
                        imgTag.index('data-original')
                    except  ValueError:
                        #所考虑的这种情况存在吗？存疑
                        answerContent = answerContent.replace(imgTag, self.fixPic(imgTag.replace('data-actualsrc', 'src').replace('data-rawheight', 'height')[:-1] + u' alt="知乎图片"/>'))
                    else:
                        #将data-original替换为src即为原图
                        answerContent = answerContent.replace(imgTag, self.fixPic(self.removeTagAttribute(imgTag, ['src']).replace('data-original', 'src').replace("data-rawheight", 'height')[:-1] + u' alt="知乎图片"/>'))
        
        return answerContent
    
    def fixNoScriptTag(self, content = ''):
        
        return

    def fixPic(self, imgTagContent = ''):
        for src in re.findall(r'(?<=src=")http://[/\w\.^"]*?zhimg.com[/\w^"]*?.jpg', imgTagContent):
            imgTagContent = imgTagContent.replace(src, self.imgBasePath + self.getFileName(src))
            self.imgSet.add(src)
        return '<div class="duokan-image-single">{}</div>'.format(imgTagContent)

    def removeTagAttribute(self, tagContent = '', removeAttrList = []):
        for attr in removeAttrList:
            for attrStr in re.findall(r'\s' + attr + '[^\s>]*', tagContent):
                tagContent = tagContent.replace(attrStr, '')
        return tagContent
    
    def removeTag(text='', tagname=[]):
        for tag in tagname:
            text = text.replace('</'+tag+'>', '')
            text = re.sub(r"<" + tag + r'.*?>', '', text)
        return text

    def getFileName(self, imgHref = ''):
        return imgHref.split('/')[-1]

class questionFilter(baseFilter):
    u'每运行一次filter就相当于生成了一本电子书，所以在这个里面也应当为之加上封面，最后输出时大不了再跳过封面输出就好了，电子书应当每个章节都有自己的封面，同时也要有一个总封面'
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
        return datetime.datetime.strptime(date, '%Y-%m-%d') 

    def getResult(self):
        self.result = {}
        self.getQuestionInfoDict()
        self.getAnswerContentDictList()
        self.result = {
                'questionInfo' : self.questionInfo,
                'answerList'   : sorted(self.answerDictList, key=lambda answerDict: answerDict['answerAgreeCount'], reverse=True)
                }
        agreeCount = 0
        for answerDict in self.result['answerList']:
            agreeCount += answerDict['answerAgreeCount']
        self.result['agreeCount']  = agreeCount
        self.result['answerCount'] = len(self.answerDictList)
        self.result['FrontDict']   = self.getChapterFrontPage()
        return self.result
        
    def printDict(data = {}, key = '', prefix = ''):
        if isinstance(data, dict):
            for key in data.keys():
                printDict(data[key], key, prefix + '   ')
        else:
            print prefix + str(key) + ' => ' + str(data)
    
