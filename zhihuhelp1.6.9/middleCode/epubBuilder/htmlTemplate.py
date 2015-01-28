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
                    <meta charset="utf-8" />
                    <title>{PageTitle}</title>
                </head>
                <body>
                {Guide}
                {Index}
                {Content}
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
                <img  class="guide-img" src="../images/{guideImg}" />
                <h1>{title}</h1>
                <h3>{author}</h3>
                <p>{desc}</p>
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
            <a href='#{index}'>{index} . {title}</a>
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
            {QuestionContent}
            <br />
            <hr />
            {AnswerContent}
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
            <div class='question' id='{index}'>
                <div class='question-index'>{index}</div>
                <div class='question-title'>{title}</div>
                <div class='question-desc'>{desc}</div>
                <div class='question-comment'>{comment}</div>
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
                    {authorLogo}
                    </div>
                    <div class='author-name'>
                    <a href='{authorLink}'>{authorName}</a>,
                    </div>
                    <div class='author-sign'>
                    {authorSign}
                    </div>
                </div>
                <div class='answer-content'>
                    {answerContent}
                </div>
                <div class='answer-info'>
                    <div class='answer-agree'>
                    {answerAgree}
                    </div>
                    <div class='answer-comment'>
                    {answerComment}
                    </div>
                    <div class='answer-date'>
                    {answerDate}
                    </div>
                </div>
            </div>
            <hr />
            """ % dataDict

