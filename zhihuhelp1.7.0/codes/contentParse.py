# -*- coding: utf-8 -*-
import re
import HTMLParser  # 转换网页代码
import datetime  # 简单处理时间

from baseClass import *
from bs4 import BeautifulSoup


class Parse(BaseClass):
    def __init__(self, content):
        BaseClass.logger.debug(u"开始解析网页")
        self.content = BeautifulSoup(content, 'html.parser')
        self.rawContent = content

    def getAnswerAuthorInfoDict(self, content):
        personInfo = {}
        if content.find('h3', {'class': 'zm-item-answer-author-wrap'}).img is None:
            # 匿名用户
            personInfo['authorID'] = u"coder'sGirlFriend~"
            personInfo['authorSign'] = u''
            personInfo['authorLogo'] = u'http://pic1.zhimg.com/da8e974dc_s.jpg'
            personInfo['authorName'] = u'匿名用户'
        else:
            # 可能为空
            personInfo['authorID'] = self.getContentAttr(
                content.find('h3', {'class': 'zm-item-answer-author-wrap'}).find('a', {'class': 'zm-item-link-avatar'}),
                'href')
            personInfo['authorID'] = self.matchAuthorID(personInfo['authorID'])
            personInfo['authorSign'] = self.getContentAttr(
                content.find('h3', {'class': 'zm-item-answer-author-wrap'}).find('strong',
                                                                                 {'class': 'zu-question-my-bio'}),
                'title')
            personInfo['authorLogo'] = self.getContentAttr(
                content.find('h3', {'class': 'zm-item-answer-author-wrap'}).img, 'data-source')
            personInfo['authorName'] = content.find('h3', {'class': 'zm-item-answer-author-wrap'}).find_all('a')[1].text
            for key in personInfo:
                personInfo[key] = unicode(personInfo[key])
        return personInfo

    def getAnswerContentList(self):
        u"""
        取得答案列表
        需重载
        """
        return self.content.find_all('div')

    def getAnswerDict(self, content):
        u"""
        content作为已经切分好了的答案bs_tag对象传入
        不要乱传参
        """
        answerDict = {}
        authorInfo = self.getAnswerAuthorInfoDict(content)
        for key in authorInfo:
            answerDict[key] = authorInfo[key]
        # 需要移除<noscript>中的内容
        # 需要考虑对『违反当前法律法规，暂不予以显示』内容的处理
        bufferString = content.find("div", {"class": "zm-item-vote"})
        if bufferString is None:
            answerDict['answerAgreeCount'] = self.getContentAttr(content.find("div", {"class": "zm-item-vote-info"}),
                                                                 'data-votecount', 0)
        else:
            answerDict['answerAgreeCount'] = self.getContentAttr(
                bufferString.find("a", {"class": "zm-item-vote-count"}), 'data-votecount', 0)
        if content.find('div', {'id': 'answer-status'}) != None:
            answerDict['answerContent'] = u'<p>回答被建议修改：包含少儿不宜的内容</p>'
            answerDict["updateDate"] = '1970-01-01'
            answerDict["commitDate"] = '1970-01-01'
            answerDict["noRecordFlag"] = 0
            answerDict["answerCommentCount"] = 0
        else:
            bufferString = content.find("div", {"class": "zm-item-rich-text", "data-action": "/answer/content"})
            if bufferString.find("textarea", {"class", "content"}) is None:
                # 单个问题&答案
                answerDict['answerContent'] = self.getTagContent(
                    bufferString.find("div", {"class", "zm-editable-content"}))
            else:
                answerDict['answerContent'] = self.getTagContent(bufferString.find("textarea", {"class", "content"}))
            answerDict["updateDate"] = content.find("span", {"class": "answer-date-link-wrap"}).text
            answerDict["commitDate"] = self.getContentAttr(content.find("span", {"class": "answer-date-link-wrap"}).a,
                                                           "data-tip")
            answerDict["noRecordFlag"] = self.getContentAttr(
                content.find("div", {"class": "zm-meta-panel"}).find("a", {"class": "copyright"}), "data-author-avatar")
            answerDict["answerCommentCount"] = self.matchInt(content.find("a", {"name": "addcomment"}).text)

        answerLink = self.getContentAttr(content.find("a", {"class": "answer-date-link"}), "href")
        answerDict["questionID"] = self.matchQuestionID(answerLink)
        answerDict["answerID"] = self.matchAnswerID(answerLink)

        if answerDict['answerAgreeCount'] == '':
            answerDict['answerAgreeCount'] = 0
        if answerDict['noRecordFlag'] == '':
            answerDict['noRecordFlag'] = 0
        else:
            answerDict['noRecordFlag'] = 1
        answerDict['answerHref'] = 'http://www.zhihu.com/question/{0}/answer/{1}'.format(answerDict['questionID'],
                                                                                         answerDict['answerID'])
        answerDict['answerContent'] = HTMLParser.HTMLParser().unescape(answerDict['answerContent'])  # 对网页内容解码，可以进一步优化

        if answerDict['commitDate'] == '':
            answerDict['commitDate'] = answerDict['updateDate']
        for key in ['updateDate', 'commitDate']:  # 此处的时间格式转换还可以进一步改进
            if len(answerDict[key]) != 10:
                if len(answerDict[key]) == 0:
                    answerDict[key] = self.getYesterday().isoformat()
                else:
                    answerDict[key] = datetime.date.today().isoformat()
        return answerDict

    def getYesterday(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday

    def matchContent(self, partten, content, defaultValue=""):
        result = re.search(partten, str(content))
        if result == None:
            return defaultValue
        return result.group(0)

    def matchInt(self, content):
        u"""
        返回文本形式的文字中最长的数字串，若没有则返回'0'
        """
        return self.matchContent("\d+", content, "0")

    def matchQuestionID(self, rawLink):
        return self.matchContent("(?<=question/)\d{8}", rawLink)

    def matchAnswerID(self, rawLink):
        return self.matchContent("(?<=answer/)\d{8}", rawLink)

    def matchAuthorID(self, rawLink):
        return self.matchContent("""(?<=people/)[^/'"]+""", rawLink)

    def getTagContent(self, tag):
        u'''
        只用于提取bs中tag.contents的内容，不要乱传参
        思路来自stackoverflow，http://stackoverflow.com/questions/8112922/beautifulsoup-innerhtml
        帅爆了！
        '''
        content = unicode(tag)
        content = "".join([unicode(x) for x in tag.contents])
        return content

    def getContentAttr(self, content, attr, defaultValue=""):
        u"""
        获取bs中tag.content的指定属性
        若content为空或者没有指定属性则返回默认值
        """
        if content == None:
            return defaultValue
        return content.get(attr, defaultValue)


class ParseQuestion(Parse):
    u'''
    输入网页内容，返回两个dict，一个是问题信息dict，一个是答案dict列表
    '''

    def getAnswerContentList(self):
        return self.content.find_all("div", {"class": "zm-item-answer "})

    def getInfoDict(self):
        "列表长度有可能为0(没有回答),1(1个回答),2(2个回答)...,需要分情况处理"
        contentList = self.getAnswerContentList()
        questionInfoDictList = []
        answerDictList = []
        questionInfoDictList.append(self.getQuestionInfoDict())
        if len(contentList) != 0:
            for content in contentList:
                answerDictList.append(self.getAnswerDict(content))
        return questionInfoDictList, answerDictList

    def getQuestionInfoDict(self):
        questionInfoDict = {}
        bufString = self.content.find("div", {"id": "zh-question-title"}).get_text()
        questionInfoDict['questionTitle'] = bufString
        bufString = self.content.find("a", {"name": "addcomment"}).get_text()
        questionInfoDict['questionCommentCount'] = self.matchInt(bufString)
        questionInfoDict['questionDesc'] = self.getTagContent(
            self.content.find("div", {"id": "zh-question-detail"}).find('div'))
        bufString = self.content.find("h3", {"id": "zh-question-answer-num"})['data-num']
        questionInfoDict['questionAnswerCount'] = self.matchInt(bufString)

        bufString = self.content.find("div", {"id": "zh-question-side-header-wrap"}).find("div", {
            "class": "zg-gray-normal"}).a.strong.text
        questionInfoDict['questionFollowCount'] = self.matchInt(bufString)
        bufString = self.content.find("div", {"id": "zh-question-side-header-wrap"}).find("div", {
            "class": "zg-gray-normal"}).a.strong.text
        questionInfoDict['questionViewCount'] = self.matchInt(bufString)
        bufString = \
            self.content.find("div", {"class": "zu-main-sidebar"}).find_all("div", {"class": "zm-side-section"})[
                -1].find_all("div", {"class": "zg-gray-normal"})[1].find("strong").text
        questionInfoDict['questionViewCount'] = bufString
        questionInfoDict['questionIDinQuestionDesc'] = self.getContentAttr(
            self.content.find("div", {'id': 'zh-single-question-page'}), 'data-urltoken')
        return questionInfoDict


class ParseAnswer(ParseQuestion):
    def getQuestionInfoDict(self):
        questionInfoDict = {}
        bufString = self.content.find("div", {"id": "zh-question-title"}).get_text()
        questionInfoDict['questionTitle'] = bufString
        bufString = self.content.find("a", {"name": "addcomment"}).get_text()
        questionInfoDict['questionCommentCount'] = self.matchInt(bufString)
        questionInfoDict['questionDesc'] = self.getTagContent(
            self.content.find("div", {"id": "zh-question-detail"}).find('div'))
        bufString = self.content.find("div", {"class": "zh-answers-title"}).find('a', {
            'class': 'zg-link-litblue'}).get_text()
        questionInfoDict['questionAnswerCount'] = self.matchInt(bufString)

        bufString = self.content.find("div", {"id": "zh-question-side-header-wrap"}).find("div", {
            "class": "zg-gray-normal"}).a.strong.text
        questionInfoDict['questionFollowCount'] = self.matchInt(bufString)
        bufString = self.content.find("div", {"id": "zh-question-side-header-wrap"}).find("div", {
            "class": "zg-gray-normal"}).a.strong.text
        questionInfoDict['questionViewCount'] = self.matchInt(bufString)
        bufString = self.content.find("div", {"class": "zu-main-sidebar"}).find("div",
                                                                                {"class": "zm-side-section"}).find(
            "div", {"class": "zg-gray-normal"}).find("strong").text
        questionInfoDict['questionViewCount'] = bufString
        rawLink = self.getContentAttr(self.content.find("link", {'rel': 'canonical'}), 'href')
        questionInfoDict['questionIDinQuestionDesc'] = self.matchQuestionID(rawLink)
        return questionInfoDict

    def getAnswerContentList(self):
        return self.content.find_all("div", {"id": "zh-question-answer-wrap"})


class ParseAuthor(Parse):
    u'''
    输入网页内容，返回一个dict，答案dict列表
    '''

    def getAnswerContentList(self):
        return self.content.find("div", {"id": "zh-profile-answer-list"}).find_all("div", {"class": "zm-item"})

    def getInfoDict(self):
        contentList = self.getAnswerContentList()
        answerDictList = []
        questionInfoDictList = []
        for content in contentList:
            answerDict = self.getAnswerDict(content)
            if len(answerDict['answerID']) == 0:
                continue
            answerDictList.append(answerDict)
            lastQuestionInfoDict = {}
            if len(questionInfoDictList) > 0:
                lastQuestionInfoDict = questionInfoDictList[
                    -1]  # 在话题和收藏夹里，同一问题下的答案会被归并到一起，造成questionDict信息丢失，所以需要额外传入问题信息数据
            questionInfoDictList.append(self.getQuestionInfoDict(content, lastQuestionInfoDict))
        return questionInfoDictList, answerDictList

    def getQuestionInfoDict(self, content, lastQuestionInfoDict={}):
        questionInfoDict = {}
        questionTitle = content.find("a", {'class': "question_link"})
        if questionTitle is None:
            return lastQuestionInfoDict
        questionInfoDict['questionTitle'] = questionTitle.get_text()
        rawLink = self.getContentAttr(content.find("a", {'class': "question_link"}), 'href')
        questionInfoDict['questionIDinQuestionDesc'] = self.matchQuestionID(rawLink)
        return questionInfoDict


class ParseCollection(ParseAuthor):
    u"""
    直接继承即可
    """

    def getAnswerContentList(self):
        return self.content.find_all("div", {"class": "zm-item"})

    def getQuestionInfoDict(self, content, lastQuestionInfoDict={}):
        questionInfoDict = {}
        questionTitle = content.find('h2', {'class': 'zm-item-title'})
        if questionTitle is None:
            return lastQuestionInfoDict
        questionInfoDict['questionTitle'] = content.find('h2', {'class': 'zm-item-title'}).get_text()
        rawLink = self.getContentAttr(content.find('h2', {'class': 'zm-item-title'}).a, 'href')
        questionInfoDict['questionIDinQuestionDesc'] = self.matchQuestionID(rawLink)
        return questionInfoDict


class ParseTopic(ParseAuthor):
    def getAnswerContentList(self):
        return self.content.find("div", {"id": "zh-topic-top-page-list"}).find_all("div", {"itemprop": "question"})


'''
class ParseColumn:
class ParseTable:
'''


# ParseFrontPageInfo
class AuthorInfoParse(Parse):
    u'标准网页：/about'

    def getInfoDict(self):
        infoDict = {}

        infoDict['dataID'] = self.getContentAttr(self.content.find("button", {'class': 'zm-rich-follow-btn'}),
                                                 'data-id')
        infoDict['authorLogoAddress'] = self.getContentAttr(self.content.find('img', {'class': 'avatar-l'}), 'src')
        infoDict['weiboAddress'] = self.getContentAttr(
            self.content.find('a', {'class': 'zm-profile-header-user-weibo'}), 'href')
        infoDict['watched'] = self.matchInt(
            self.content.find_all('div', {'class': 'zm-side-section-inner'})[-1].span.strong.get_text())
        infoDict['authorID'] = self.matchAuthorID(
            self.getContentAttr(self.content.find('div', {'class': 'title-section'}).a, 'href'))
        infoDict['name'] = self.content.find('div', {'class': 'title-section'}).find(attrs={'class': 'name'}).get_text()
        infoDict['sign'] = self.getContentAttr(
            self.content.find('div', {'class': 'title-section'}).find(attrs={'class': 'bio'}), 'title')

        try:
            infoDict['desc'] = self.content.find('div', {'class': 'zm-profile-header-description'}).find('span', {
                'class': 'fold-item'}).get_text()
        except AttributeError:
            infoDict['desc'] = ''

        infoList = self.content.find('div', {'class': 'profile-navbar'}).find_all('span', {'class': 'num'})
        kindList = ['ask', 'answer', 'post', 'collect', 'edit']
        i = 0
        for kind in kindList:
            infoDict[kind] = self.matchInt(self.getTagContent(infoList[i]))
            i += 1

        infoList = self.content.find('div', {'class': 'zm-profile-side-following'}).find_all('a', {'class': 'item'})
        infoDict['followee'] = self.matchInt(infoList[0].get_text())
        infoDict['follower'] = self.matchInt(infoList[1].get_text())

        infoList = self.content.find('div', {'class': 'zm-profile-details-reputation'}).find_all('i', {
            'class': 'zm-profile-icon'})
        kindList = ['agree', 'thanks', 'collected', 'shared']
        i = 0
        for kind in kindList:
            infoDict[kind] = self.matchInt(self.getTagContent(infoList[i]))
            i += 1
        return infoDict


class TopicInfoParse(Parse):
    u'标准网页:正常值'

    def getInfoDict(self):
        infoDict = {}
        infoDict['title'] = self.content.find('h1', {'class': 'zm-editable-content'}).get_text()
        infoDict['description'] = self.getTagContent(
            self.content.find('div', {'id': 'zh-topic-desc'}).find('div', 'zm-editable-content'))
        infoDict['topicID'] = self.matchInt(
            self.getContentAttr(self.content.find('a', {'id': 'zh-avartar-edit-form'}), 'href'))
        infoDict['logoAddress'] = self.getContentAttr(self.content.find('img', {'class': 'zm-avatar-editor-preview'}),
                                                      'src')
        infoDict['logoAddress'] = self.matchInt(
            self.getTagContent(self.content.find('div', {'class': 'zm-topic-side-followers-info'})))
        return infoDict


class CollectionInfoParse(Parse):
    u'标准网页:正常值'

    def getInfoDict(self):
        infoDict = {}
        infoDict['title'] = self.getTagContent(self.content.find('h2', {'id': 'zh-fav-head-title'}))
        infoDict['description'] = self.getTagContent(self.content.find('div', {'id': 'zh-fav-head-description'}))
        infoDict['collectionID'] = self.matchInt(
            self.getContentAttr(self.content.find('div', {'id': 'zh-list-meta-wrap'}).find_all('a')[1], 'href'))
        infoDict['commentCount'] = self.matchInt(
            self.getTagContent(self.content.find('div', {'id': 'zh-list-meta-wrap'}).find('a', {'name': 'addcomment'})))
        infoDict['followerCount'] = self.matchInt(
            self.content.find_all('div', {'class': 'zm-side-section'})[2].find_all('div', {'class': 'zg-gray-normal'})[
                1].a.get_text())

        infoDict['authorID'] = self.matchAuthorID(
            self.getContentAttr(self.content.find('a', {'class': 'zm-list-avatar-link'}), 'href'))
        infoDict['authorSign'] = self.content.find('div', {'id': 'zh-single-answer-author-info'}).find('div',
                                                                                                       'zg-gray-normal').get_text()
        infoDict['authorName'] = self.content.find('div', {'id': 'zh-single-answer-author-info'}).a.get_text()
        return infoDict
