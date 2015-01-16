# -*- coding: utf-8 -*-

from contentParse import ParseQuestion

class PageWorker(object):
    def __init__(self, conn = None, maxThread = 1, targetUrl = ''):
        self.conn         = conn
        self.cursor       = conn.cursor()
        self.maxPage      = ''
        self.maxThread    = maxThread
        self.url          = targetUrl
        self.suffix       = ''
        self.workSchedule = {}
        self.addProperty()

    def getMaxPage(self, content):
        try:
            pos      = content.index(u'">下一页</a></span>')
            rightPos = content.rfind(u"</a>",0,pos)
            leftPos  = content.rfind(u">",0,rightPos)
            maxPage  = int(content[leftPos+1:rightPos])
            print u"答案列表共计{}页".format(maxPage)
            return maxPage
        except:
            print u"答案列表共计1页"
            return 1
    
    def setWorkSchedule(self):
        content      = getHttpContent(self.url + self.suffix + str(self.maxPage))
        self.maxPage = self.getMaxPage(content)
        for i in range(self.maxPage):
            self.workSchedule[i] = self.url + self.suffix + str(i)
    
    def addProperty(self):
        return

class QuestionWorker(PageWorker):
    def boss(self):
        maxTry = self.maxTry
        while maxTry > 0 and len(self.workSchedule) > 0:
            self.leader()
            maxTry -= 1
        return 
    
    def leader(self):
        threadPool = []
        for key in self.workSchedule:
            threadPool.append(threading.Thread(target=self.worker, args=(key)))

        threadsCount = len(threadPool)
        while threadCount > 0:
            bufCount = self.maxThread - threading.activeCount()
            if bufCount > 0:
                while bufCount > 0 and threadCount > 0:
                    threadPool[threadsCount - 1].start()
                    bufCount    -= 1
                    threadCount -= 1
                    time.sleep(0.1)
            else:
                print u'正在读取答案页面，还有{}张页面等待读取'.format(threadCount)
                time.sleep(1)
        self.conn.commit()
    
    def worker(self, workNo = 0):
        u"""
        worker只执行一次，待全部worker执行完毕后由调用函数决定哪些worker需要再次运行
        重复的次数由self.maxTry指定
        这样可以给知乎服务器留出生成页面缓存的时间
        """
        content = getHttpContent(url = self.workSchedule[workNo], timeout = self.waitFor)
        if content == '':
            return
        parse = ParseQuestion(content)
        questionInfoDict, answerDictList = parse.getInfoDict()
        save2DB(self.cursor, questionInfoDict, 'questionID', 'QuestionInfo')
        for answerDict in answerDictList:
            save2DB(self.cursor, answerDict, 'answerHref', 'AnswerContent')
        del self.workSchedule[i]
        return 

    def addProperty(self):
        self.maxPage   = 1
        self.suffix    = '?sort=created&page='
        self.maxTry    = 5
        self.waitFor   = 5
        return
"""
class JsonWorker:
"""
