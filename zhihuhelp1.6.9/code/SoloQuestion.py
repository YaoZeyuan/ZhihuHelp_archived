# -*- coding: utf-8 -*-
import  urllib2
import  HTMLParser
import  re
import  zlib
import  threading
import  time
import  datetime
import  HTMLParser#HTML解码&lt;
import  json#在returnPostHeader中解析Post返回值
import  os#打开更新页面

import  urllib#编码请求字串，用于处理验证码
from    ZhihuEpub   import  *
PostHeader  =   OldPostHeader()
f   =   open('ReadList.txt','r')

for t   in  f:
    
    
    
    
    
    
    
    
    
    
    
    
    
    


def returnReDict():#返回编译好的正则字典#Pass
    Dict    =   {}
    Dict['_AgreeCount']                 =   re.compile(r'(?<=data-votecount=")\d*(?=">)')
    Dict['_AnswerContent']              =   #直接使用<div class=" zm-editable-content clearfix">进行提取，需要先移除所有img与nosprict标签，然后在解引用，原图片地址在新img标签里的data-original内
    Dict['_AnswerID']                   =   re.compile(r'(?<=<a class="answer-date-link meta-item" target="_blank" href="/question/\d{8}/answer/)\d{8}(?=">)')
    Dict['_Questionhref']               =   re.compile(r'(?<=<a class="answer-date-link meta-item" target="_blank" href=")[/question\danswer]{34}(?=">)')
    Dict['_UpdateTime']                 =   re.compile(r'(?<=<a class="answer-date-link meta-item" target="_blank" href="/question/\d{8}/answer/\d{8}">).*(?=</a></span></textarea>)')#分为13：25、昨天 00:26、2013-05-07三种情况，需进一步处理
    Dict['_CommitCount']                =   re.compile(r'(?<=<i class="z-icon-comment"></i>).*?(?= )')#若转化为int失败则是添加评论#即为0条
    Dict['_ID']                         =   re.compile(r'(?<=<a data-tip="p\$t\$)[^"]*(?=" href="/people/)')#真精巧
    Dict['_Sign']                       =   re.compile(r'(?<=<strong title=").*?(?=" class="zu-question-my-bio">)')
    Dict['_UserIDLogoAdress']           =   re.compile(r'(?<=src=")http://p\d\.zhimg\.com[/\w]{7}[_\w]{11}\.jpg(?=" class="zm-list-avatar)')
    Dict['_UnSuccessName']              =   re.compile(r'(?<=<h3 class="zm-item-answer-author-wrap">).*(?=</h3></div>)')#?存疑
    return  Dict

def ReadAnswer(ReDict,html_parser,text="",QuestionTitle=''):#UnitTest#newCommitTag
    Dict={}    
    Dict["ID"]              =   ""   ##    
    Dict["Sign"]            =   ""#
    Dict["AgreeCount"]      =   0#
    Dict["CommitCount"]     =   0#
    Dict["QuestionID"]      =   ""#
    Dict["AnswerID"]        =   ""#
    Dict["UpdateTime"]      =   "1970-01-01"#
    Dict["QuestionTitle"]   =   ""  ##
    Dict["Questionhref"]    =   ""  #
    Dict["AnswerContent"]   =   ""  ##
    Dict["UserName"]        =   "ErrorName" ##
    Dict['UserIDLogoAdress']=   ''  #
    if  text=='':
        return  Dict
    def Help_ReadAnswer(t="",flag=True):
        u"""
        #辅助系函数
        *   用于提取答案内容，提高代码复用度    
        *   因为某些项匹配失败后应直接调用默认值，所以添加了Flag以做区分
        """
        try:
            Dict[t]      =   ReDict['_'+t].search(text).group(0)
        except  AttributeError:
            if  flag:
                print   u"没有收集到"   +   t
                print   u"知乎页面结构已变动，程序无法正常运行，快上知乎@姚泽源喊他更新脚本" 
                return  False
            else    :
                pass
        return True

    #特殊处理
    
    try:
        Dict["AnswerContent"]   =   html_parser.unescape(removeTag(returnTagContent(text=t,tagname='div',TrueTagName='<div class=" zm-editable-content clearfix">'),['img','noscript']))
        Dict["AnswerContent"]   =   removeAttibute(Dict["AnswerContent"],['src']).replace('data-original','src')
    except  AttributeError:
        print   u"答案内容没有收集到"
        print   u"知乎页面结构已变动，程序无法正常运行，快上知乎@姚泽源喊他更新脚本" 
        return  Dict
    
    Dict["QuestionTitle"]   =   QuestionTitle
    try :                               
        ID                  =   ReDict['_ID'].search(text).group(0)
        _UserName    	    =	re.compile(r'(?<=<a data-tip="p\$t\$'+ID+r'" href="/people/'+ID+r'">).*?(?=</a>)')#   这里必须要用到已经捕获的ID，否则没法获得用户名
        Dict["UserName"]    =   _UserName.search(text).group(0)
    except  AttributeError  :
        try :#对应于知乎用户与匿名用户两种情况
            Dict["UserName"]    =   ReDict['_UnSuccessName'].search(text).group(0)
            ID                  =   '404NotFound!'
        except  AttributeError:
            Dict["UserName"]    =   u"知乎用户"
            ID                  =   'ZhihuUser!'

    Dict["ID"]              =   ID
    
    #常规匹配   
    #时间放到最后，因为要靠时间验证是否匹配成功
    for t   in  ["AgreeCount","QuestionID","AnswerID","UpdateTime","Questionhref"]:
        if  Help_ReadAnswer(t):
            pass
        else:
            return Dict
    
    for t   in  ['UserIDLogoAdress','Sign','CommitCount']:    
        if  Help_ReadAnswer(t,False):
            pass
        else:
            return Dict

    Dict["Questionhref"]    =   'http://www.zhihu.com'+Dict["Questionhref"]
    
    if  len(Dict["UpdateTime"])!=10 :        
        if  len(Dict["UpdateTime"])!=5  :
            Dict["UpdateTime"]  =   time.strftime(u'%Y-%m-%d',time.localtime(time.time()-86400))#昨天
        else    :
            Dict["UpdateTime"]  =   time.strftime(u'%Y-%m-%d',time.localtime(time.time()))#今天
    
    return Dict
def WorkForFetchUrl(url='',ReDict={},html_parser=None,AnswerDictList=[],ErrorList=[],IndexList=[]):#抓取回答链接#注意，Page是字符串#Pass)
    try :
        content =   OpenUrl(urllib2.Request(headers=PostHeader,url=t.replace('\r','').replace('\n','')),Timeout=30).decode(encoding="utf-8",errors='ignore').replace('\r','').replace('\n','')
        title   =   re.search(r'<title>*?</title>',content.replace('\r','').replace('\n','').replace(' ','')).group(0)
        File    =   open(title+'.htm','w')
        File.write(content)
        File.close()
    except  IOError as e:
            print   e
            ErrorList.append(url)
            return
    except  ValueError as   e   :
            print   e
            ErrorReportText(Info=u'404网页已删除\t:\t'+str(e))
            return
    QuestionTitle   =   re.search('(?<=<title>).*?(?=</title>)',content).group(0)
    for t   in  content.split('<div tabindex="-1" class="zm-item-answer" data-aid=')[1:-2]:#直接忽略掉最后的答案
        Dict    =   ReadAnswer(ReDict,html_parser,t,QuestionTitle)#使用的是单行模式，所以要去掉\r\n避免匹配失败
        if  Dict['UpdateTime']!='1970-01-01':
            AnswerDictList.append(Dict)
            IndexList.append(Dict["Questionhref"])#此处可以加限制条件
def ThreadWorker(cursor=None,MaxThread=200,UrlList=[]):#newCommitTag
    MaxPage =   len(UrlList)
    ReDict  =   returnReDict()
    AnswerDictList=[]#储存Dict，一并执行SQL
    html_parser=HTMLParser.HTMLParser()
    ThreadList=[]
    Times       =   0
    ErrorCount  =   0
    LoopFlag    =   True
    ErrorList   =   []
    IndexList   =   []
    for Page in  UrlList:
        ThreadList.append(threading.Thread(target=WorkForFetchUrl,args=(Page,ReDict,html_parser,AnswerDictList,ErrorList,IndexList)))
    
    while   Times<10    and LoopFlag:
        print   u'开始第{}遍抓取，本轮共有{}张页面待抓取,共尝试10遍'.format(Times+1,len(ThreadList))
        for Page in  range(MaxPage):
            if  threading.activeCount()-1 <   MaxThread:#实际上是总线程数
                ThreadList[Page].start()#有种走钢丝的感觉。。。
            else    :
                PrintInOneLine(u'正在读取答案页面，线程库中还有{}条线程等待运行'.format(MaxPage-Page))
                time.sleep(1)
        ThreadLiveDetect(ThreadList)

        LoopFlag    =   False
        MaxPage     =   0
        ThreadList  =   []
        for t   in  ErrorList:
            ThreadList.append(threading.Thread(target=WorkForFetchUrl,args=(t,ReDict,html_parser,AnswerDictList,ErrorList,IndexList)))
            MaxPage     +=  1
            LoopFlag    =   True
        Times   +=  1
        ErrorList   =   []
        if  LoopFlag:
            print   u'第{}遍答案抓取执行完毕，{}张页面抓取失败,3秒后进行下一遍抓取'.format(Times+1,ErrorCount)
            time.sleep(3)
    DictNo      =   0#美化输出
    DictCountNo =   len(AnswerDictList)
    for Dict    in  AnswerDictList:
        DictNo  +=  1
        PrintInOneLine(u'正在将第{}/{}个答案存入数据库中'.format(DictNo,DictCountNo))
        AppendDictIntoDataBase(cursor,Dict)
    return  IndexList
def AppendDictIntoDataBase(cursor=None,Dict={}) :   #假定已有数据库#PassTag
    bufDict     =   Dict
    bufAnswerContent    =   bufDict['AnswerContent']  
    del bufDict['AnswerContent']
    SaveToDB(cursor=cursor,NeedToSaveDict=bufDict,primarykey='Questionhref',TableName='AnswerInfoTable')
    bufDict                     =   {}
    bufDict['AnswerContent']    =   bufAnswerContent
    bufDict['Questionhref']     =   Dict['Questionhref']
    SaveToDB(cursor=cursor,NeedToSaveDict=bufDict,primarykey='Questionhref',TableName='AnswerContentTable')
    return 


