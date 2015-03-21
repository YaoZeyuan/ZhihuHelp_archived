# -*- coding: utf-8 -*-
def baseTemplate(dataDict = {}):
    u'''
    *   stdStruct 
    {
        'Title'  : '',
        'Header' : '',
        'Body'   : '',
        'Footer' : '',
    }
    '''
    return u"""
            <!DOCTYPE html>
            <html lang="zh-CN">
                <head>
                    <meta charset="utf-8" />
                    <link rel="stylesheet" type="text/css" href="../markdownStyle.css"/>
                    <link rel="stylesheet" type="text/css" href="../userDefine.css"/>
                    <title>{Title}</title>
                </head>
                <body>
                {Header}
                {Body}
                {Footer}
                </body>
            </html>
            """.format(**dataDict) 

def structTemplate(dataDict={}):
    u'''
    *   stdStruct 
    {
        'leftColumn'   : '',
        'middleColumn' : '',
        'rightColumn'  : '',
    }
    '''
    return u"""
<div class='left-column'>
{leftColumn}
</div>
<div class='middle-column'>
{middleColumn}
</div>
<div class='right-column'>
{rightColumn}
</div>
    """.format(**dataDict)


def contentTemplate(dataDict = {}):
    u'''
    *   stdStruct 
    {
        'contentHeader' : '',
        'contentBody'   : '',
        'contentFooter' : '',
    }
    '''
    return u"""
<div class='content'>
  <div class='content-header'>
    {contentHeader}
  </div>
  <div class='content-body'>
    {contentBody}
  </div>
  <div class='content-body'>
    {contentFooter}
  </div>
</div>
            """.format(**dataDict)

def contentHeaderTemplate(dataDict = {}):
    u'''
    *   stdStruct 
    {
        'titleImage'         : '',
        'titleName'          : '',
        'titleDesc'          : '',
        'titleCommentsCount' : '',
    }
    '''
        return u'''
<div class='title'>
    <div class='title-header'>
        <div class='title-image'>
            {titleImage}
        </div>
    </div>
    <div class='title-body'>
        <div class='title-name'>
            {titleName}
        </div>
        <div class='title-desc'>
            {titleDesc}
        </div>
    </div>
    <div class='title-foot'>
        <div class='title-comment-count'>
            {titleCommentsCount}
        </div>
    </div>
</div>'''.format(**dataDict)

def contentBodyTemplate(dataDict = {}):
    u'''
    *   stdStruct 
    {
        'authorLogo'    : '',
        'authorName'    : '',
        'authorSign'    : '',
        'content'       : '',
        'agreeCount'    : '',
        'commentsCount' : '',
        'updateTime'    : '',
    }
    '''
    return u"""
<div class='content'>
    <div class='content-head'>
        <div class='author-info'>
            <div class='author-logo'>
                {authorLogo}
            </div>
            <div class='author-name'>
                {authorName}
            </div>
            <div class='author-sign'>
                {authorSign}
            </div>
        </div>
    </div>
    <div class='content-body'>
        {content}
    </div>
    <div class='content-foot'>
        <div class='agree-count'>
            {agreeCount}
        </div>
        <div class='comment-count'>
            {commentsCount}
        </div>
        <div class='update-time'>
            {updateTime}
        </div>
    </div>
</div>
<hr />""".format(**dataDict)
