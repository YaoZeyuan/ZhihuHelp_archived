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
        'titleCommentCount' : '',
    }
    '''
    return u'''
<div class='title'>
    <div class='title-header'>
        <div class='title-image'>
          <div class='text-center'>
            {titleImage}
          </div>
        </div>
    </div>
    <div class='title-body'>
        <div class='title-name'>
          <h1>
            {titleName}
          </h1>
        </div>
        <div class='title-desc'>
            {titleDesc}
        </div>
    </div>
    <div class='title-footer'>
        <div class='title-comment-count'>
            {titleCommentCount}
        </div>
    </div>
</div><br />'''.format(**dataDict)

def contentBodyTemplate(dataDict = {}):
    u'''
    *   stdStruct 
    {
        'authorLogo'   : '',
        'authorName'   : '',
        'authorSign'   : '',
        'content'      : '',
        'agreeCount'   : '',
        'commentCount' : '',
        'updateDate'   : '',
    }
    '''
    return u"""
<div class='content'>
    <div class='content-header'>
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
    <br />
    <div class='content-body'>
        {content}
    </div>
    <div class='content-footer'>
        <div class='agree-count'>
            {agreeCount}
        </div>
        <div class='comment-count'>
            {commentCount}
        </div>
        <div class='update-date'>
            {updateDate}
        </div>
    </div>
</div>
<hr />""".format(**dataDict)

def infoPageTemplate(dataDict = {}):
    return '''
<div class='info-page'>
  <div class='base-info'>
    <div class='title'>{title}</div>
    <div></div>
  </div>
  <br />
  <div>
    <div class='copy-right'>{copyRight}</div>
    <div ></div>
  </div>
</div>
    '''.format(**dataDict)

