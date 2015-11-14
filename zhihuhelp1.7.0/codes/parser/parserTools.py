# -*- coding: utf-8 -*-

import re
import datetime  # 简单处理时间

from codes.baseClass import *
from bs4 import BeautifulSoup


class ParserTools(BaseClass):
    @staticmethod
    def get_yesterday():
        today = datetime.date.today()
        one = datetime.timedelta(days=1)
        yesterday = today - one
        return yesterday.isoformat()

    @staticmethod
    def get_today():
        return datetime.date.today().isoformat()

    @staticmethod
    def match_content(patten, content, default=""):
        result = re.search(patten, str(content))
        if result is None:
            return default
        return result.group(0)

    @staticmethod
    def match_int(content):
        u"""
        返回文本形式的文字中最长的数字串，若没有则返回'0'
        """
        return ParserTools.match_content("\d+", content, "0")

    @staticmethod
    def match_question_id(rawLink):
        return ParserTools.match_content("(?<=question/)\d{8}", rawLink)

    @staticmethod
    def match_answer_id(rawLink):
        return ParserTools.match_content("(?<=answer/)\d{8}", rawLink)

    @staticmethod
    def match_author_id(rawLink):
        return ParserTools.match_content("""(?<=people/)[^/'"]+""", rawLink)

    @staticmethod
    def get_tag_content(tag):
        u"""
        用于提取bs中tag.contents的内容
        """
        return "".join([unicode(x) for x in tag.contents])

    @staticmethod
    def get_attr(dom, attr, defaultValue=""):
        u"""
        获取bs中tag.content的指定属性
        若content为空或者没有指定属性则返回默认值
        """
        if dom is None:
            return defaultValue
        return dom.get(attr, defaultValue)

    @staticmethod
    def parse_date(date='1357-08-12'):
        if u'昨天' in date:
            return ParserTools.get_yesterday()
        if u'今天' in date:
            return ParserTools.get_today()
        return ParserTools.match_content(r'\d{4}-\d{2}-\d{2}', date, date)  # 一三五七八十腊，三十一天永不差！


class AuthorInfo(ParserTools):
    """
    实践一把《代码整洁之道》的做法，以后函数尽量控制在5行之内
    """

    def __init__(self, dom=None):
        self.set_dom(dom)
        return

    def set_dom(self, dom):
        self.info = {}
        if not (dom is None):
            self.dom = dom.find('div', class_='zm-item-answer-author-info')
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        if self.dom.find('img') is None:
            self.create_anonymous_info()
        else:
            self.parse_author_info()
        return

    def parse_author_info(self):
        self.create_anonymous_info()
        self.create_anonymous_info()
        self.create_anonymous_info()
        self.create_anonymous_info()
        return

    def create_anonymous_info(self):
        self.info['authorID'] = u"coder'sGirlFriend~"
        self.info['authorSign'] = u''
        self.info['authorLogo'] = u'http://pic1.zhimg.com/da8e974dc_s.jpg'
        self.info['authorName'] = u'匿名用户'
        return

    def parse_author_id(self):
        author = self.dom.find('a', class_='zm-item-link-avatar')
        link = self.get_attr(author, 'href')
        self.info['authorID'] = self.match_answer_id(link)
        return

    def parse_author_sign(self):
        sign = self.dom.find('strong', class_='zu-question-my-bio')
        self.info['authorSign'] = self.get_attr(sign, 'title')
        return

    def parse_author_logo(self):
        self.info['authorLogo'] = self.get_attr(self.dom.find('img'), 'src')
        return

    def parse_author_name(self):
        self.info['authorName'] = self.dom.find('a')[-1].text
        return


class Answer(ParserTools):
    """
    示例代码
    <div tabindex="-1" class="zm-item-answer  zm-item-expanded" itemscope="" itemtype="http://schema.org/Answer" data-aid="23458712" data-atoken="70095598" data-collapsed="0" data-created="1446209879" data-deleted="0" data-helpful="1" data-isowner="0" data-copyable="1">
<a class="zg-anchor-hidden" name="answer-23458712"></a>


<div class="zm-votebar">
<button class="up" aria-pressed="false" title="赞同">
<i class="icon vote-arrow"></i>
<span class="label">赞同</span>
<span class="count">7</span>
</button>
<button class="down" aria-pressed="false" title="反对，不会显示你的姓名">
<i class="icon vote-arrow"></i>
<span class="label">反对，不会显示你的姓名</span>
</button>
</div>


<div class="answer-head">
<div class="zm-item-answer-author-info">
<h3 class="zm-item-answer-author-wrap">


<a data-tip="p$t$abandonstone" class="zm-item-link-avatar" href="/people/abandonstone">
<img src="https://pic2.zhimg.com/9379d0b856df5796b3a21694cee452b5_s.jpg" class="zm-list-avatar" data-source="https://pic2.zhimg.com/9379d0b856df5796b3a21694cee452b5_s.jpg">
</a>



<a data-tip="p$t$abandonstone" href="/people/abandonstone">噶愛成神</a>，<strong title="INFP 彎而正直 中等偏下" class="zu-question-my-bio">INFP 彎而正直 中等偏下</strong>

</h3>
</div>
<div class="zm-item-vote-info " data-votecount="7">

<span class="voters">
<span class="user-block"><a data-tip="p$t$wei-yi-jing-58" href="http://www.zhihu.com/people/wei-yi-jing-58" class="zg-link" title="妖都妖子">妖都妖子</a>、</span><span class="user-block"><a data-tip="p$t$da-shuai-bi-77" href="http://www.zhihu.com/people/da-shuai-bi-77" class="zg-link" title="Freya Zheng">Freya Zheng</a>、</span><span class="user-block"><a data-tip="p$t$weng-weng-46-17" href="http://www.zhihu.com/people/weng-weng-46-17" class="zg-link" title="wEnG WeNg">wEnG WeNg</a></span>
</span>


<a href="javascript:;" class="more"> 等人赞同</a>


</div>
</div>
<div class="zm-item-rich-text js-collapse-body" data-resourceid="7011484" data-action="/answer/content" data-author-name="噶愛成神" data-entry-url="/question/37011291/answer/70095598">


<div class="zh-summary summary clearfix" style="display:none;">

老子不和男的結婚:）

</div>


<div class="zm-editable-content clearfix">
老子不和男的結婚:）

</div>

</div>
<a class="zg-anchor-hidden ac" name="23458712-comment"></a>
<div class="zm-item-meta zm-item-comment-el answer-actions clearfix">
<div class="zm-meta-panel">

<span class="answer-date-link-wrap">
<a class="answer-date-link meta-item" target="_blank" href="/question/37011291/answer/70095598">发布于 昨天 20:57</a>
</span>

<a href="#" name="addcomment" class=" meta-item toggle-comment">
<i class="z-icon-comment"></i>3 条评论</a>


<a href="#" class="meta-item zu-autohide" name="thanks" data-thanked="false"><i class="z-icon-thank"></i>感谢</a>



<a href="#" class="meta-item zu-autohide goog-inline-block goog-menu-button" name="share" role="button" aria-expanded="false" style="-webkit-user-select: none;" tabindex="0" aria-haspopup="true"><div class="goog-inline-block goog-menu-button-outer-box"><div class="goog-inline-block goog-menu-button-inner-box"><div class="goog-inline-block goog-menu-button-caption"><i class="z-icon-share"></i>分享</div><div class="goog-inline-block goog-menu-button-dropdown">&nbsp;</div></div></div></a>
<a href="#" class="meta-item zu-autohide" name="favo">
<i class="z-icon-collect"></i>收藏</a>




<span class="zg-bull zu-autohide">?</span>

<a href="#" name="nohelp" class="meta-item zu-autohide">没有帮助</a>

<span class="zg-bull zu-autohide">?</span>
<a href="#" name="report" class="meta-item zu-autohide goog-inline-block goog-menu-button" role="button" aria-expanded="false" style="-webkit-user-select: none;" tabindex="0" aria-haspopup="true"><div class="goog-inline-block goog-menu-button-outer-box"><div class="goog-inline-block goog-menu-button-inner-box"><div class="goog-inline-block goog-menu-button-caption">举报</div><div class="goog-inline-block goog-menu-button-dropdown">&nbsp;</div></div></div></a>



<span class="zg-bull">?</span>

<a href="/terms#sec-licence-1" target="_blank" class="meta-item copyright"> 作者保留权利 </a>



</div>
</div>
</div>
    """

    def __init__(self, dom=None):
        self.set_dom(dom)
        return

    def set_dom(self, dom):
        self.info = {}
        if not (dom is None):
            self.header = dom.find('div', class_='zm-item-vote-info')
            self.body = dom.find('div', class_='zm-editable-content')
            self.footer = dom.find('div', class_='zm-meta-panel')
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        self.parse_header_info()
        self.parse_answer_content()
        self.parse_footer_info()
        return

    def parse_header_info(self):
        self.parse_vote_count()
        return

    def parse_footer_info(self):
        self.parse_date_info()
        self.parse_comment_count()
        self.parse_no_record_flag()
        self.parse_href_info()
        return

    def parse_vote_count(self):
        self.info['answerAgreeCount'] = self.get_attr(self.header, 'data-votecount')
        return self.info['answerAgreeCount']

    def parse_answer_content(self):
        self.info['answerContent'] = self.body.text()
        return

    def parse_date_info(self):
        data_block = self.footer.find('a', class_='answer-date-link')
        commit_date = self.get_attr(data_block, 'data-tip')
        if commit_date == '':
            commit_date = data_block.text()
            self.info['editDate'] = self.info['commitDate'] = self.parse_date(commit_date)
        else:
            update_date = data_block.text()
            self.info['editDate'] = self.parse_date(update_date)
            self.info['commitDate'] = self.parse_date(commit_date)

    def parse_comment_count(self):
        comment = self.footer.find('a', name='addcomment').text()
        self.info['answerCommentCount'] = self.match_int(comment)
        return

    def parse_no_record_flag(self):
        no_record_flag = self.footer.find('a', class_='copyright').text()
        self.info['noRecordFlag'] = int(u'禁止转载' in no_record_flag)
        return

    def parse_href_info(self):
        href_tag = self.footer.find('a', class_='answer-date-link')
        href = self.get_attr(href_tag, 'href')
        self.parse_question_id(href)
        self.parse_answer_id(href)
        self.info['answerHref'] = "http://www.zhihu.com/question/{questionID}/answer/{answerID}".format(**self.info)
        return

    def parse_question_id(self, href):
        self.info['questionID'] = self.matchQuestionID(href)
        return

    def parse_answer_id(self, href):
        self.info['answerID'] = self.match_answer_id(href)
        return


class QuestionInfo(ParserTools):
    """
        特指single_question 和 single_answer中的内容
    """

    def __init__(self, dom=None):
        self.set_dom(dom)
        return

    def set_dom(self, dom):
        self.info = {}
        if not (dom is None):
            self.dom = dom
            self.side_dom = dom.find('div', _class='zu-main-sidebar')
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        self.parse_base_info()
        self.parse_status_info()
        return

    def parse_base_info(self):
        self.parse_question_id()
        self.parse_title()
        self.parse_desc()
        self.parse_comment_count()
        return

    def parse_question_id(self):
        meta = self.dom.select("meta[http-equiv='mobile-agent']")
        content = self.get_attr(meta, 'content', 0)
        self.info['question_id'] = self.match_question_id(content)
        return

    def parse_title(self):
        title = self.dom.select('#zh-question-title h2')
        self.info['title'] = title[0].string
        return

    def parse_desc(self):
        desc = self.dom.find(id='zh-question-detail')
        self.info['desc'] = desc.find('div', _class='zm-editable-content').string
        return

    def parse_comment_count(self):
        div = self.dom.find(id='zh-question-meta-wrap')
        comment = div.find('i', name='z-icon-comment')
        self.info['comment'] = self.match_int(comment.string)
        return

    def parse_status_info(self):
        self.parse_views()
        return

    def parse_followers_count(self):
        div = self.side_dom.find('div', _class='zh-question-followers-sidebar')
        div = div.find('div', _class='zg-gray-normal')
        strong = div.find('strong')
        self.info['followers'] = 0
        if not strong is None:
            self.info['followers'] = self.match_int(strong.string)
        return

    def parse_views(self):
        div = self.side_dom.find_all('div', _class='zm-side-section')[-1]
        views = div.find('strong')  # 在最后一个side-section中的第一个strong是问题浏览次数
        self.info['views'] = self.match_int(views.string)
        return

    def parse_answer_count(self):
        self.info['answers'] = 0  # 默认为0
        count = self.dom.select('#zh-answers-title a.zg-link-litblue, #zh-question-answer-num')
        if len(count) != 0:
            self.info['answers'] = self.match_int(count.string)
        return


class BaseParser(ParserTools):
    def __init__(self, content):
        BaseClass.logger.debug(u"开始解析网页")
        self.dom = BeautifulSoup(content, 'html.parser')
        self.answer_parser = Answer()

    def get_answer_list(self):
        u"""
        基础功能：获取答案列表
        需重载
        """
        return

    def get_extro_info(self):
        """
        扩展功能：获取额外信息
        需重载
        """
        return
