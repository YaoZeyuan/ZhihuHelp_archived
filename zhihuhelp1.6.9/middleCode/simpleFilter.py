# -*- coding: utf-8 -*-
import datetime
import re

class ImgDownloader():
    u'''
     负责下载图片到指定文件夹内 
    '''
    def __init__(self, targetDir = '', maxThread = 5, maxTry = 5, imgSet = set()):
        self.targetDir  = targetDir
        self.maxThread  = maxThread
        self.imgSet     = imgSet
        self.threadPool = []
        self.complete   = set()
    
    def leader(self):
        threadPool = []
        for img in self.imgSet:
            threadPool.append(threading.Thread(target=self.worker, kwargs={'link':key}))
        threadsCount = len(threadPool)
        threadLiving = 2
        while (threadsCount > 0 or threadLiving > 1):
            print 'threading.activeCount() = {}'.format(threadLiving)
            bufLength = self.maxThread - threadLiving
            if bufLength > 0 and threadsCount > 0:
                while bufLength > 0 and threadsCount > 0:
                    threadPool[threadsCount - 1].start()
                    bufLength    -= 1
                    threadsCount -= 1
                    time.sleep(0.1)
            else:
                print u'正在下载图片，还有{}/{}张图片等待读取'.format(len(self.workSchedule) - len(self.complete), len(self.workSchedule))
                time.sleep(1)
            threadLiving = threading.activeCount()
        print 'download complete'
        return

    def worker(self, link = ''):
        u"""
        worker只执行一次，待全部worker执行完毕后由调用函数决定哪些worker需要再次运行
        重复的次数由self.maxTry指定
        这样可以给知乎服务器留出生成页面缓存的时间
        """
        if link in self.complete:
            return
        content = self.getHttpContent(url = link, timeout = self.waitFor)
        if content == '':
            return
        fileName = self.getFileName(link)
        imgFile  = open(self.targetDir + fileName, 'wb')
        imgFile.write(content)
        imgFile.close()
        self.complete.add(workNo)
        return 

    def getHttpContent(self, url='', extraHeader={} , data=None, timeout=5):
        u"""获取网页内容
     
        获取网页内容, 打开网页超过设定的超时时间则报错
        
        参数:
            url         一个字符串,待打开的网址
            extraHeader 一个简单字典,需要添加的http头信息
            data        需传输的数据,默认为空
            timeout     int格式的秒数，打开网页超过这个时间将直接退出，停止等待
        返回:
            pageContent 打开成功时返回页面内容，字符串或二进制数据|失败则返回空字符串
        报错:
            IOError     当解压缩页面失败时报错
        """
        if data == None:
            request = urllib2.Request(url = url)
        else:
            request = urllib2.Request(url = url, data = data)
        #add default extra header
        for headerKey in self.extraHeader.keys():
            request.add_header(headerKey, self.extraHeader[headerKey])
        #add userDefined header
        for headerKey in extraHeader.keys():
            request.add_header(headerKey, extraHeader[headerKey])
        try: 
            rawPageData = urllib2.urlopen(request, timeout = timeout)
        except  urllib2.HTTPError as error:
            print u'网页打开失败'
            print u'错误页面:' + url
            if hasattr(error, 'code'):
                print u'失败代码:' + str(error.code)
            if hasattr(error, 'reason'):
                print u'错误原因:' + error.reason
        except  urllib2.URLError as error:
            print u'网络连接异常'
            print u'错误页面:' + url
            print u'错误原因:'
            print error.reason
        except  socket.timeout as error:
            print u'打开网页超时'
            print u'超时页面' + url
        else:
            return self.decodeGZip(rawPageData)
        return ''

    def decodeGZip(self, rawPageData):
        u"""返回处理后的正常网页内容
     
        判断网页内容是否被压缩，无则直接返回，若被压缩则使用zlip解压后返回
        
        参数:
            rawPageData   urlopen()传回的fileLike object
        返回:
            pageContent   页面内容，字符串或二进制数据|解压缩失败时则返回空字符串
        报错:
            无
        """
        if rawPageData.info().get(u"Content-Encoding") == "gzip":
            try:
                pageContent = zlib.decompress(rawPageData.read(), 16 + zlib.MAX_WBITS)
            except zlib.error as ziperror:
                print u'解压出错'
                print u'出错解压页面:' + rawPageData.geturl()
                print u'错误信息：'
                print zliberror
                return ''
        else:
            pageContent = rawPageData.read()
            return pageContent

    def getFileName(self, imgHref = ''):
        return imgHref.split('/')[-1]

class BaseFilter():
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
        self.addProperty()
        return

    def addProperty(self):
        return
    
    def authorLogoFix(self, imgHref = ''):
        self.imgSet.add(imgHref)
        #return self.imgBasePath + self.getFileName(imgHref)
        return '<img src="{}"/>'.format(imgHref)

    def contentImgFix(self, content = '', imgQuarty = 1):
        if imgQuarty == 0:
            content = self.removeTag(content, ['img', 'noscript'])
        else:
            #将writedot.jpg替换为正常图片
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
                        
            if imgQuarty == 1:
                for imgTag in re.findall(r'<img.*?>', content):
                    imgContent = imgTag[:-1] + u'class="answer-content-img" alt="知乎图片"/>'
                    content = content.replace(imgTag, self.fixPic(imgContent))
            else:
                for imgTag in re.findall(r'<img.*?>', content):
                    try :
                        imgTag.index('data-original')
                    except  ValueError:
                        #所考虑的这种情况存在吗？存疑
                        content = content.replace(imgTag, self.fixPic(imgTag[:-1] + u'class="answer-content-img" alt="知乎图片"/>'))
                    else:
                        #将data-original替换为src即为原图
                        content = content.replace(imgTag, self.fixPic(self.removeTagAttribute(imgTag, ['src']).replace('data-original', 'src')[:-1] + u'class="answer-content-img" alt="知乎图片"/>'))
        
        return content

    def fixPic(self, imgTagContent = ''):
        return imgTagContent
        #for src in re.findall(r'(?<=src=")http://[/\w\.^"]*?zhimg.com[/\w^"]*?.jpg', imgTagContent):
        #    imgTagContent = imgTagContent.replace(src, self.imgBasePath + self.getFileName(src))
        #    self.imgSet.add(src)
        #return '<div class="duokan-image-single">{}</div>'.format(imgTagContent)

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

    def printDict(data = {}, key = '', prefix = ''):
        u'''
        用于测试字典内容是否与要求一致
        '''
        if isinstance(data, dict):
            for key in data.keys():
                printDict(data[key], key, prefix + '   ')
        else:
            print prefix + str(key) + ' => ' + str(data)


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
        questionInfo['questionDesc']  = self.contentImgFix(bufDict[6])
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
        answerListDict = {}
        for answer in bufList:
            answerDict = {}
            answerDict['authorID']           = answer[0]
            answerDict['authorSign']         = answer[1]
            answerDict['authorLogo']         = self.authorLogoFix(answer[2])
            answerDict['authorName']         = answer[3]
            answerDict['answerAgreeCount']   = int(answer[4])
            answerDict['answerContent']      = self.contentImgFix(answer[5])
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
        self.result[result['questionInfo'][questionID]] = result
        return self.result
        
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
            answerDict['answerContent']      = self.contentImgFix(answer[5])
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
        self.authorID   = self.urlInfo['author']
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
        bufDict = self.cursor.execute(sql, [self.questionID,]).fetchone()
        questionInfo = {}
        questionInfo['questionID']    = bufDict[0]
        questionInfo['commentCount']  = bufDict[1]
        questionInfo['followCount']   = bufDict[2]
        questionInfo['answerCount']   = bufDict[3]
        questionInfo['viewCount']     = bufDict[4]
        questionInfo['questionTitle'] = bufDict[5]
        questionInfo['questionDesc']  = self.contentImgFix(bufDict[6])
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
            answerDict['answerContent']      = self.contentImgFix(answer[5])
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
        self.getQuestionInfoDict()
        self.getAnswerContentDictList()

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
