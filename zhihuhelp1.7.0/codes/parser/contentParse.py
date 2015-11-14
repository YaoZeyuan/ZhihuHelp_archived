# -*- coding: utf-8 -*-
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
        questionInfoDict['questionCommentCount'] = self.match_int(bufString)
        questionInfoDict['questionDesc'] = self.get_tag_content(
            self.content.find("div", {"id": "zh-question-detail"}).find('div'))
        bufString = self.get_attr(self.content.find("h3", {"id": "zh-question-answer-num"}), 'data-num')
        questionInfoDict['questionAnswerCount'] = self.match_int(bufString)

        bufString = self.content.find("div", {"id": "zh-question-side-header-wrap"}).find("div", {
            "class": "zg-gray-normal"}).a.strong.text
        questionInfoDict['questionFollowCount'] = self.match_int(bufString)
        bufString = self.content.find("div", {"id": "zh-question-side-header-wrap"}).find("div", {
            "class": "zg-gray-normal"}).a.strong.text
        questionInfoDict['questionViewCount'] = self.match_int(bufString)
        bufString = \
            self.content.find("div", {"class": "zu-main-sidebar"}).find_all("div", {"class": "zm-side-section"})[
                -1].find_all("div", {"class": "zg-gray-normal"})[1].find("strong").text
        questionInfoDict['questionViewCount'] = bufString
        questionInfoDict['questionIDinQuestionDesc'] = self.get_attr(
            self.content.find("div", {'id': 'zh-single-question-page'}), 'data-urltoken')
        return questionInfoDict


class ParseAnswer(ParseQuestion):
    def getQuestionInfoDict(self):
        questionInfoDict = {}
        bufString = self.content.find("div", {"id": "zh-question-title"}).get_text()
        questionInfoDict['questionTitle'] = bufString
        bufString = self.content.find("a", {"name": "addcomment"}).get_text()
        questionInfoDict['questionCommentCount'] = self.match_int(bufString)
        questionInfoDict['questionDesc'] = self.get_tag_content(
            self.content.find("div", {"id": "zh-question-detail"}).find('div'))
        bufString = self.content.find("div", {"class": "zh-answers-title"}).find('a', {
            'class': 'zg-link-litblue'}).get_text()
        questionInfoDict['questionAnswerCount'] = self.match_int(bufString)

        bufString = self.content.find("div", {"id": "zh-question-side-header-wrap"}).find("div", {
            "class": "zg-gray-normal"}).a.strong.text
        questionInfoDict['questionFollowCount'] = self.match_int(bufString)
        bufString = self.content.find("div", {"id": "zh-question-side-header-wrap"}).find("div", {
            "class": "zg-gray-normal"}).a.strong.text
        questionInfoDict['questionViewCount'] = self.match_int(bufString)
        bufString = self.content.find("div", {"class": "zu-main-sidebar"}).find("div",
                                                                                {"class": "zm-side-section"}).find(
            "div", {"class": "zg-gray-normal"}).find("strong").text
        questionInfoDict['questionViewCount'] = bufString
        rawLink = self.get_attr(self.content.find("link", {'rel': 'canonical'}), 'href')
        questionInfoDict['questionIDinQuestionDesc'] = self.matchQuestionID(rawLink)
        return questionInfoDict

    def getAnswerContentList(self):
        return self.content.find_all("div", {"id": "zh-question-answer-wrap"})


class ParseAuthor(Parse):
    u'''
    输入网页内容，返回一个dict，答案dict列表
    '''

    def getAnswerContentList(self):
        u"""
        返回答案内容列表
        用户界面中一定会有#zh-profile-answer-list元素
        所以不必担心
        """
        return self.content.find(id="zh-profile-answer-list").find_all("div", {"class": "zm-item"})

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
        rawLink = self.get_attr(content.find("a", {'class': "question_link"}), 'href')
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
        rawLink = self.get_attr(content.find('h2', {'class': 'zm-item-title'}).a, 'href')
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

        infoDict['dataID'] = self.get_attr(self.content.find("button", {'class': 'zm-rich-follow-btn'}), 'data-id')
        infoDict['authorLogoAddress'] = self.get_attr(self.content.find('img', {'class': 'avatar-l'}), 'src')
        infoDict['weiboAddress'] = self.get_attr(self.content.find('a', {'class': 'zm-profile-header-user-weibo'}),
                                                 'href')
        infoDict['watched'] = self.match_int(
            self.content.find_all('div', {'class': 'zm-side-section-inner'})[-1].span.strong.get_text())
        infoDict['authorID'] = self.match_author_id(
            self.get_attr(self.content.find('div', {'class': 'title-section'}).a, 'href'))
        infoDict['name'] = self.content.find('div', {'class': 'title-section'}).find(attrs={'class': 'name'}).get_text()
        infoDict['sign'] = self.get_attr(
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
            infoDict[kind] = self.match_int(self.get_tag_content(infoList[i]))
            i += 1

        infoList = self.content.find('div', {'class': 'zm-profile-side-following'}).find_all('a', {'class': 'item'})
        infoDict['followee'] = self.match_int(infoList[0].get_text())
        infoDict['follower'] = self.match_int(infoList[1].get_text())

        infoList = self.content.find('div', {'class': 'zm-profile-details-reputation'}).find_all('i', {
            'class': 'zm-profile-icon'})
        kindList = ['agree', 'thanks', 'collected', 'shared']
        i = 0
        for kind in kindList:
            infoDict[kind] = self.match_int(self.get_tag_content(infoList[i]))
            i += 1
        return infoDict


class TopicInfoParse(Parse):
    u'标准网页:正常值'

    def getInfoDict(self):
        infoDict = {}
        infoDict['title'] = self.content.find('h1', {'class': 'zm-editable-content'}).get_text()
        infoDict['description'] = self.get_tag_content(
            self.content.find('div', {'id': 'zh-topic-desc'}).find('div', 'zm-editable-content'))
        infoDict['topicID'] = self.match_int(
            self.get_attr(self.content.find('a', {'id': 'zh-avartar-edit-form'}), 'href'))
        infoDict['logoAddress'] = self.get_attr(self.content.find('img', {'class': 'zm-avatar-editor-preview'}), 'src')
        infoDict['logoAddress'] = self.match_int(
            self.get_tag_content(self.content.find('div', {'class': 'zm-topic-side-followers-info'})))
        return infoDict


class CollectionInfoParse(Parse):
    u'标准网页:正常值'

    def getInfoDict(self):
        infoDict = {}
        infoDict['title'] = self.get_tag_content(self.content.find('h2', {'id': 'zh-fav-head-title'}))
        infoDict['description'] = self.get_tag_content(self.content.find('div', {'id': 'zh-fav-head-description'}))
        infoDict['collectionID'] = self.match_int(
            self.get_attr(self.content.find('div', {'id': 'zh-list-meta-wrap'}).find_all('a')[1], 'href'))
        infoDict['commentCount'] = self.match_int(self.get_tag_content(
            self.content.find('div', {'id': 'zh-list-meta-wrap'}).find('a', {'name': 'addcomment'})))
        infoDict['followerCount'] = self.match_int(
            self.content.find_all('div', {'class': 'zm-side-section'})[2].find_all('div', {'class': 'zg-gray-normal'})[
                1].a.get_text())

        infoDict['authorID'] = self.match_author_id(
            self.get_attr(self.content.find('a', {'class': 'zm-list-avatar-link'}), 'href'))
        infoDict['authorSign'] = self.content.find('div', {'id': 'zh-single-answer-author-info'}).find('div',
                                                                                                       'zg-gray-normal').get_text()
        infoDict['authorName'] = self.content.find('div', {'id': 'zh-single-answer-author-info'}).a.get_text()
        return infoDict
