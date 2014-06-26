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
from    ZhihuHelp   import  *
    

import  os

import  sys#修改默认编码
reload( sys )
sys.setdefaultencoding('utf-8')

import  sqlite3#使用数据库管理数据
import  urllib2
import  socket#用于捕获超时错误
import  zipfile
import  pickle
import  threading#使用线程下载图片，直接默认20线程#知乎图片是用CDN分发的，不必担心
import  time#睡眠
import  re

import  ConfigParser#ini文件读取
######复制头文件#####3
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
import  sqlite3#数据库！
###########################################################
#数据库部分
import  pickle
import  socket#捕获Timeout错误


































    
    
    
    
    
    


def returnReDict():#返回编译好的正则字典#Pass
    Dict    =   {}
    Dict['_AgreeCount']                 =   re.compile(r'(?<=data-votecount=")\d*(?=">)')
    #Dict['_AnswerContent']              =   #直接使用<div class=" zm-editable-content clearfix">进行提取，需要先移除所有img与noscript标签，然后在解引用，原图片地址在新img标签里的data-original内
    Dict['_AnswerID']                   =   re.compile(r'(?<=<a class="answer-date-link meta-item" target="_blank" href="/question/\d{8}/answer/)\d{8}(?=">)')
    Dict['_QuestionID']                 =   re.compile(r'(?<=<a class="answer-date-link meta-item" target="_blank" href="/question/)\d{8}(?=/answer/\d{8})')#数字位数可能有误#不过对11年的数据也有效，貌似多虑了——除非知乎问题能突破5千万条，否则没必要更新
    Dict['_Questionhref']               =   re.compile(r'(?<=<a class="answer-date-link meta-item" target="_blank" href=")[/question\danswer]{34}(?=">)')
    Dict['_UpdateTime']                 =   re.compile(r'(?<=<a class="answer-date-link meta-item" target="_blank" href="/question/\d{8}/answer/\d{8}">).*(?=</a></span>)')#分为13：25、昨天 00:26、2013-05-07三种情况，需进一步处理
    Dict['_CommitCount']                =   re.compile(r'(?<=<i class="z-icon-comment"></i>).*?(?= )')#若转化为int失败则是添加评论#即为0条
    Dict['_ID']                         =   re.compile(r'(?<=<a data-tip="p\$t\$)[^"]*(?=" href="/people/)')#真精巧
    Dict['_Sign']                       =   re.compile(r'(?<=<strong title=").*?(?=" class="zu-question-my-bio">)')
    Dict['_UserIDLogoAdress']           =   re.compile(r'(?<=src=")http://p\d\.zhimg\.com[/\w]{7}[_\w]{11}\.jpg')
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
    if  text.find('<div class=" zm-editable-content clearfix">')==-1:#提前校验
        return  Dict

    def Help_ReadAnswer(t="",flag=True):
        u"""
        #辅助系函数
        *   用于提取答案内容，提高代码复用度    
        *   因为某些项匹配失败后应直接调用默认值，所以添加了Flag以做区分
        """
        try:
            Dict[t]      =   html_parser.unescape(ReDict['_'+t].search(text).group(0))
        except  AttributeError:
            if  flag:
                print   u"没有收集到"   +   t
                print   u"知乎页面结构已变动，程序无法正常运行，快上知乎@姚泽源喊他更新脚本" 
                return  False
            else    :
                pass
        return True

    #特殊处理
    #Dict['UserIDLogoAdress']=   ReDict['_UserIDLogoAdress'].search(text).group(0)
    #print   "UserIDLogoAdress    =   ",Dict['UserIDLogoAdress']
    textBuf    =   text
    try:
        listtext    =   []
        Buf   =   SuperRemoveTagAndContent(html_parser.unescape(returnTagContent(text=text,tagname='div',TrueTagName='<div class=" zm-editable-content clearfix">')),'<noscript>','</noscript>')
        #print   Buf
        for t   in  re.findall(r'<img.*?>',Buf):
            Buf =   Buf.replace(t,removeAttibute(t,['src']).replace('data-actualsrc="','src="'))
        Dict["AnswerContent"]   =   Buf
        #ErrorReportText(Dict["AnswerContent"])
        for t   in  re.findall(r'<img.*?>',text):
            text    =   text.replace(t,removeAttibute(t,['src']).replace('data-original','src'))
        #Dict["AnswerContent"]   =   removeAttibute(Dict["AnswerContent"],['src']).replace('data-original','src')
    except  AttributeError:
        print   u"答案内容没有收集到"
        print   u"知乎页面结构已变动，程序无法正常运行，快上知乎@姚泽源喊他更新脚本" 
        return  Dict
    Dict["QuestionTitle"]   =   html_parser.unescape(QuestionTitle)
    text  =  textBuf    
    try :                               
        ID                  =   ReDict['_ID'].search(text).group(0)
        _UserName    	    =	re.compile(r'(?<=<a data-tip="p\$t\$'+ID+r'" href="/people/'+ID+r'">).*?(?=</a>)')#   这里必须要用到已经捕获的ID，否则没法获得用户名
        Dict["UserName"]    =   html_parser.unescape(_UserName.search(text).group(0))
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
    try :
        Dict['CommitCount'] =   int(Dict['CommitCount'])
    except  :
        Dict['CommitCount'] =   0
    return Dict
def WorkForFetchUrl(url='',ReDict={},html_parser=None,AnswerDictList=[],ErrorList=[],IndexList=[]):#抓取回答链接#注意，Page是字符串#Pass)
    PostHeader  =   {
'Accept'    :   '*/*'                                                                                 
,'Accept-Encoding'   :'gzip,deflate,sdch'
,'Accept-Language'    :'zh,zh-CN;q=0.8,en-GB;q=0.6,en;q=0.4'
,'Connection'    :'keep-alive'
,'Host'    :'www.zhihu.com'
,'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'
,'Cookie':'_xsrf=9747077ec0374d469c91d06f4bf78c4d; q_c1=a5702f2ffc0344ae91e9efc0874012a8|1401117498000|1394290295000; q_c0="NTc1Mjk3OTkxMmM1NzU1N2MzZGQ5ZTMzMzRmNWVlMDR8MW9xU3hPdDF4U29BQlc4Qg==|1401117516|4bccb71dbbdd69c36ee800ef20586a6060ab8559";'
}
    try :
        content =   OpenUrl(urllib2.Request(headers=PostHeader,url=url.replace('\r','').replace('\n','')),Timeout=20).decode(encoding="utf-8",errors='ignore').replace('\r','').replace('\n','')#自己用，不发布
        if  content=='':
            raise   IOError('打开网页失败')
        title   =   re.search(r'(?<=<title>).*?(?=</title>)',content.replace('\r','').replace('\n','').replace(' ','')).group(0)
        #File    =   open(title+'.htm','w')
        #File.write(content)
        #File.close()
    except  IOError as e:
            print   e
            ErrorList.append(url)
            return
    except  ValueError as   e   :
            print   e
            ErrorReportText(Info=u'404网页已删除\t:\t'+str(e))
            return
    QuestionTitle   =   re.search('(?<=<title>).*?(?=</title>)',content).group(0)[:-6]
    for t   in  content.replace('\r','').replace('\n','').split('<div tabindex="-1"'):#直接忽略掉最后的答案
        #ErrorReportText(t)
        #ErrorReportText('\n-----------------------------\n')
        Dict    =   ReadAnswer(ReDict,html_parser,t,QuestionTitle)#使用的是单行模式，所以要去掉\r\n避免匹配失败
        if  Dict['UpdateTime']!='1970-01-01'    and Dict['AgreeCount']>5    and Dict['CommitCount']>1:
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

def Main(UrlList=[],Title=''):
    conn,cursor =   returnConnCursor()
    ErrorReportText(flag=False)#初始化错误报告文件
    Mkdir(u'./知乎答案集锦')
    Index   =   []
    Index   =   ThreadWorker(cursor,200,UrlList)
    conn.commit()
    f   =   open('Index.txt','w')
    #for k   in  f:
    #    Index.append(k)
    for k   in  Index:
        f.write(k+'\n')
    EpubBuilder(200,Index,Title)
    print   'over'
def trueMain():
    f   =   open('ReadList.txt','r')
    Url =   []
    for k   in  f:
        Url.append(k.replace('\n','').replace('\t',''))
    Main(Url[0  :50 ]   ,'1-50'     )
    Main(Url[50 :100]   ,'51-100'   )
    Main(Url[100:150]   ,'101-150'  )
    Main(Url[150:200]   ,'151-200'  )
    Main(Url[200:250]   ,'201-250'  )   
    Main(Url[250:300]   ,'251-300'  )
    #t   =    u'''<div class=" zm-editable-content clearfix">转自 @全球创意 的微博：<br /><br />下面是英国画家Louis Wain（以画 <b>猫 </b>著称）从正常状态到患上精神分裂症期间不同时期的作品<br /><br /><noscript><div class="duokan-image-single"><img height="1128" class="origin_image zh-lightbox-thumb" width="440" src="../images/9a7affe1b3f5e5a698194c673f6687e4_r.jpg"  alt="知乎图片"/></div></noscript><div class="duokan-image-single"><img height="1128" class="origin_image zh-lightbox-thumb lazy" width="440" src="../images/9a7affe1b3f5e5a698194c673f6687e4_r.jpg"  alt="知乎图片"/></div><br /><br />补充张大图：<br /><br /><noscript><div class="duokan-image-single"><img height="1024" class="origin_image zh-lightbox-thumb" width="802" src="../images/d7735604eb27de127d4bf51a5cec50c3_r.jpg"  alt="知乎图片"/></div>图片来源：</noscript><div class="duokan-image-single"><img height="1024" class="origin_image zh-lightbox-thumb lazy" width="802" src="../images/d7735604eb27de127d4bf51a5cec50c3_r.jpg"  alt="知乎图片"/></div>图片来源：<a href="http://plant-alchemy.com/cats" class=" wrap external" target="_blank" rel="nofollow">Louis Wain's Cats<i class="icon-external"></i></a></div>    
            #</div>'''
    
    
    #print   SuperRemoveTagAndContent(t,'<noscript>','</noscript>')



trueMain()
