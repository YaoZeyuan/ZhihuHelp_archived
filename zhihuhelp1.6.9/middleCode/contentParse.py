# -*- coding: utf-8 -*-
import re
import HTMLParser #转换网页代码
import time #简单处理时间
class Parse(object):
    def __init__(self, content):
        self.content = content.replace('\r', '').replace('\n', '')
        self.initRegex()
        self.addRegex()

    def initRegex(self):
        self.regDict = {}
        self.regTipDict = {}
        self.regDict['splitContent']    = r'<div tabindex="-1" class="zm-item-answer "'#关键表达式，用于切分答案
        self.regTipDict['splitContent'] = u'内容分割'
        
        #提取答主信息
        self.regDict['answerAuthorInfo']    = r'(?<=<h3 class="zm-item-answer-author-wrap">).*?(?=</h3>)'
        self.regTipDict['answerAuthorInfo'] = u'提取答主信息块'#若为匿名用户，则收集到的内容只有【匿名用户】四个字
        self.regDict['answerAuthorID']      = r'(?<=href="/people/)[^"]*'
        self.regTipDict['answerAuthorID']   = u'提取答主ID'
        self.regDict['answerAuthorLogo']    = r'(?<=<img src=")[^"]*'
        self.regTipDict['answerAuthorLogo'] = u'提取答主头像'
        self.regDict['answerAuthorSign']    = r'(?<= class="zu-question-my-bio">)[^<]*(?=</strong>)'
        self.regTipDict['answerAuthorSign'] = u'提取答主签名'#可能没有
        self.regTipDict['answerAuthorName'] = u'提取答主用户名'#需要在用户名基础上进行二次匹配,正则模板直接放在了函数里

        #提取答案信息
        self.regDict['answerAgreeCount']      = r'(?<=<div class="zm-item-vote-info " data-votecount=")[^"]*'#可能存在问题，当前测试样本中没有赞同数为0的情况，回去检查下
        self.regTipDict['answerAgreeCount']   = u'提取答案被赞同数'
        self.regDict['answerCommentCount']    = r'\d*(?= 条评论)'#为None
        self.regTipDict['answerCommentCount'] = u'提取答案被评论数'
        self.regDict['answerCollectCount']    = r''
        self.regTipDict['answerCollectCount'] = u'提取答案被收藏数'#只有在指定答案时才能用到
        
        self.regDict['answerContent']    = r'(?<=<div class=" zm-editable-content clearfix">).*?(?=</div></div><a class="zg-anchor-hidden ac")'
        self.regTipDict['answerContent'] = r'提取答案内容'
        
        self.regDict['answerInfo']      = r'(?<=class="zm-meta-panel").*?(?=<a href="#" name="report" class="meta-item zu-autohide">)'
        self.regTipDict['answerInfo']   = r'提取答案信息'
        self.regDict['noRecordFlag']    = r'<span class="copyright zu-autohide"><span class="zg-bull">'
        self.regTipDict['noRecordFlag'] = r'检查是否禁止转载'
        self.regDict['questionID']      = r'(?<= target="_blank" href="/question/)\d*' 
        self.regTipDict['questionID']   = u'提取问题ID'
        self.regDict['answerID']        = r'(?<= target="_blank" href="/question/\d{8}/answer/)\d*'
        self.regTipDict['answerID']     = u'提取答案ID'
        self.regDict['updateDate']      = r'(?<=>编辑于 )[-\d]*'#没有考虑到只显示时间和昨天今天的问题
        self.regTipDict['updateDate']   = u'提取最后更新日期'
        self.regDict['commitDate']      = r'(?<=发布于 )[-\d]*'#没有考虑到只显示时间和昨天今天的问题
        self.regTipDict['commitDate']   = u'提取回答日期'
        
        
        ##以下正则交由子类自定义之 
        #用戶首页信息提取
        self.regDict['id']      = r''
        self.regDict['name']    = r''
        self.regDict['sign']    = r''
        self.regTipDict['id']   = u'提取用户ID'
        self.regTipDict['name'] = u'提取用户名'
        self.regTipDict['sign'] = u'提取用户签名'
        
        self.regDict['followerCount']    = r''
        self.regDict['followCount']      = r''
        self.regTipDict['followerCount'] = u'提取被关注数'
        self.regTipDict['followCount']   = u'提取关注数'
        
        self.regDict['answerCount']        = r''
        self.regDict['questionCount']      = r''
        self.regDict['columnCount']        = r''
        self.regDict['editCount']          = r''
        self.regDict['collectionCount']    = r''
        self.regTipDict['answerCount']     = u'提取回答总数'
        self.regTipDict['questionCount']   = u'提取提问总数'
        self.regTipDict['columnCount']     = u'提取专栏文章数'
        self.regTipDict['editCount']       = u'提取公共编辑次数'
        self.regTipDict['collectionCount'] = u'提取所创建的收藏夹数'
        
        self.regDict['agreeCount']        = r''
        self.regDict['thanksCount']       = r''
        self.regDict['collectedCount']    = r''
        self.regTipDict['agreeCount']     = u'提取总赞同数'
        self.regTipDict['thanksCount']    = u'提取总感谢数'
        self.regTipDict['collectedCount'] = u'提取总收藏数'
        
        #其它信息
        self.regDict['collectionID']             = r''
        self.regDict['collectionDesc']           = r''
        self.regDict['collectionFollower']       = r''
        self.regDict['collectionTitle']          = r''
        self.regDict['collectionComment']        = r''
        self.regDict['collectionCreaterID']      = r''
        self.regDict['collectionCreaterName']    = r''
        self.regDict['collectionCreaterSign']    = r''
        self.regTipDict['collectionID']          = u'提取收藏夹ID'
        self.regTipDict['collectionDesc']        = u'提取收藏夹描述'
        self.regTipDict['collectionFollower']    = u'提取收藏夹被关注数'
        self.regTipDict['collectionTitle']       = u'提取收藏夹标题'
        self.regTipDict['collectionComment']     = u'提取收藏夹被评论数'
        self.regTipDict['collectionCreaterID']   = u'提取收藏夹创建者ID'
        self.regTipDict['collectionCreaterName'] = u'提取收藏夹创建者用户名'
        self.regTipDict['collectionCreaterSign'] = u'提取收藏夹创建者签名'

        self.regDict['topicID']          = r''
        self.regDict['topicTitle']       = r''
        self.regDict['topicDesc']        = r''
        self.regDict['topicFollower']    = r''
        self.regTipDict['topicID']       = u'提取话题ID'
        self.regTipDict['topicTitle']    = u'提取话题名'
        self.regTipDict['topicDesc']     = u'提取话题描述'
        self.regTipDict['topicFollower'] = u'提取话题关注者人数'

        self.regDict['roundTableID']          = r''
        self.regDict['roundTableTitle']       = r''
        self.regDict['roundTableDesc']        = r''
        self.regDict['roundTableFollower']    = r''
        self.regTipDict['roundTableID']       = u'提取圆桌ID'
        self.regTipDict['roundTableTitle']    = u'提取圆桌标题'
        self.regTipDict['roundTableDesc']     = u'提取圆桌描述'
        self.regTipDict['roundTableFollower'] = u'提取圆桌关注者人数'

        return 
    
    def addRegex(self):
        return

    def getSplitContent(self):
        return re.split(self.regDict['splitContent'], self.content)

    def matchContent(self, key, content):
        targetObject = re.search(self.regDict[key], content)
        if targetObject == None:
            #print self.regTipDict[key] + u'失败'
            return ''
        else:
            #print self.regTipDict[key] + u'成功'
            return targetObject.group(0)
    
    def getAnswerAuthorInfoDict(self, content):
        personInfo = {}
        authorInfo = self.matchContent('answerAuthorInfo', content)
        if authorInfo == u'匿名用户':
            personInfo['authorID']   = u"coder'sGirlFriend~" 
            personInfo['authorSign'] = u'' 
            personInfo['authorLogo'] = u'' 
            personInfo['authorName'] = u'匿名用户' 
        else:
            personInfo['authorID']           = self.matchContent('answerAuthorID', authorInfo)
            personInfo['authorSign']         = self.matchContent('answerAuthorSign', authorInfo)
            personInfo['authorLogo']         = self.matchContent('answerAuthorLogo', authorInfo)
            self.regDict['answerAuthorName'] = r'(?<=<a data-tip="p\$t\$' + personInfo['authorID'] + r'" href="/people/' + personInfo['authorID'] + r'">).*?(?=</a>)'
            personInfo['authorName']         = self.matchContent('answerAuthorName', authorInfo)
        
        return personInfo

    def getAnswerDict(self, content):
        answerDict = {}
        authorInfo = self.getAnswerAuthorInfoDict(content)
        for key in authorInfo:
            answerDict[key] = authorInfo[key]
        answerDict['answerAgreeCount'] = self.matchContent('answerAgreeCount', content)
        answerDict['answerContent']    = self.matchContent('answerContent', content)
        answerInfo = self.matchContent('answerInfo', content)
        for key in ['questionID', 'answerID', 'answerCommentCount', 'updateDate', 'commitDate', 'noRecordFlag']:
            answerDict[key] = self.matchContent(key, answerInfo)
        if answerDict['answerCommentCount'] == '':
            answerDict['answerCommentCount'] = 0
        if answerDict['noRecordFlag'] == '':
            answerDict['noRecordFlag'] = False
        else:
            answerDict['noRecordFlag'] = True
        answerDict['answerHref']     = 'http://www.zhihu.com/question/{0}/answer/{1}'.format(answerDict['questionID'], answerDict['answerID']) 
        answerDict['answerContent']  = HTMLParser.HTMLParser().unescape(answerDict['answerContent']).encode("utf-8")#对网页内容解码，可以进一步优化
        
        if answerDict['updateDate'] == '':
            answerDict['updateDate'] = answerDict['commitDate']
        for key in ['updateDate', 'commitDate']:#此处的时间格式转换还可以进一步改进
            if len(answerDict[key]) != 10:        
                pass
                #if  len(answerDict[key])==5:#这里有问题，一个汉字的长度用len算出来等于3，这么写会导致判断失误，要改掉
                #    answerDict[key] = time.strftime(u'%Y-%m-%d',time.localtime(time.time()))#今天
                #else:
                #    answerDict[key] = time.strftime(u'%Y-%m-%d',time.localtime(time.time()-86400))#昨天

        return answerDict

class ParseQuestion(Parse):
    u'''
    理想情况应当是：输入网页内容，返回两个dict，一个是问题信息dict，一个是答案dict列表
    如果答案太多一页显示不完该当何如？
    '''

    def addRegex(self):
        #实例化Regex
        #为Regex添加合适的项目
        self.regDict['questionIDinQuestionDesc']     = r'(?<=<a href="/question/)\d{8}(?=/followers"><strong>)' 
        self.regTipDict['questionIDinQuestionDesc']  = u'提取问题ID'
        self.regDict['questionFollowCount']     = r'(?<=<a href="/question/\d{8}/followers"><strong>).*(?=</strong></a>人关注该问题)' 
        self.regTipDict['questionFollowCount']  = u'提取问题关注人数'
        self.regDict['questionCommentCount']    = r'(?<=<i class="z-icon-comment"></i>).*?(?= 条评论</a>)'#该模式对答案中的评论也有效，需要小心处理
        self.regTipDict['questionCommentCount'] = u'提取问题评论数'
        
        self.regDict['questionTitle']    = r'(?<=<h2 class="zm-item-title zm-editable-content">).*?(?=</h2>)'
        self.regTipDict['questionTitle'] = u'提取问题标题'
        self.regDict['questionDesc']     = r'(?<=<textarea class="content hidden">).*?(?=</textarea>)'#取到的数据是html编码过的数据，需要逆处理一次才能存入数据库里
        self.regTipDict['questionDesc']  = u'提取问题描述'

        self.regDict['questionAnswerCount']    = r'(?<=id="zh-question-answer-num">)\d*'
        self.regTipDict['questionAnswerCount'] = u'问题下回答数'
        self.regDict['questionCollapsedAnswerCount']    = r'(?<=<span id="zh-question-collapsed-num">)\d*(?=</span>)'
        self.regDict['questionCollapsedAnswerCount']    = u'问题下回答折叠数'
        self.regDict['questionViewCount']        = r'(?<=<div class="zg-gray-normal">被浏览 <strong>)\d*(?=</strong>)'
        self.regTipDict['questionViewCount']     = u'问题浏览数'
    
    def getInfoDict(self):
        "列表长度有可能为0(没有回答),1(1个回答),2(2个回答)...,需要分情况处理"
        contentList = self.getSplitContent() 
        contentLength = len(contentList)
        questionInfoDict = {}#仅供测试临时使用，测试完成后需删除之
        if contentList == 0:
            questionInfoDict = self.getQusetionInfoDict(contentList[0], contentList[0])
            answerDictList   = [{}]
        else:
            questionInfoDict = self.getQusetionInfoDict(contentList[0], contentList[contentLength - 1])
            answerDictList   = []
            for i in range(1, contentLength):
                answerDictList.append(self.getAnswerDict(contentList[i]))
        return questionInfoDict, answerDictList
    
    def getQusetionInfoDict(self, titleContent, tailContent):
        questionInfoDict = {}
        for key in ['questionCommentCount', 'questionTitle', 'questionDesc', 'questionAnswerCount']:
            questionInfoDict[key] = self.matchContent(key, titleContent)   
        for key in ['questionIDinQuestionDesc', 'questionFollowCount', 'questionViewCount']:
            questionInfoDict[key] = self.matchContent(key, tailContent)   
        questionInfoDict['questionDesc']  = HTMLParser.HTMLParser().unescape(questionInfoDict['questionDesc']).encode("utf-8")#对网页内容解码，可以进一步优化
        return questionInfoDict
'''   
class ParseAnswer:
class ParseCollection:
class ParseColumn:
class ParseTopic:
class ParseTable:
'''
