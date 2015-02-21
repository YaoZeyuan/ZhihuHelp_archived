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
    if dataDict['Guide'] == '':
        return u"""
            <!DOCTYPE html>
            <html lang="zh-CN">
                <head>
                    <link rel="stylesheet" type="text/css" href="../markdownStyle.css"/>
                    <link rel="stylesheet" type="text/css" href="../userDefine.css"/>
                    <meta charset="utf-8" />
                    <title>%(PageTitle)s</title>
                </head>
                <body>
                %(Index)s
                %(Content)s
                </body>
            </html>
            """ % dataDict
    else:
        return u"""
            <!DOCTYPE html>
            <html lang="zh-CN">
                <head>
                    <link rel="stylesheet" type="text/css" href="../markdownStyle.css"/>
                    <link rel="stylesheet" type="text/css" href="../userDefine.css"/>
                    <meta charset="utf-8" />
                    <title>%(PageTitle)s</title>
                </head>
                <body>
                %(Guide)s
                <hr />
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
            <div class="text-center">
                <img  class="guide-img" src="../images/%(guideImg)s" />
                <h1>%(title)s</h1>
                <h3>%(author)s</h3>
                <p>%(desc)s</p>
            </div>
            ''' % dataDict

def oneFileIndexTemplate(dataDict = {}):
    u'''
    *   stdStruct 
    {
        'title'    : '',
        'index'    : '',
    }
    '''
    return u'''
            <a href='#%(index)s'>%(index)s . %(title)s</a>
            <br />
            ''' % dataDict

def treeFileIndexTemplate(dataDict = {}):
    u'''
    *   stdStruct 
    {
        'title'    : '',
        'index'    : '',
        'href'     : '',
    }
    '''
    return u'''
            <a href='%(href)s'>%(index)s . %(title)s</a>
            <br />
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
    if dataDict['desc'] == '':
        return u'''
            <div class='question' id='%(index)s'>
                <div class='question-title'>%(index)s.%(title)s</div>
            </div>
            ''' % dataDict

    else:
        return u'''
            <div class='question' id='%(index)s'>
                <div class='question-title'>%(index)s.%(title)s</div>
                <hr />
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

def simpleIndexTemplate(indexContent = ''):
    return u'''
            <!DOCTYPE html>
            <html lang="zh-CN">
                <head>
                    <link rel="stylesheet" type="text/css" href="./markdownStyle.css"/>
                    <link rel="stylesheet" type="text/css" href="./userDefine.css"/>
                    <meta charset="utf-8" />
                    <title>目录</title>
                </head>
                <body>
                <p class="text-center">目录</p>
                <br />
                {}
                </body>
            </html>'''.format(indexContent)
