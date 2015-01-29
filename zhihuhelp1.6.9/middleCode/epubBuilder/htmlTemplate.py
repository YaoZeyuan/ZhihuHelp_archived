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
            <br />
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
                <div class='question-index'>%(index)s</div>
                <div class='question-title'>%(title)s</div>
                <div class='question-desc'>%(desc)s</div>
                <div class='question-comment'>%(comment)s</div>
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
                </div>
                <div class='answer-content'>
                    %(answerContent)s
                </div>
                <div class='answer-info'>
                    <div class='answer-agree'>
                    %(answerAgree)s
                    </div>
                    <div class='answer-comment'>
                    %(answerComment)s
                    </div>
                    <div class='answer-date'>
                    %(answerDate)s
                    </div>
                </div>
            </div>
            <hr />
            """ % dataDict

