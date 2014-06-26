# -*- coding: utf-8 -*-
import  os

import  sys#修改默认编码
reload( sys )
sys.setdefaultencoding('utf-8')

import  sqlite3#使用数据库管理数据
import  urllib2
import  zipfile
import  pickle
import  threading#使用线程下载图片，直接默认20线程#知乎图片是用CDN分发的，不必担心
import  time#睡眠
import re

def PrintInOneLine(text=''):
    sys.stdout.write("\r                                                                          \r")
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()
def OpenHttpPage(url=''):#打开网页,负责下载图片或者打开json列表,只尝试一次，失败时返回空字符串，错误信息中包含未打开网址。#
    try :
        Content =   urllib2.urlopen(url=url,timeout=10)
    except  urllib2.HTTPError   as  inst:
        print   inst
        if  int(inst.code/100)   ==   4:
            print   u'您所要找的网页在一片没有知识的荒原上'#不报错
            raise   IOError(u"404 Not Found"+u"错误页面\t：\t"+Request.get_full_url())#此失败不可修复，通过报错直接跳过读取该页面
            return  ''
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
                raise   IOError(u"解压缩错误"+u"错误页面\t：\t"+Request.get_full_url())#此失败不可修复，通过报错直接跳过读取该页面
                k   =   ""
        else    :
            k   =   Content.read()
        #k   =   k.decode(u"utf-8",errors="ignore")#不进行编码，原样返回
        return  k
    return  ''#失败则返回空字符串

def CheckImgFileExist(CheckList=[],ErrorList=[]):
    for url in  CheckList:
        MetaName    =   u'../知乎图片池/'   +   PixName(url)
        if  not os.path.isfile(MetaName):
            ErrorList.append(url)

def DownloadPicWithThread(ImgList=[],MaxThread=20):#添加图片池功能#当图片下载完成时在ImgList中删除之
    Time=0
    MaxPage     =   len(ImgList)
    ErrorList   =   []
    while   Time<10 and MaxPage!=0:
        Buf_ImgList =   []
        Time+=1
        ThreadList  =   []
        for t   in  ImgList:#因为已下载过的文件不会重新下载，所以直接重复执行十遍，不必检测错误#待下载的文件可能会突破万这一量计，所以还是需要一些优化
            ThreadList.append(threading.Thread(target=DownloadImg,args=(t,Buf_ImgList,)))
        for Page in  range(MaxPage):
            if  threading.activeCount()-1 <   MaxThread:#实际上是总线程数
                ThreadList[Page].start()
            else    :
                print   u'第({}/10)轮下载图片，线程库中还有{}条线程等待运行'.format(Time,MaxPage-Page)
                time.sleep(1)

        Thread_LiveFlag =   True
        while   Thread_LiveFlag:#等待线程执行完毕
            Thread_LiveFlag =   False
            ThreadRunning   =   0
            for t   in  ThreadList:
                if  t.isAlive():
                    Thread_LiveFlag=True
                    ThreadRunning+=1
            print   u"第({}/10)轮下载图片，目前还有{}条线程正在运行,等待所有线程执行完毕".format(Time,ThreadRunning)
            if  ThreadRunning>0:
                time.sleep(1)

        ImgList     =       list(set(ImgList)-set(Buf_ImgList))#剔除不能下载的图片链接地址
        ErrorList   +=      Buf_ImgList#将下载失败的图片列表储存起来
        Buf_ImgList =       []  
        CheckImgFileExist(CheckList=ImgList,ErrorList=Buf_ImgList)
        ImgList     =       Buf_ImgList
        MaxPage     =       len(ImgList)
        if  MaxPage !=0:
            print   u'第{}轮下载执行完毕，剩余{}张图片待下载，若下载失败的图片过多可以调用迅雷进行下载，待下载图片列表为『程序所在文件夹\电子书制作临时资源库\待下载图片列表.txt』，将迅雷下载下来的图片放置于『程序所在文件夹\电子书制作临时资源库\知乎图片池』中即可'.format(Time,MaxPage)
            time.sleep(1)#休息一秒后继续
        else    :
            print   u'所有图片下载完毕'
    print   u'开始输出下载失败的图片列表'
    f   =   open(u'./下载失败的图片列表.txt','a')#输出下载失败列表
    f.write(u'\n-------------------------------------------\n')
    f.write(u'时间戳:\t'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')  
    f.write(u'-------------------------------------------\n')
    print   '以下文件下载失败'
    for t   in  ErrorList:
        f.write(t+'\n')
        PrintInOneLine(t)
    f.close()
def returnCursor():
    if  os.path.isfile('./ZhihuDateBase.db'):
        conn    =   sqlite3.connect("./ZhihuDateBase.db")
        conn.text_factory = str
        cursor  =   conn.cursor()
        return  cursor
    else:
        print   u'抱歉，没有找到数据库，请先运行知乎助手'
        return  None
def Mkdir(DirName=u''):
    if  DirName=='':
        return
    else:
        try :                        
            os.mkdir(DirName)
        except  OSError:
            pass#已存在
    return
def CreateMimeType():
    f   =   open('mimetype','w')
    f.write('application/epub+zip')
    f.close()
def CreateContainer_XML():
    f   =   open('META-INF/container.xml','w')      
    f.write('''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf"
     media-type="application/oebps-package+xml" />
  </rootfiles>
</container>''')
    f.close()
def returnTagContent(text='',tagname=''):
    TagBeginStr     =   re.search(r"<"+tagname+r'.*?>',text).group(0)#如果没有这个标签会报AttributeError
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
    return  text[BeginPos:rowEndPos]
def removeTag(text='',tagname=[]):
    text    =   text.replace('</'+tagname+'>','')
    text    =   re.sub(r"<"+tagname+r'.*?>','',text)
    return  text
def removeAttibute(text='',AttList=[]):
    for Att in  AttList:
        for t   in  re.findall(Att+'[^\s^>]*',text):
            text    =   text.replace(t,'')
    return text
def closeimg(text='',ImgList=[]):
    for t   in  re.findall(r'<img.*?>',text):
        text    =   text.replace(t,fixPic(removeAttibute(t,['data-rawwidth','data-original']).replace("data-rawheight",'height')[:-1]+u'  alt="知乎图片"/>',ImgList))
    return text
def PixName(t):
    return  re.search(r'[^/"]*?\.jpg',t).group(0)
def fixPic(t='',ImgList=[]):
    for k   in  re.findall(r'(?<=src=")http://[/\w\.^"]*?zhimg.com[/\w^"]*?.jpg',t):
        t   =   t.replace(k,'../images/'+PixName(k))
        ImgList.append(k)
    return  t
def DownloadImg(imghref='',ErrorList=[]):#下载失败时应报错或重试#外围应再套一层检测错误的函数
    try :
        CheckName   =   u'../知乎图片池/'
        try :
            MetaName    =     PixName(imghref)
        except  AttributeError:#需要编写测试用例
            print       u'程序出现错误，未能成功提取图片链接'
            print       u'目标网址'+imghref
            print       u'已陷入死循环，请关闭程序'
            raise       IOError('over')
            MetaName    =     ''
        imgfilename =   './OEBPS/images/'+MetaName   
        if  not os.path.isfile(CheckName+MetaName):
            k   =   OpenHttpPage(url=imghref)#这里会返回IOError
            if  len(k)==0:
                print   u'Download image error'
                return 0
            imgfile     =   open(imgfilename,"wb")
            imgfile.write(k)
            imgfile.close()
        if  not os.path.isfile(imgfilename):
            imgfile     =   open(imgfilename,"wb")
            imgpoolfile =   open(CheckName+MetaName,"rb")
            imgfile.write(imgpoolfile.read())
            imgfile.close()
            imgpoolfile.close()
    except  IOError as  e:
        ErrorList.append(imghref)
        print   u'图片{}下载失败'.format(MetaName)
        print   u'错误信息:'
        print   e
    else    :
        print   u'图片{}下载成功'.format(MetaName)
    return 0
def CreateOPF(OPFInfoDict={},Mainfest='',Spine=''):#生成文件函数均假定当前目录为电子书根目录
    f   =   open('./OEBPS/content.opf','w')
    XML =   u'''<?xml version='1.0' encoding='utf-8'?>
               <package unique-identifier="%(AuthorAddress)s" version="2.0">
               <metadata xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/"  >
               <dc:title>%(BookTitle)s</dc:title>
               <dc:identifier id="%(AuthorAddress)s">%(AuthorAddress)s</dc:identifier>
               <dc:language>zh-CN</dc:language>
               <dc:creator>%(AuthorName)s</dc:creator>
               <dc:description>%(Description)s</dc:description>
               <dc:rights>本电子书由ZhihuHelper制作生成，仅供个人阅读学习，严禁用于商业用途</dc:rights>
               <meta name="cover" content="cover-image" />
               </metadata>
               <!-- Content Documents -->
               <manifest>
               <item id="main-css" href="stylesheet.css" media-type="text/css"/> <!--均与OPF处同一文件夹内，所以不用写绝对路径-->
               <item id="ncx"   href="toc.ncx"      media-type="application/x-dtbncx+xml"/>
               <item id="cover" href="html/cover.html"   media-type="application/xhtml+xml"/>
               <item id="title" href="html/title.html"   media-type="application/xhtml+xml"/>'''%OPFInfoDict +   Mainfest+                '''
               <item id="cover-image" href="images/cover.jpg" media-type="image/jpg"/>
               <!-- Need to Choose Image Type -->
               </manifest>
               <spine toc="ncx" >
               <itemref idref="cover" linear="yes"/>
               <itemref idref="title" linear="yes"/>
               
               '''+Spine+'''
               </spine>
               <guide>
               <reference type="cover"  title="封面" href="html/cover.html"   />
               <reference type="toc"    title="目录" href="html/title.html" />
               </guide>
               </package>
               '''
    f.write(XML)
    f.close()
def CreateNCX(NCXInfoDict={},Ncx=''):
    f   =   open('./OEBPS/toc.ncx','w')
    XML =   '''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" 
                 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="%(AuthorAddress)s"/>
    <meta name="dtb:depth" content="-1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>%(BookTitle)s</text>
  </docTitle>'''%NCXInfoDict+Ncx+'''
</ncx>
    '''
    f.write(XML)
    f.close()
def PrintDict(Dict={}):
    for t   in Dict:
        print t,Dict[t]
ImgList =   []

def ZipToEpub(EpubName='a.epub'):
    epub    =   zipfile.ZipFile(os.path.abspath('../../'+os.curdir+u'/知乎答案集锦/'+EpubName),'w')
    epub.write('mimetype', compress_type=zipfile.ZIP_STORED)
    DictNo  =   0
    for p in os.listdir('.'):
        print   'p=',p,'EpubName=',EpubName
        if  p   ==  EpubName    or  p   ==  'mimetype':
            print   'yuanwenjian'
            continue
        if  not os.path.isfile(p):
            for f in os.listdir(p):
                if  not os.path.isfile(os.path.join(p, f)):
                        for k in os.listdir(os.path.join(p, f)):
                            DictNo+=1
                            if  DictNo%10==0:
                                PrintInOneLine(u'将文件添加至电子书内k=',os.path.join(p,f,k))#否则用户会被弹幕刷屏至死#宁可刷屏至死，也不能显得慢。。。改成10了，不谢
                            epub.write(os.path.join(p,f,k), compress_type=zipfile.ZIP_STORED)
                else:
                    PrintInOneLine(u'将文件添加至电子书内_f=',os.path.join(p, f))
                    epub.write(os.path.join(p,f), compress_type=zipfile.ZIP_STORED)
        else    :
            PrintInOneLine(u'将文件添加至电子书内_p=',p)
            epub.write(p,compress_type=zipfile.ZIP_STORED)
    epub.close()
##########################################################新开始
def ChooseTarget(url=''):#选择
    try :
        ID      =   re.search(r'(?<=zhihu\.com/people/)(?P<ID>[\w\.-]*)',url).group(0)#匹配ID
    except  AttributeError:
        pass
    else:
        print   u'成功匹配到知乎ID，ID=',ID
        return  1,ID
    try :
        Collect =   re.search(r'(?<=zhihu\.com/collection/)(?P<collect>\d*)',url).group(0)#匹配收藏
    except  AttributeError:
        pass
    else:
        print   u'成功匹配到收藏夹，收藏夹代码=',Collect
        return  2,Collect
    try :
        Roundtable= re.search(r'(?<=zhihu\.com/roundtable/)[^/]*',url).group(0)#知乎圆桌
    except  AttributeError:
        pass
    else:
        print   u'成功匹配到知乎圆桌，圆桌名=',Roundtable
        return  3,Roundtable
    try :
        Topic   =   re.search(r'(?<=zhihu\.com/topic/)[^/]*',url).group(0)#知乎话题
    except  AttributeError:
        pass
    else:
        print   u'成功匹配到话题，话题代码=',Topic
        return  4,Topic
    return  0,""

def DealAnswerDict(cursor=None,AnswerDict={},ImgList=[]):#必须是符合规定的Dict，规定附后
    for t in AnswerDict['AnswerList']:
        Dict                    =   {}
        SelectAnswerList        =   cursor.execute("select * from AnswerInfoTable where Questionhref=?",(t,)).fetchone()#SQLTag
        cursor.execute('select  AnswerContent   from    AnswerContentTable  where   Questionhref=?',(t,))
        AnswerContent           =   cursor.fetchone()[0]
        if  SelectAnswerList==None:
            AnswerDict[Dict['AnswerID']]={}
            AnswerDict[Dict['AnswerID']]['HtmlStr']     =   ''
            AnswerDict[Dict['AnswerID']]['AgreeCount']  =   0
            AnswerDict['AgreeCount']    =0
            AnswerDict['Title']         =t
            AnswerDict['HtmlStr']       ='<html><body>Wrong</body></html>'
            continue
        Dict['ID']              =   SelectAnswerList[0]
        Dict['Sign']            =   SelectAnswerList[1]
        Dict['AgreeCount']      =   SelectAnswerList[2]
        Dict['AnswerContent']   =   closeimg(AnswerContent.replace('<hr>','<hr />').replace('<br>','<br />'),ImgList)
        Dict['QuestionID']      =   SelectAnswerList[3]
        Dict['AnswerID']        =   SelectAnswerList[4]
        Dict['UpdateTime']      =   SelectAnswerList[5]
        Dict['CommitCount']     =   SelectAnswerList[6]
        Dict['QuestionTitle']   =   SelectAnswerList[7]
        Dict['Questionhref']    =   SelectAnswerList[8]
        Dict['UserName']        =   SelectAnswerList[9]
        if  len(SelectAnswerList[10])>10:#话题界面下没有用户IDLogo
            Dict['UserIDLogoAdress']=   '../images/'+SelectAnswerList[10][-15:]
            ImgList.append(SelectAnswerList[10])
        else    :
            Dict['UserIDLogoAdress']=   ''
        if  len(Dict['Sign'])==0:
            SignStr =''
        else:
            SignStr =',<strong>%(Sign)s</strong>'%Dict
        HtmlStr =u"""
        <div    class="answer-body">
            <div    class="answer-content">
                <img align="right" src="%(UserIDLogoAdress)s" alt=""/><a style="color:black;font:blod" href=http://www.zhihu.com/people/%(ID)s>%(UserName)s</a>
                """%Dict+SignStr+u"""<br /><br />
                %(AnswerContent)s    
            </div>
            <div    class='zm-item-comment-el'>
                <div  class='update' >
                    赞同：%(AgreeCount)s
                </div>
                <p  class='comment'   align   ="right">           
                    评论：%(CommitCount)s 
                </p>
            </div>
        </div>
        <div>
        <h2> </h2>
        </div>
        """%Dict
        AnswerDict[t]={}
        AnswerDict[t]['HtmlStr']     =   HtmlStr
        AnswerDict[t]['AgreeCount']  =   int(Dict['AgreeCount'])
        
        
        if  AnswerDict.has_key('AgreeCount'):
            AnswerDict['AgreeCount']    +=  int(Dict['AgreeCount'])
            if  len(AnswerDict['Title'])==0 and len(Dict['QuestionTitle'])!=0:
                AnswerDict['Title']         =   Dict['QuestionTitle'] 
        else:
            AnswerDict['AgreeCount']    =   int(Dict['AgreeCount'])
            AnswerDict['Title']         =   Dict['QuestionTitle']
    if  len(AnswerDict['Title'])!=0 and not AnswerDict.has_key('HtmlStr'):
        AnswerDict['HtmlStr']       =   u'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
            <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="provider" content="www.zhihu.com"/>
        <meta name="builder" content="ZhihuHelpv1.4"/>
        <meta name="right" content="该文档由ZhihuHelp_v1.4生成。ZhihuHelp为姚泽源为知友提供的知乎答案收集工具，仅供个人交流与学习使用。在未获得知乎原答案作者的商业授权前，不得用于任何商业用途。"/>
        <link rel="stylesheet" type="text/css" href="../stylesheet.css"/>
                    <title>%(Title)s</title>
                    </head>
                    <body>
                    <center><h3>%(Title)s</h3></center><hr/><br />\n'''%AnswerDict#生成答案头#这点内存占用量，主不在乎~哈哈#一会仿知乎日报调整下标题的大小，现在手机没电了，打不开
    if  not AnswerDict.has_key('HtmlStr'):#如果到最后也没找到问题标题的话。。。
        AnswerDict['HtmlStr']       =   u'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
                            <head>
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                        <meta name="provider" content="www.zhihu.com"/>
                        <meta name="builder" content="ZhihuHelpv1.4"/>
                        <meta name="right" content="该文档由ZhihuHelp_v1.4生成。ZhihuHelp为姚泽源为知友提供的知乎答案收集工具，仅供个人交流与学习使用。在未获得知乎原答案作者的商业授权前，不得用于任何商业用途。"/>
                        <link rel="stylesheet" type="text/css" href="../stylesheet.css"/>
                                    <title></title>
                                    </head>
                                    <body>
                                    <center><h3></h3></center><hr/><br />\n'''
    #对答案进行排序#好吧，麻烦点
    SortList    =   []
    for t   in  AnswerDict['AnswerList']:
        SortList.append((AnswerDict[t]['AgreeCount'],AnswerDict[t]['HtmlStr']))
    for t   in sorted(SortList,key=lambda  SortList:SortList[0],reverse=True):
        AnswerDict['HtmlStr']+=t[1]
    AnswerDict['HtmlStr']+='</body></html>'


def MakeInfoDict(InfoDict={},TargetFlag=0):
    Dict    =   {}
    if  TargetFlag==1:
        Dict['BookTitle']       =   InfoDict['Name']+u'的知乎回答集锦'
        Dict['AuthorAddress']   =   InfoDict['ID']
        Dict['AuthorName']      =   InfoDict['Name']
        Dict['Description']     =   InfoDict['Sign']
    if  TargetFlag==2:
        Dict['BookTitle']       =   u'知乎收藏之'+InfoDict['Title']
        Dict['AuthorAddress']   =   InfoDict['CollectionID']
        Dict['AuthorName']      =   InfoDict['AuthorName']
        Dict['Description']     =   InfoDict['Description']
    if  TargetFlag==4:
        Dict['BookTitle']       =   u'知乎话题精华之'+InfoDict['Title']
        Dict['AuthorAddress']   =   InfoDict['TopicID']
        Dict['AuthorName']      =   u'知乎'
        Dict['Description']     =   InfoDict['Description']
    return Dict   




def ZhihuHelp_Epub(MaxThread=20):
    cursor  =   returnCursor()
    FReadList   =   open('ReadList.txt','r')
    Mkdir(u"电子书制作临时资源库")
    Mkdir(u'电子书制作临时资源库/知乎图片池')
    Mkdir(u"知乎答案集锦")
    for url in  FReadList:
        ImgList     =   []#清空ImgList
        InfoDict    =   {}
        IndexList   =   []
        AnswerDict  =   {}#初始化
        print   url
        url =   url.replace("\r",'').replace("\n",'')
        TargetFlag,TargetID =   ChooseTarget(url)
        if  TargetFlag!=4 and TargetFlag!=2 and TargetFlag!=1:
            continue
        try :
            IndexList           =   pickle.loads(cursor.execute('select Pickle from VarPickle where Var= ?',(url,)).fetchone()[0])
            InfoDict            =   pickle.loads(cursor.execute('select Pickle from VarPickle where Var= ?',(url+'InfoDict',)).fetchone()[0])
        except  TypeError:
            print   u'该url未成功读取'
            continue
        InfoDict            =   MakeInfoDict(InfoDict=InfoDict,TargetFlag=TargetFlag)
        os.chdir(u'电子书制作临时资源库')
        BufDir              =   u'%(BookTitle)s(%(AuthorAddress)s)_电子书制作临时文件夹'%InfoDict
        Mkdir(BufDir)
        os.chdir(BufDir)
        f   =   open('mimetype','w')
        f.write(u'application/epub+zip')
        f.close()
        Mkdir('META-INF')
        Mkdir('OEBPS')
        os.chdir(u'./'+'OEBPS')
        Mkdir('html')
        Mkdir('images')
        os.chdir('..')
        print   u'文件目录创建完毕'
        #文件目录创建完毕
        
        #先生成目录与正文
        AnswerDict          =   {}
        for t   in IndexList:
            QuestionID                  =   int(re.search(r'(?<=http://www.zhihu.com/question/)\d*?(?=/answer/)',t).group(0))
            if  AnswerDict.has_key(QuestionID)      :
                #存在该键值
                AnswerDict[QuestionID]['AnswerList'].append(t)#记录答案链接，稍后进行进一步处理
            else    :
                AnswerDict[QuestionID]  =   {}
                AnswerDict[QuestionID]['AnswerList']    =   []
                AnswerDict[QuestionID]['AnswerList'].append(t)
        SortList    =   []
        DictNo      =   0#为了输出更好看一些
        DictCountNo =   len(AnswerDict)
        for t   in  AnswerDict:
            DictNo+=1
            PrintInOneLine(u'正在处理第{}个回答共{}个'.format(DictNo,DictCountNo))
            DealAnswerDict(cursor=cursor,ImgList=ImgList,AnswerDict=AnswerDict[t])
            SortList.append((t,AnswerDict[t]['AgreeCount']))
        #开始输出目录与文件
        print   u'答案处理完成，开始输出文件'
        TitleHtml   =   open("./OEBPS/html/title.html",'w')
        TitleHtml.write(u'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
             <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
             <head>
         <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
         <meta name="provider" content="www.zhihu.com"/>
         <meta name="builder" content="ZhihuHelpv1.4"/>
         <meta name="right" content="该文档由ZhihuHelp_v1.4生成。ZhihuHelp为姚泽源为知友提供的知乎答案收集工具，仅供个人交流与学习使用。在未获得知乎原答案作者的商业授权前，不得用于任何商业用途。"/>
         <link rel="stylesheet" type="text/css" href="stylesheet.css"/>
                     <title>目录</title>
                     </head>
                     <body>
                     <center><h1>目录</h1></center><hr/><br />\n''')
        No  =   1
        Ncx=   u'''<navMap><navPoint id="title" playOrder="1">
              <navLabel>
                <text>目录</text>
              </navLabel>
              <content src="html/title.html"/>
            </navPoint>''' 
        Mainfest=''
        Spine=''
        DictNo      =   0
        DictCountNo =   len(SortList)
        for t   in sorted(SortList,key=lambda  SortList:SortList[1],reverse=True):
            DictNo      +=   1
            PrintInOneLine(u'正在输出第{}个文件，共{}个'.format(DictNo,DictCountNo))
            No+=1
            TitleStr    =   AnswerDict[t[0]]['Title']
            Ncx     +=u'<navPoint id="chapter{No}" playOrder="{No}"> <navLabel> <text>{title}</text> </navLabel> <content src="html/chapter{No}.html"/> </navPoint> \n'.format(title=TitleStr,No=No)
            Mainfest+=u'<item id="chapter{No}" href="html/chapter{No}.html" media-type="application/xhtml+xml"   />\n'.format(No=No)
            Spine   +=u'<itemref idref="chapter{No}" linear="yes"/>\n'.format(No=No)
        
            TitleHtml.write(u"""<p><a href="chapter{No}.html">{Title}</a></p><br />\n""".format(No=No,Title=TitleStr))
            f   =   open(u'./OEBPS/html/chapter{}.html'.format(No),'w')
            f.write(AnswerDict[t[0]]['HtmlStr'])
            f.close()
        Ncx +="</navMap>"
        
        
        TitleHtml.write(u"""</body></html>\n""")
        TitleHtml.close()
        
        
        CreateOPF(InfoDict,Mainfest,Spine)
        CreateNCX(InfoDict,Ncx)
        f   =   open('./META-INF/container.xml','w')
        f.write('''<?xml version="1.0"?>
        <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
          <rootfiles>
            <rootfile full-path="OEBPS/content.opf"
             media-type="application/oebps-package+xml" />
          </rootfiles>
        </container>''')#元文件
        f.close()
        #临时创建一个封面文件
        f=  open("OEBPS/html/cover.html","w")
        coverHtmlStr    =   '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
             <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
             <head>
         <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
         <meta name="provider" content="www.zhihu.com"/>
         <meta name="builder" content="ZhihuHelpv1.4"/>
         <meta name="right" content="该文档由ZhihuHelp_v1.4生成。ZhihuHelp为姚泽源为知友提供的知乎答案收集工具，仅供个人交流与学习使用。在未获得知乎原答案作者的商业授权前，不得用于任何商业用途。"/>
         <link rel="stylesheet" type="text/css" href="stylesheet.css"/>
                     <title>%(BookTitle)s</title>
                     </head>
                     <body>
                     <center>
                     <img  class="cover" src="../images/cover.jpg"/>
                     <br />\n
        <h1>%(BookTitle)s</h1>
        <h2>%(AuthorName)s</h2></center>
        <center><a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/cn/">
        <img alt="知识共享许可协议" style="border-width:0" src="../images/88x31.png">
        </a>
        </center>
        <center>本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/cn/">知识共享署名-非商业性使用-禁止演绎 3.0 中国大陆许可协议</a>进行许可。</center>
        </body>
        </html>
        '''%InfoDict
        f.write(coverHtmlStr)
        f.close()
        print   u'答案生成完毕，输出待下载图片链接，若图片下载时间过长可自行用迅雷下载并将下载完成的图片放在文件夹：/电子书制作临时资源库/XXX_电子书制作临时文件夹/OEBPS/images内，程序检测到图片已存在即不会再去下载,减少程序运行时间'
        #输出链接，反正最多就三四万个。。。
        f   =   open(u"../%(BookTitle)s待下载图片链接.txt"%InfoDict,'w')
        ImgList =   list(set(ImgList))
        for t   in  ImgList:
            f.write(t+'\r\n')
        f.close()
        print   u'开始下载图片'
        #复制CSS与cover两个文件到临时文件夹中
        #print os.path.abspath('../../'+os.curdir+'/电子书制作资源文件夹/cover.jpg')
        f   =   open(os.path.abspath('../../'+os.curdir+u'/电子书制作资源文件夹/cover.jpg'),'rb')#真凶残啊。。。
        k   =   open(u'OEBPS/images/cover.jpg','wb')
        k.write(f.read())
        k.close()
        f.close()
        f   =   open(os.path.abspath('../../'+os.curdir+u'/电子书制作资源文件夹/88x31.png'),'rb')#真凶残啊。。。 
        k   =   open(u'OEBPS/images/88x31.png','wb')  
        k.write(f.read())                           
        k.close()              
        f.close()       
        
        
        
        f   =   open(os.path.abspath('../../'+os.curdir+u'/电子书制作资源文件夹/stylesheet.css'),'r')
        k   =   open(u'OEBPS/stylesheet.css','w')
        k.write(f.read())
        k.close()
        f.close()
        DownloadPicWithThread(ImgList,MaxThread=MaxThread)
        ZipToEpub(InfoDict['BookTitle']+'.epub')
        os.chdir('..')
        os.chdir('..')#回到元目录
        print   u'%(BookTitle)s制作完成'%InfoDict
ZhihuHelp_Epub()
