# -*- coding: utf-8 -*-
#公共库
import  sys#修改默认编码#放置于首位
reload( sys )
sys.setdefaultencoding('utf-8')

import  sqlite3#使用数据库管理数据

import  pickle


import  urllib2
import  urllib#编码请求字串，用于处理验证码
import  socket#用于捕获超时错误
import  zlib
import  threading
import  re
import  HTMLParser#HTML解码&lt;
import  json#在returnPostHeader中解析Post返回值


import  time
import  datetime

import  os#打开更新页面
####
#工具程序所用模块
import  ConfigParser#ini文件读取，Setting()
import  shutil#文件操作模块
#用于存放工具性函数
def CheckUpdate():#检查更新，强制更新#newCommitTag
    u"""
        *   功能
            *   检测更新。
            *   若在服务器端检测到新版本，自动打开浏览器进入新版下载页面
            *   网页请求超时或者版本号正确都将自动跳过
        *   输入
            *   无
        *   返回
            *   无
    """
    print   u"检查更新。。。"
    try:
        UpdateTime  =   urllib2.urlopen(u"http://zhihuhelpbyyzy-zhihu.stor.sinaapp.com/ZhihuHelpUpdateTime.txt",timeout=10)
    except:
        return
    Time        =   UpdateTime.readline().replace(u'\n','').replace(u'\r','')
    url         =   UpdateTime.readline().replace(u'\n','').replace(u'\r','')
    UpdateComment=  UpdateTime.read()#可行？
    if  Time=="2015-01-18":
        return
    else:
        print   u"发现新版本，\n更新说明:{}\n更新日期:{} ，点按回车进入更新页面".format(UpdateComment,Time)
        print   u'新版本下载地址:'+url
        raw_input()
        import  webbrowser
        webbrowser.open_new_tab(url)
    return
def Setting(ReadFlag=True,ID='',Password='',MaxThread='',PicDownload=''):#newCommitTag
    u"""
        *   功能
            *   在无参的情况下，读取设置文件，返回设置内容
            *   有参时，将参数写入设置文件中
        *   输入
            *   ReadFlag
                *   标志是否读取设置文件,否则重新进行设置
            *   ID
                *   用户名
            *   Password
                *   密码
            *   MaxThread
                *   最大线程数
        *   返回
             *   ID,Password,MaxThread

     """
    config  =   ConfigParser.SafeConfigParser()
    if  not os.path.isfile('setting.ini'):
        f   =   open('setting.ini','w')
        f.close()
    config.read('setting.ini')
    if  not config.has_section('ZhihuHelp'): 
        config.add_section('ZhihuHelp') 
    if  ReadFlag:
        ID          =   config.get('ZhihuHelp','UserName'   ,raw=True)
        Password    =   config.get('ZhihuHelp','Password'   ,raw=True)
        MaxThread   =   config.get('ZhihuHelp','MaxThread'  ,raw=True)
        PicDownload =   config.get('ZhihuHelp','PicDownload',raw=True)
                    #是否下载图片,0不下载，1下载普通图片，2下载高清大图
                    #若无以上任一设置，会抛出异常
    else    :
        if  ID!='':
            config.set('ZhihuHelp','UserName'   ,ID              )
            config.set('ZhihuHelp','Password'   ,Password        )
        if  MaxThread!='':
            config.set('ZhihuHelp','MaxThread'  ,str(MaxThread)  )
        if  PicDownload!='':
            config.set('ZhihuHelp','PicDownload',str(PicDownload))
        config.write(open('setting.ini','w'))
    if  PicDownload=='':
        PicDownload=1
    if  MaxThread=='':
        MaxThread=20
    return  ID,Password,int(MaxThread),int(PicDownload)

def PrintDict(Dict={},Front=''):
    u"""
        *   功能
            *   辅助类函数
            *   用于将字典内容以规则化的树状形式进行输出
        *   输入
            *   Dict
                *   待输出字典
            *   Front
                *   前导空格
        *   返回
            *   无
     """
    for r   in  Dict:
        if  type(Dict[r]) ==   type(Dict):
            print   '||'+'\t'+Front+'\t'+str(r)+':'
            PrintDict(Dict[r],Front=Front+'\t\t')
        else:
            if(len(Front)>0):
                Front_  =   (Front[:-1]+'∟'+Front[-1:])
            else:
                Front_=''
            print   '||'+u'\t'+Front_+str(r) ,':\t',str(Dict[r])
def PrintInOneLine(text=''):#Pass
    u"""
        *   功能
            *   反复在一行内输出内容
            *   输出前会先将光标移至行首，输出完毕后不换行
        *   输入
            *   待输出字符
        *   返回
            *  无
            *  若输出失败则将失败的文本输出至『未成功打开的页面.txt』内
     """
    try:
        sys.stdout.write("\r"+" "*60+'\r')
        sys.stdout.flush()
        sys.stdout.write(text)
        sys.stdout.flush()
    except:
        ErrorReportText(text)
def OpenUrl(Request,Timeout=5):#打开网页,只尝试一次，失败时返回空字符串，错误信息中包含未打开网址。话说字符串分割对空列表还有效否？#OKTag
    u"""
        *   功能
            *   打开Request中指定的网页，成功则返回原始网页内容\
                （只针对gzip进行解压缩，对其他格式例如jpg直接返回二进制内容，不进行额外处理）
            *   仅尝试一次，若打开失败则返回空字符串
        *   输入
            *   Request
                *   待打开的Http请求
            *   Timeout
                *   超时时间
        *   返回
            *   所打开网页的原始内容
            *   失败返回空字符串
     """
    try :
        Content =   urllib2.urlopen(Request,timeout=Timeout)
    except  urllib2.HTTPError   as  inst:
        print   inst
        if  int(inst.code/100) == 4:
            if int(inst.code) == 429:
                print u'同时打开的网页数量过多导致打开网页请求被知乎服务器拒绝，稍后重试'
            else:
                print   u'您所要找的网页在一片没有知识的荒原上'
                raise   ValueError(u"404 Not Found"+u"错误页面\t：\t"+Request.get_full_url())#此失败不可修复，通过报错直接跳过读取该页面
        else:
            if  int(inst.code/100)==    5:
                print   u"知乎正在紧张的撰写答案,服务器繁忙ing，稍后重试"
            else    :
                print   inst.code#未知错误
                print   u'打开网页时出现未知错误'
    except  urllib2.URLError as inst    :
        print   inst
        print   inst.reason#原因不详
        print   u'错误网址：'+Request.get_full_url()
        print   u'打开网页异常#稍后重试'
    except  socket.timeout  as  e   :
        print   e
        print   u"打开网页超时"
    else:
        if  Content.info().get(u"Content-Encoding")=="gzip":             
            try:    
                k   =   zlib.decompress(Content.read(), 16+zlib.MAX_WBITS)
            except  zlib.error as   ziperror:
                print   u'解压缩出错'
                print   u'错误信息：'
                print   zliberror
                raise   IOError(u"解压网页内容时出现错误"+u"错误页面\t：\t"+Request.get_full_url())#此失败不可修复，通过报错直接跳过读取该页面
        else    :
            k   =   Content.read()
        #去除了编码为utf-8部分
        return  k
    return  ''#失败则返回空字符串

def ErrorReturn(ErrorInfo=""):#返回错误信息并退出，错误信息要用unicode编码
    u"""
        *   功能
            *   打印错误信息，等待用户敲回车之后再退出
        *   输入
            *   ErrorInfo
                *   待打印错误信息
        *   返回
            *   无
     """
    print   ErrorInfo
    print   u"点按回车退出"
    raw_input()                                                                       
    os._exit(0)                                                                     

def setMaxThread():
    u"""
        *   功能
            *   引导用户设定最大线程数
            *   默认20，其间出现任何意外都会定为20
        *   输入
            *   无
        *   返回
            *   所设定的最大线程数
     """
    try:
        MaxThread=int(raw_input())
    except  ValueError as e  :
        print   e
        print   u'貌似输入的不是数...最大线程数重置为20，点击回车继续运行'
        MaxThread=20
        raw_input()
    if  MaxThread>200   or  MaxThread<1:
        if  MaxThread>200:
            print   u"线程不要太大好伐\n你线程开的这么凶残你考虑过知乎服务器的感受嘛"
        else:
            print   u"不要输负数啊我去"
        print u"最大线程数重置为20"
        MaxThread=20
        print u'猛击回车继续~'      
        raw_input()
    return  MaxThread     

def ThreadLiveDetect(ThreadList=[]):
    u"""
        *   功能
            *   等待给定list中的线程执行完毕
        *   输入
            *   线程列表
        *   返回
            *   待列表中的所有线程执行完毕后返回
            *   不会检测死锁
     """
    LiveFlag =   True
    while   LiveFlag:#等待线程执行完毕
        LiveFlag =   False
        Running   =   0
        for t   in  ThreadList:
            if  t.isAlive():
                LiveFlag=True
                Running+=1
        PrintInOneLine(   u"目前还有{}条线程正在运行,等待所有线程执行完毕".format(Running))
        time.sleep(1)
def ErrorReportText(Info='',flag=True):
    u"""
        *   功能
            *   将错误信息写入到『ErrorReport.txt』中
        *   输入
            *   Info
                *   错误信息
            *   flag
                *   标示符
                *   True    ->  新建文件
                *   False   ->  在原有文件上添加
        *   返回
            *   无
     """
    if  flag    :
        f   =open(u'ErrorReport.txt','ab')
    else    :
        f   =open(u'ErrorReport..txt','wb')
    f.write(Info)
    f.close()
def CopyFile(root='',TargetFile='',flag=True):#Pass
    u"""
        *   功能
            *   将root所指向的文件复制到TargetFile中
            *   复制错误会将文件地址输出至错误文件中
        *   输入
            *   root
                *   原文件地址
            *   TargetFile
                *   目标文件地址
            *   flag
                *   二进制标示符
                *   Fasle表示其为二进制文件
        *   返回
            *   无
     """
    try :
        if  flag    :
            f   =   open(root,'r')
            k   =   open(TargetFile,'w')
        else:
            k   =   open(TargetFile,'wb')
            f   =   open(root,'rb')
        k.write(f.read())
    except  IOError as e:
        print   e
        ErrorReportText(str(e))
    return

def ChooseTarget(url=''):#选择#Pass
    u"""
    *   功能
        *   识别不同的网址类别
    *   输入
        *   网址
    *   返回
        *   用户主页
            *   1，用户ID
        *   收藏夹主页
            *   2，收藏夹ID
        *   知乎圆桌
            *   3，圆桌ID
        *   知乎话题
            *   4，话题ID
    """
    try :
        ID      =   re.search(r'(?<=zhihu\.com/people/)[^/#\n\r]*',url).group(0)#匹配ID
    except  AttributeError:
        pass
    else:
        print   u'成功匹配到知乎ID，ID=',ID
        return  1,ID
    try :
        Collect =   re.search(r'(?<=zhihu\.com/collection/)\d*',url).group(0)#匹配收藏
    except  AttributeError:
        pass
    else:
        print   u'成功匹配到收藏夹，收藏夹代码=',Collect
        return  2,Collect
    try :
        Roundtable= re.search(r'(?<=zhihu\.com/roundtable/)[^/#\n\r]*',url).group(0)#知乎圆桌
    except  AttributeError:
        pass
    else:
        print   u'成功匹配到知乎圆桌，圆桌名=',Roundtable
        return  3,Roundtable
    try :
        Topic   =   re.search(r'(?<=zhihu\.com/topic/)\d*',url).group(0)#知乎话题
    except  AttributeError:
        pass
    else:
        print   u'成功匹配到话题，话题代码=',Topic
        return  4,Topic
    return  0,""

def Mkdir(DirName=u''):#PassTag
    u"""
        *   功能
            *   创建指定文件夹
            *   若文件夹已存在，则跳过
        *   输入
            *   文件夹名
                *   不需要指定路径
        *   返回
            *   无
     """
    if  DirName=='':
        return
    else:
        try :                        
            os.mkdir(DirName)
        except  OSError:
            pass#已存在
    return

###网页分析部分
def returnTagContent(text='',tagname='',TrueTagName=''):#NonUseTag#返回时会带上标签
    u"""
        *   功能
            *   返回指定Tag的内容，例如<h3><body id="65">asbd<h>asd</h>sad</body></h3>，返回<body id="65">asbd<h>asd</h>sad</body>
            *   输入
            *   text
                *   待处理内容
            *   tagname
                *   标签名
            *   TrueTagName
                *   起始标签名的全称，用于定位标签的位置
        *   返回
            *   Tag的内容
     """
    TagBeginStr     =   TrueTagName
    BeginPos        =   text.index(TagBeginStr)+len(TagBeginStr)
    rowEndPos       =   text.index('</'+tagname+'>')
    newText         =   text[BeginPos:rowEndPos]#初始字符位置
    #开始检测是否有重复标签
    completeTime    =   len(re.findall(r"<"+tagname+r'.*?>',newText)) 
    while   completeTime:
        bufPos  =   rowEndPos
        for i   in  range(completeTime):
            bufPos  =   text.index('</'+tagname+'>',bufPos+1)
        newText         =   text[rowEndPos:bufPos]
        completeTime    =   len(re.findall(r"<"+tagname+r'.*?>',newText)) 
        rowEndPos       =   bufPos
    return  text[BeginPos-len(TagBeginStr):rowEndPos+len(tagname)+3]
def removeTagContentWithTag(text='',TagList=[]):#移除List中所有的Tag
    for name,truename   in  TagList:
        try     :
            text    =   text.replace(returnTagContent(text=text,tagname=name,TrueTagName=tagname),'')
        except  :
            pass
    return text

def removeTag(text='',tagname=[]):#NonUseTag
    for tag in  tagname:
        text    =   text.replace('</'+tag+'>','')
        text    =   re.sub(r"<"+tag+r'.*?>','',text)
    return  text
def removeAttibute(text='',AttList=[]):#PassTag
    for Att in  AttList:
        for t   in  re.findall(r'\s'+Att+'[^\s^>]*',text):
            text    =   text.replace(t,'')
    return text

def EpubToHtml(filename=""):
    u"""
        *   功能
            *   在epub文件的基础上输出为一个单一Html格式文件
            *   假定起始位于根目录
        *   输入
            *   filename
                *   目标文件名  
                *   例如
                    *   姚泽源的知乎回答集锦(502BadGateway)
        *   返回
            *   无                                            
    """
    shutil.rmtree(u"./知乎答案集锦/"+filename,True)#移除之前生成的答案
    Mkdir(u"./知乎答案集锦/"+filename)
    htmlFile    =   open(u"./知乎答案集锦/"+filename+'/'+filename+u"_HTML网页版.html","wb")
    navigate_html=  ""#导航
    main_html   =   ""#主体部分
    #最后手工打开title.html，获取封面

    title_Template  =   re.compile(r"<title>.*?</title>")
    body_Template   =   re.compile(r"<body>.*?</body>"  )

    for htmlcache   in  sorted(filter(lambda x:x[0]=='c' and x[1]=='h',os.listdir(u"./电子书制作临时资源库/"+filename+u"_电子书制作临时文件夹/OEBPS/html")),cmp = lambda x,y:int(x[7:-5])-int(y[7:-5])  ) :#if  not (htmlcache != "title.html"    or  htmlcache != "cover.html"):#安全起见可以再排个序
        buf_file    =   open(u"./电子书制作临时资源库/"+filename+u"_电子书制作临时文件夹/OEBPS/html/"+htmlcache ,"r")
        t   =   buf_file.read().replace("\r",'').replace("\n",'')
        buf_title   =   title_Template.search(t).group(0)[7:-8]
        buf_body    =   body_Template.search(t).group(0)[6:-7]
        navigate_html+= '<li><a href = "#%(index)s">%(title)s</a></li>\n'%{'index':htmlcache[:-5],'body':buf_body[5:-5],'title':buf_title}
        main_html   +=  '<hr/><br/><div id="%(index)s">%(body)s</div>\n '%{'index':htmlcache[:-5],'body':buf_body[5:-5]}
        buf_file.close()
    
    buf_file    =   open(u"./电子书制作临时资源库/"+filename+u"_电子书制作临时文件夹/OEBPS/html/cover.html" ,"r")
    t   =   buf_file.read().replace("\r",'').replace("\n",'')
    buf_title   =   re.search(r"<head>.*?</head>",t).group(0)
    buf_body    =   re.search(r"<body>.*?</body>",t).group(0)[6:-7]
    t   =   u'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">%(title)s\n<body>\n%(body)s\n<div id="index"><h2>目录</h2><ol>%(index)s</ol></div>%(main)s<body/>'%{'title':buf_title,'body':buf_body[5:-5],'index':navigate_html,'main':main_html}
    htmlFile.write(t.replace('src="../images/','src="./images/'))
    htmlFile.close()
    shutil.copytree(u"./电子书制作临时资源库/"+filename+u"_电子书制作临时文件夹/OEBPS/images",u"./知乎答案集锦/"+filename+'/images')
    shutil.copy(u"./电子书制作临时资源库/"+filename+u"_电子书制作临时文件夹/OEBPS/stylesheet.css",u"./知乎答案集锦/"+filename+'/')


