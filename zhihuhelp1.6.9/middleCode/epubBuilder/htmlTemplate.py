# -*- coding: utf-8 -*-
def baseTemplate(dataDict = {}):
    u'''
    *   stdStruct 
    {
        'PageTitle' : '',
        'Guide'     : '',
        'Index'     : '',
        'Content'   : '',
    }
    '''
    return u"""
            <!DOCTYPE html>
            <html lang="zh-CN">
                <head>
                    <link rel="stylesheet" type="text/css" href="./markdownStyle.css"/>
                    <link rel="stylesheet" type="text/css" href="./userDefine.css"/>
                    <meta charset="utf-8" />
                    <title>%(PageTitle)s</title>
                </head>
                <body>
                %(Guide)s
                %(Index)s
                %(Content)s
                </body>
            </html>
            """ % dataDict

def guideTemplate(dataDict = {}):
    u'''
    *   stdStruct 
    {
        'title'    : '',
        'author'   : '',
        'desc'     : '',
        'guideImg' : '',
    }
    '''
    return u'''
            <center>
                <img  class="guide-img" src="../images/%(guideImg)s" />
                <h1>%(title)s</h1>
                <h3>%(author)s</h3>
                <p>%(desc)s</p>
            </center>
            ''' % dataDict

def indexTemplate(dataDict = {}):
    u'''
    *   stdStruct 
    {
        'title'    : '',
        'index'    : '',
    }
    '''
    return u'''
            <a href='#%(index)s'>%(index)s . %(title)s</a>
            ''' % dataDict


def contentTemplate(dataDict = {}):
    u'''
    *   stdStruct 
    {
        'QuestionContent' : '',
        'AnswerContent'   : '',
    }
    '''
    return u"""
            %(QuestionContent)s
            <hr />
            %(AnswerContent)s
            """ % dataDict

def questionContentTemplate(dataDict = {}):
    u'''
    *   stdStruct 
    {
        'index'   : '',
        'title'   : '',
        'desc'    : '',
        'comment' : '',
    }
    '''
    return u'''
            <div class='question' id='%(index)s'>
                <div class='question-title'>%(index)s.%(title)s</div>
                <div class='question-desc'>%(desc)s</div>
                <div class='question-comment'>评论数:%(comment)s</div>
            </div>
            ''' % dataDict

def answerContentTemplate(dataDict = {}):
    u'''
    *   stdStruct 
    {
        'authorLogo'    : '',
        'authorLink'    : '',
        'authorName'    : '',
        'authorSign'    : '',
        'answerContent' : '',
        'answerAgree'   : '',
        'answerComment' : '',
        'answerDate'    : '',
    }
    '''
    return u"""
            <div class='answer'>
                <div class='author-info'>
                    <div class='author-logo'>
                    %(authorLogo)s
                    </div>
                    <div class='author-name'>
                    <a href='%(authorLink)s'>%(authorName)s</a>,
                    </div>
                    <div class='author-sign'>
                    %(authorSign)s
                    </div>
                    <br >
                </div>
                <br >
                <div class='answer-content'>
                    %(answerContent)s
                </div>
                <br >
                <div class='answer-info'>
                    <div class='answer-agree'>
                    赞同数:%(answerAgree)s
                    </div>
                    <div class='answer-comment'>
                    评论数:%(answerComment)s
                    </div>
                    <div class='answer-date'>
                    更新日期:%(answerDate)s
                    </div>
                </div>
            </div>
            <br >
            <hr />
            """ % dataDict

