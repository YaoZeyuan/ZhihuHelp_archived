# -*- coding: utf-8 -*-
from baseClass import *

import re
import HTMLParser #转换网页代码
import datetime#简单处理时间

class Parse(BaseClass):
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
        self.regDict['answerAuthorSign']    = r'(?<=<strong title=").*(?=" class="zu-question-my-bio">)'
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
        self.regDict['updateDate']      = r'(?<=>编辑于 )[-:\d]*'#没有考虑到只显示时间和昨天今天的问题
        self.regTipDict['updateDate']   = u'提取最后更新日期'
        self.regDict['commitDate']      = r'(?<=发布于 )[-:\d]*'#没有考虑到只显示时间和昨天今天的问题
        self.regTipDict['commitDate']   = u'提取回答发布日期'
        
        
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
            #print u'匹配失败的内容为'
            #print content
            #exit()
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
        if answerDict['answerAgreeCount'] == '':
            answerDict['answerAgreeCount'] = 0
        if answerDict['answerCommentCount'] == '':
            answerDict['answerCommentCount'] = 0
        if answerDict['noRecordFlag'] == '':
            answerDict['noRecordFlag'] = 0
        else:
            answerDict['noRecordFlag'] = 1
        answerDict['answerHref']     = 'http://www.zhihu.com/question/{0}/answer/{1}'.format(answerDict['questionID'], answerDict['answerID']) 
        answerDict['answerContent']  = HTMLParser.HTMLParser().unescape(answerDict['answerContent'])#对网页内容解码，可以进一步优化
        
        if answerDict['updateDate'] == '':
            answerDict['updateDate'] = answerDict['commitDate']
        for key in ['updateDate', 'commitDate']:#此处的时间格式转换还可以进一步改进
            if len(answerDict[key]) != 10:        
                if len(answerDict[key]) == 0:
                    answerDict[key] = self.getYesterday().isoformat()
                else:
                    answerDict[key] = datetime.date.today().isoformat()
        return answerDict
    
    def getYesterday(self):
        today=datetime.date.today() 
        oneday=datetime.timedelta(days=1) 
        yesterday=today-oneday  
        return yesterday

class ParseQuestion(Parse):
    u'''
    输入网页内容，返回两个dict，一个是问题信息dict，一个是答案dict列表
    '''

    def addRegex(self):
        #实例化Regex
        #为Regex添加合适的项目
        self.regDict['questionIDinQuestionDesc']     = r'(?<=<a href="/question/)\d{8}(?=/followers"><strong>)' 
        self.regTipDict['questionIDinQuestionDesc']  = u'提取问题ID'
        self.regDict['questionFollowCount']          = r'(?<=<a href="/question/\d{8}/followers"><strong>).*(?=</strong></a>人关注该问题)' 
        self.regTipDict['questionFollowCount']       = u'提取问题关注人数'
        self.regDict['questionCommentCount']         = r'(?<=<i class="z-icon-comment"></i>).*?(?= 条评论</a>)'#该模式对答案中的评论也有效，需要小心处理
        self.regTipDict['questionCommentCount']      = u'提取问题评论数'
        
        self.regDict['questionTitle']    = r'(?<=<title>)[^-]*?(?=-)'
        self.regTipDict['questionTitle'] = u'提取问题标题'
        self.regDict['questionDesc']     = r'(?<=<div class="zm-editable-content">).*?(?=</div>)'#取到的数据是html编码过的数据，需要逆处理一次才能存入数据库里
        self.regTipDict['questionDesc']  = u'提取问题描述'

        self.regDict['questionAnswerCount']          = r'(?<=id="zh-question-answer-num">)\d*'
        self.regTipDict['questionAnswerCount']       = u'问题下回答数'
        self.regDict['questionCollapsedAnswerCount'] = r'(?<=<span id="zh-question-collapsed-num">)\d*(?=</span>)'
        self.regDict['questionCollapsedAnswerCount'] = u'问题下回答折叠数'
        self.regDict['questionViewCount']            = r'(?<=<div class="zg-gray-normal">被浏览 <strong>)\d*(?=</strong>)'
        self.regTipDict['questionViewCount']         = u'问题浏览数'
    
    def getInfoDict(self):
        "列表长度有可能为0(没有回答),1(1个回答),2(2个回答)...,需要分情况处理"
        contentList = self.getSplitContent() 
        contentLength = len(contentList)
        questionInfoDictList = []
        answerDictList       = []
        if contentList == 0:
            questionInfoDictList.append(self.getQusetionInfoDict(contentList[0], contentList[0]))
        else:
            questionInfoDictList.append(self.getQusetionInfoDict(contentList[0], contentList[contentLength - 1]))
            for i in range(1, contentLength):
                answerDictList.append(self.getAnswerDict(contentList[i]))
        return questionInfoDictList, answerDictList
    
    def getQusetionInfoDict(self, titleContent, tailContent):
        questionInfoDict = {}
        for key in ['questionCommentCount', 'questionTitle', 'questionDesc', 'questionAnswerCount']:
            questionInfoDict[key] = self.matchContent(key, titleContent)   
        for key in ['questionIDinQuestionDesc', 'questionFollowCount', 'questionViewCount']:
            questionInfoDict[key] = self.matchContent(key, tailContent)   
        questionInfoDict['questionDesc'] = HTMLParser.HTMLParser().unescape(questionInfoDict['questionDesc'])#对网页内容解码，可以进一步优化
        return questionInfoDict

class ParseAnswer(ParseQuestion):
    def addRegex(self):
        #实例化Regex
        #为Regex添加合适的项目
        self.regDict['questionIDinQuestionDesc']    = r'(?<=<a href="/question/)\d{8}(?=/followers"><strong>)' 
        self.regTipDict['questionIDinQuestionDesc'] = u'提取问题ID'
        self.regDict['questionFollowCount']         = r'(?<=<a href="/question/\d{8}/followers"><strong>).*(?=</strong></a>人关注该问题)' 
        self.regTipDict['questionFollowCount']      = u'提取问题关注人数'
        self.regDict['questionCommentCount']        = r'(?<=<i class="z-icon-comment"></i>).*?(?= 条评论</a>)'#该模式对答案中的评论也有效，需要小心处理
        self.regTipDict['questionCommentCount']     = u'提取问题评论数'
        
        self.regDict['questionTitle']    = r'(?<=<title>)[^-]*?(?=-)'
        self.regTipDict['questionTitle'] = u'提取问题标题'
        self.regDict['questionDesc']     = r'(?<=<div class="zm-editable-content">).*?(?=</div>)'#取到的数据是html编码过的数据，需要逆处理一次才能存入数据库里
        self.regTipDict['questionDesc']  = u'提取问题描述'

        self.regDict['questionAnswerCount']          = r'(?<=查看全部 )\d*(?= 个回答)'
        self.regTipDict['questionAnswerCount']       = u'问题下回答数'
        self.regDict['questionCollapsedAnswerCount'] = r'(?<=<span id="zh-question-collapsed-num">)\d*(?=</span>)'
        self.regDict['questionCollapsedAnswerCount'] = u'问题下回答折叠数'
        self.regDict['questionViewCount']            = r'(?<=<p>所属问题被浏览 <strong>)\d*(?=</strong>)'
        self.regTipDict['questionViewCount']         = u'问题浏览数'
    
    def getQusetionInfoDict(self, titleContent, tailContent):
        questionInfoDict = {}
        for key in ['questionCommentCount', 'questionTitle', 'questionDesc', 'questionAnswerCount']:
            questionInfoDict[key] = self.matchContent(key, titleContent)   
        for key in ['questionIDinQuestionDesc', 'questionFollowCount', 'questionViewCount']:
            questionInfoDict[key] = self.matchContent(key, tailContent)   
        questionInfoDict['questionAnswerCount'] = int(questionInfoDict['questionAnswerCount']) + 1 #知乎显示的全部回答数是被js处理过的。。。需要手工加一。。。汗
        questionInfoDict['questionDesc']  = HTMLParser.HTMLParser().unescape(questionInfoDict['questionDesc'])#对网页内容解码，可以进一步优化
        return questionInfoDict


class ParseAuthor(Parse):
    u'''
    输入网页内容，返回一个dict，答案dict列表
    '''

    def addRegex(self):
        #实例化Regex
        #为Regex添加合适的项目
        self.regDict['splitContent']    = r'div class="zm-item" id="mi'#关键表达式，用于切分答案
        self.regDict['answerContent']   = r'(?<=<textarea class="content hidden">).*(?=<span class="answer-date-link-wrap">)'
        self.regDict['answerInfo']      = r'(?<=<div class="zm-meta-panel">).*?(?=<a href="#" name="collapse" class="collapse meta-item zg-right"><i class="z-icon-fold">)'
        self.regDict['updateInfo']      = r'(?<=<span class="answer-date-link-wrap">).*?(?=</span>)'
        self.regTipDict['updateInfo']   = u'提取答案更新日期信息'

        self.regDict['questionInfo']             = r'(?<=<h2><a class="question_link").*?(?=</a></h2>)'
        self.regTipDict['questionInfo']          = u'提取问题相关信息'
        self.regDict['questionIDinQuestionDesc'] = r'(?<=href="/question/)\d{8}'
        self.regDict['questionTitle']            = r'(?<=>).*'

    def getInfoDict(self):
        contentList = self.getSplitContent() 
        answerDictList       = []
        questionInfoDictList = []
        for content in contentList:
            answerDict = self.getAnswerDict(content)
            #切割时会把最开始的个人介绍内容也切出来，在那里提取不到答案内容，会导致程序故障，需要跳过
            if len(answerDict['answerID']) == 0:
                continue
            answerDictList.append(answerDict)
            questionInfoDictList.append(self.getQusetionInfoDict(content))
        return questionInfoDictList, answerDictList

    def getAnswerDict(self, content):
        answerDict = {}
        authorInfo = self.getAnswerAuthorInfoDict(content)
        for key in authorInfo:
            answerDict[key] = authorInfo[key]
        answerDict['answerAgreeCount'] = self.matchContent('answerAgreeCount', content)
        answerDict['answerContent']    = self.matchContent('answerContent', content)
        answerInfo = self.matchContent('answerInfo', content)
        updateInfo = self.matchContent('updateInfo', content)
        for key in ['questionID', 'answerID', 'updateDate', 'commitDate']:
            answerDict[key] = self.matchContent(key, updateInfo)
        for key in ['answerCommentCount','noRecordFlag']:
            answerDict[key] = self.matchContent(key, answerInfo)

        if answerDict['answerAgreeCount']   == '':
            answerDict['answerAgreeCount']   = 0
        if answerDict['answerCommentCount'] == '':
            answerDict['answerCommentCount'] = 0
        if answerDict['noRecordFlag']       == '':
            answerDict['noRecordFlag']       = 0
        else:
            answerDict['noRecordFlag'] = 1
        answerDict['answerHref']     = 'http://www.zhihu.com/question/{0}/answer/{1}'.format(answerDict['questionID'], answerDict['answerID']) 
        answerDict['answerContent']  = HTMLParser.HTMLParser().unescape(answerDict['answerContent'])#对网页内容解码，可以进一步优化
        
        if answerDict['updateDate'] == '':
            answerDict['updateDate'] = answerDict['commitDate']
        for key in ['updateDate', 'commitDate']:#此处的时间格式转换还可以进一步改进
            if len(answerDict[key]) != 10:        
                if len(answerDict[key]) == 0:
                    answerDict[key] = self.getYesterday().isoformat()
                else:
                    answerDict[key] = datetime.date.today().isoformat()
        return answerDict

    def getQusetionInfoDict(self, content):
        questionInfoDict = {}
        questionInfo = self.matchContent('questionInfo', content)
        for key in ['questionTitle', 'questionIDinQuestionDesc']:
            questionInfoDict[key] = self.matchContent(key, questionInfo)   
        return questionInfoDict

class ParseCollection(ParseAuthor):
    u"""
    直接继承即可
    """
    def addRegex(self):
        #实例化Regex
        #为Regex添加合适的项目
        self.regDict['splitContent']    = r'div class="zm-item"'#关键表达式，用于切分答案
        self.regDict['answerContent']   = r'(?<=<textarea class="content hidden">).*(?=<span class="answer-date-link-wrap">)'
        self.regDict['answerInfo']      = r'(?<=<div class="zm-meta-panel">).*?(?=<a href="#" name="collapse" class="collapse meta-item zg-right"><i class="z-icon-fold">)'
        self.regDict['updateInfo']      = r'(?<=<span class="answer-date-link-wrap">).*?(?=</span>)'
        self.regTipDict['updateInfo']   = u'提取答案更新日期信息'

        self.regDict['questionInfo']             = r'(?<=<h2 class="zm-item-title"><a target="_blank" ).*?(?=</a></h2>)'
        self.regTipDict['questionInfo']          = u'提取问题相关信息'
        self.regDict['questionIDinQuestionDesc'] = r'(?<=href="/question/)\d{8}'
        self.regDict['questionTitle']            = r'(?<=>).*'

class ParseTopic(ParseAuthor):
    def addRegex(self):
        #实例化Regex
        #为Regex添加合适的项目
        self.regDict['splitContent']     = r'<div class="feed-main">'#关键表达式，用于切分答案
        self.regDict['answerContent']    = r'(?<=<textarea class="content hidden">).*(?=<span class="answer-date-link-wrap">)'
        self.regDict['answerInfo']       = r'(?<=<div class="zm-meta-panel">).*?(?=<a href="#" name="collapse" class="collapse meta-item zg-right"><i class="z-icon-fold">)'
        self.regDict['updateInfo']       = r'(?<=<span class="answer-date-link-wrap">).*?(?=</span>)'
        self.regTipDict['updateInfo']    = u'提取答案更新日期信息'
        self.regDict['answerAuthorSign'] = r'(?<=<strong title=")[^<]*(?=" class="zu-question-my-bio">)'

        self.regDict['questionInfo']             = r'(?<=<h2><a class="question_link").*?(?=</a></h2>)'
        self.regTipDict['questionInfo']          = u'提取问题相关信息'
        self.regDict['questionIDinQuestionDesc'] = r'(?<=href="/question/)\d{8}'
        self.regDict['questionTitle']            = r'(?<=>).*'
'''   
class ParseColumn:
class ParseTable:
'''



#ParseFrontPageInfo
class AuthorInfoParse(Parse):
    u'规范:所有获取信息块的内容，均以Content结尾，只有直接获取对应数据的表达式才能以对应名词命名'
    u'标准网页：/about'
    def addRegex(self):
        self.regDict = {}
        self.regDict['weiboContent']    = r'(?<=<div class=\'weibo-wrap\'>).*?(?=</div>)'
        self.regTipDict['weiboContent'] = u'微博内容'
        self.regDict['weiboAddress']    = r'(?<=href=").*?(?=")'
        self.regTipDict['weiboAddress'] = u'微博地址'

        self.regDict['nameInfoContent'] = r'(?<=<div class="title-section ellipsis">).*?(?=</div>)'
        self.regTipDict['nameInfoContent'] = u'用户名&ID&签名内容'
        self.regDict['authorID'] = r'(?<=href="/people/).*?(?=")'
        self.regTipDict['authorID'] = u'用户ID'
        self.regDict['sign'] = r'(?<=<span class="bio" title=").*?(?=")'#不必担心引号问题，引号会在html中被自动转义
        self.regTipDict['sign'] = u'用户签名'
        self.regDict['name'] = r'(?<=">).*?(?=</a>)'
        self.regTipDict['name'] = u'用户名'
        

        self.regDict['userDesc'] = r'(?<=<span class="description unfold-item"><span class="content">).*?(?=</span><a href="javascript:;" class="unfold")'
        self.regTipDict['userDesc']  = u'用户描述'
        
        self.regDict['userActiveInfoContent'] = r'(?<=<div class="profile-navbar clearfix">).*?(?=<div class="zm-profile-section-wrap zm-profile-details-wrap">)'
        self.regTipDict['userActiveInfoContent']  = u'用户提问/回答/专栏/收藏夹数/公共编辑数'

        self.regDict['userHonourInfoContent'] = r'(?<=<div class="zm-profile-module-desc">).*?(?=<div class="zm-profile-module zg-clear">)'
        self.regTipDict['userHonourInfoContent']  = u'用户赞同数/感谢数/收藏数/分享数'

        self.regDict['userFollowInfoContent'] = r'(?<=<div class="zm-profile-side-following zg-clear">).*?(?=</div>)'
        self.regTipDict['userFollowInfoContent']  = u'用户关注数&被关注数'

        self.regDict['columnCountInfoContent'] = r'(?<=<div class="zm-profile-side-section-title">).*?(?=</div>)'
        self.regTipDict['columnCountInfoContent']  = u'关注的专栏数信息'

        self.regDict['topicCountInfoContent'] = r'(?<=<div class="zm-profile-side-section-title">).*?(?=</div>)'
        self.regTipDict['topicCountInfoContent']  = u'关注的话题数信息'
        
        self.regDict['userViewContent'] = r'(?<=<div class="zm-profile-side-section"><div class="zm-side-section-inner"><span class="zg-gray-normal">).*?(?=</div>)'
        self.regTipDict['userViewContent']  = u'用户浏览数信息'
        self.regDict['watched']    = r'(?<=<strong>)\d*(?=</strong>)'
        self.regTipDict['watched'] = u'用户浏览数'
        
        self.regDict['authorLogoContent']    = r'(?<=<div class="zm-profile-header-avatar-container ">).*?(?="class="zm-profile-header-img zg-avatar-big zm-avatar-editor-preview"/>)'
        self.regTipDict['authorLogoContent'] = u'用户头像内容'
        self.regDict['authorLogoAddress']    = r'(?<=src=").*'
        self.regTipDict['authorLogoAddress'] = u'用户头像'
        
        self.regDict['dataID']    = r'(?<=data-id=").*?(?=")'
        self.regTipDict['dataID'] = u'dataID'
    
    def getInfoDict(self):
        infoDict = {}

        infoDict['dataID'] = self.matchContent('dataID', self.content)

        authorLogoContent = self.matchContent('authorLogoContent', self.content)
        infoDict['authorLogoAddress'] = self.matchContent('authorLogoAddress', authorLogoContent)

        weiboContent = self.matchContent('weiboContent', self.content)
        infoDict['weiboAddress'] = self.matchContent('weiboAddress', weiboContent)

        userViewContent     = self.matchContent('userViewContent', self.content)
        infoDict['watched'] = self.matchContent('watched', userViewContent)

        nameInfoContent = self.matchContent('nameInfoContent', self.content)
        for key in ['authorID', 'name', 'sign']:
            infoDict[key] = self.matchContent(key, nameInfoContent)
        infoDict['desc'] = self.matchContent('userDesc', self.content)

        try:
            userActiveInfoContent = self.matchContent('userActiveInfoContent', self.content)
            infoDict['ask'], infoDict['answer'], infoDict['post'], infoDict['collect'], infoDict['edit'] = re.findall(r'(?<=<span class="num">)\d*(?=</span></a>)', userActiveInfoContent)
        except ValueError as error:
            print u'匹配用户提问数/回答数/专栏数/收藏夹数/公共编辑数失败'
            print u'错误内容:'
            print error

        try:
            userFollowInfoContent = self.matchContent('userFollowInfoContent', self.content)
            infoDict['followee'], infoDict['follower'] = re.findall(r'(?<=<strong>)\d*(?=</strong><label>)', userFollowInfoContent)
        except ValueError as error:
            print u'匹配用户关注数/被关注数失败'
            print u'错误内容:'
            print error
        
        try:
            userHonourInfoContent = self.matchContent('userHonourInfoContent', self.content)
            infoDict['agree'], infoDict['thanks'], infoDict['collected'], infoDict['shared'] = re.findall(r'(?<=<span><strong>)\d*(?=</strong>)', userHonourInfoContent)
        except ValueError as error:
            print u'匹配用户赞同数/感谢数/被收藏数/被分享数失败'
            print u'错误内容:'
            print error

        return infoDict

class TopicInfoParse(Parse):
    u'标准网页:正常值'
    def addRegex(self):
        self.regDict = {}
        self.regDict['topicTitle']    = r'(?<=<title>).*?(?= - )'
        self.regTipDict['topicTitle'] = u'话题标题'
        self.regDict['topicID']    = r'(?<=zhihu://topics/)\d{8}(?="><meta name="description")'
        self.regTipDict['topicID'] = u'话题ID'

        self.regDict['watchCountInfoContent']    = r'(?<=<div class="zm-topic-side-followers-info">).*?(?=</div>)'
        self.regTipDict['watchCountInfoContent'] = u'关注人数信息'
        self.regDict['watchCount']    = r'(?<=<strong>)\d*(?=</strong>)'
        self.regTipDict['watchCount'] = u'关注人数'

        self.regDict['topicDesc']    = r'(?<=<div class="zm-editable-content" data-editable-maxlength="130" >).*?(?=</div>)'
        self.regTipDict['topicDesc'] = u'问题描述'

        self.regDict['topicLogoContent']    = r'(?<=<a class="zm-entry-head-avatar-link" ).*?(?=</div>)'
        self.regTipDict['topicLogoContent'] = u'话题题图信息'
        self.regDict['topicLogo']    = r'(?<=src=").*?(?=")'
        self.regTipDict['topicLogo'] = u'话题题图'
        return

    def getInfoDict(self):
        infoDict = {}
        infoDict['title'] = self.matchContent('topicTitle', self.content) 
        infoDict['description'] = self.matchContent('topicDesc', self.content) 
        infoDict['topicID'] = self.matchContent('topicID', self.content) 

        topicLogoContent = self.matchContent('topicLogoContent', self.content) 
        infoDict['logoAddress'] = self.matchContent('topicLogo', topicLogoContent) 

        watchCountInfoContent = self.matchContent('watchCountInfoContent', self.content)
        infoDict['followerCount'] = self.matchContent('watchCount', watchCountInfoContent)
        return infoDict

class CollectionInfoParse(Parse):
    u'标准网页:正常值'
    def addRegex(self):
        self.regDict['collectionTitle'] = r'(?<=<h2 class="zm-item-title zm-editable-content" id="zh-fav-head-title">).*?(?=</h2>)'
        self.regTipDict['collectionTitle']  = u'收藏夹标题'
        self.regDict['collectionDesc'] = r'(?<=<div class="zm-editable-content" id="zh-fav-head-description">).*?(?=</div>)'
        self.regTipDict['collectionDesc']  = u'收藏夹描述'
        self.regDict['collectionID']    = r'(?<=<a href="/collection/)\d{8}(?=/log)'
        self.regTipDict['collectionID'] = u'收藏夹ID'
        
        self.regDict['collectionCommentCountContent'] = r'(?<=<div class="zm-item-meta zm-item-comment-el" id="zh-list-meta-wrap">).*?(?=</div>)'
        self.regTipDict['collectionCommentCountContent']  = u'收藏夹评论数内容'
        self.regDict['collectionCommentCount']    = r'(?<=<i class="z-icon-comment"></i>)\d*'
        self.regTipDict['collectionCommentCount'] = u'收藏夹评论数'

        self.regDict['collectionWatchCountContent'] = r'(?<=<div id="zh-favlist-webshare-container" class="zh-question-webshare-links clearfix">).*?(?=<div id="zh-favlist-followers" class="zu-small-avatar-list">)'
        self.regTipDict['collectionWatchCountContent']  = u'收藏夹关注数内容'
        self.regDict['collectionWatchCount'] = r'(?<=<div class="zg-gray-normal"><a href="/collection/\d{8}/followers">)\d*(?=</a>)'
        self.regTipDict['collectionWatchCount']  = u'收藏夹关注数内容'

        self.regDict['creatorInfoContent']     = r'(?<=<div class="zm-list-content-medium" id="zh-single-answer-author-info">).*?(?=</div>)'
        self.regTipDict['creatorInfoContent']  = u'创建者信息内容'
        self.regDict['authorID']    = r'(?<=<a href="/people/).*?(?=")'
        self.regTipDict['authorID'] = u'用户ID'
        self.regDict['authorSign']    = r'(?<=<div class="zg-gray-normal">).*'
        self.regTipDict['authorSign'] = u'用户签名'
        self.regDict['authorName']    = r''#需要用户ID的支持
        self.regTipDict['authorName'] = u'用户名'

    def getInfoDict(self):
        infoDict = {}
        infoDict['title']        = self.matchContent('collectionTitle', self.content)
        infoDict['description']  = self.matchContent('collectionDesc', self.content)
        infoDict['collectionID'] = self.matchContent('collectionID', self.content)

        commentCountContent = self.matchContent('collectionCommentCountContent', self.content)
        infoDict['commentCount'] = self.matchContent('collectionCommentCount', commentCountContent)
        if len(infoDict['commentCount']) == 0:
            infoDict['commentCount'] = 0
        else:
            infoDict['commentCount'] = int(infoDict['commentCount'])
        
        watchContent = self.matchContent('collectionWatchCountContent', self.content)
        infoDict['followerCount'] = self.matchContent('collectionWatchCount', watchContent)
        
        creatorInfoContent = self.matchContent('creatorInfoContent', self.content)
        for key in ['authorID', 'authorSign']:
            infoDict[key] = self.matchContent(key, creatorInfoContent)
        
        self.regDict['authorName'] = r'(?<={}">).*?(?=</a></h2>)'.format(infoDict['authorID'])
        infoDict['authorName']     = self.matchContent('authorName', creatorInfoContent)

        return infoDict
