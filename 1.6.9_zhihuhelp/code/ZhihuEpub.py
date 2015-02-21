# -*- coding: utf-8 -*-
import  zipfile#将文件夹压缩为Epub(zip)格式
import  shutil#删除目录
######Tool######
from    MarkDownCssStyle    import  returnMarkDownCssStyle
from    ZhihuLib import *

def CheckImgFileExist(CheckList=[],ErrorList=[]):#PassTag
    u"""
        *   功能
            *   检测CheckList中的文件是否存在，将不存在的文件添加到ErrorList中
        *   输入
            *   CheckList
            *   ErrorList
        *   返回
            *   无
     """
    for url in  CheckList:
        MetaName    =   u'../知乎图片池/'   +   PixName(url)
        if  not os.path.isfile(MetaName):
            ErrorList.append(url)

def DownloadPicWithThread(ImgList=[],MaxThread=20):#添加图片池功能#当图片下载完成时在ImgList中删除之#newCommitTag
    u"""
        *   功能
            *   下载ImgList中的所有图片
            *   若图片下载失败，将图片地址打印并输出至『未成功打开的网页.txt』中
        *   输入
            *   ImgList
                *   待下载图片列表
            *   MaxThread
                *   最大线程数
                    *   即最大并发下载数
        *   返回
            *   无
     """
    Time=0
    MaxPage     =   len(ImgList)
    ErrorList   =   []
    while   Time<10 and MaxPage>0:
        Buf_ImgList =   []
        Time+=1
        ThreadList  =   []
        buf_t_PageRecord    =   0
        for t in  ImgList:#因为已下载过的文件不会重新下载，所以直接重复执行十遍，不必检测错误#待下载的文件可能会突破万这一量计，所以还是需要一些优化
            buf_t_PageRecord    +=  1
            ThreadList.append(threading.Thread(target=DownloadImg,args=(t,Buf_ImgList,u"({}/{})".format(buf_t_PageRecord,MaxPage))))
        Page    =   0
        while Page <  MaxPage:
            t   =   MaxThread - (threading.activeCount() - 1)
            if  t   >   0 :
                while  t   >   0  and Page < MaxPage :
                    ThreadList[Page].start()
                    Page += 1
                    t    -= 1
                time.sleep(0.1)
            else    :
                PrintInOneLine(u'第({}/10)轮下载图片，还有{}张图片等待下载'.format(Time,MaxPage-Page))
                time.sleep(1)
        ThreadLiveDetect(ThreadList)
        
        ImgList     =       list(set(ImgList)-set(Buf_ImgList))#剔除不能下载的图片链接地址
        ErrorList   +=      Buf_ImgList#将下载失败的图片列表储存起来,一并输出
        Buf_ImgList =       []  
        CheckImgFileExist(CheckList=ImgList,ErrorList=Buf_ImgList)
        ImgList     =       Buf_ImgList

        MaxPage     =       len(ImgList)
        if  MaxPage !=0:
            print   u'第{}轮下载执行完毕，剩余{}张图片待下载，若下载失败的图片过多可以调用迅雷进行下载，待下载图片列表为『程序所在文件夹\电子书制作临时资源库\待下载图片列表.txt』，将迅雷下载下来的图片放置于『程序所在文件夹\电子书制作临时资源库\知乎图片池』中即可'.format(Time,MaxPage)
            time.sleep(1)#休息一秒后继续
        else    :
            print   u'\n所有图片下载完毕'
    ErrorList   =   list(set(ErrorList))
    if  len(ErrorList)>0:
        print   u'开始输出下载失败的图片列表'
        f   =   open(u'../下载失败的图片列表.txt','a')#输出下载失败列表
        f.write(u'\n-------------------------------------------\n')
        f.write(u'时间戳:\t'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')  
        f.write(u'-------------------------------------------\n')
        print   u'以下文件下载失败'
        for t   in  ErrorList:
            f.write(t+'\n')
            print   t
        f.close()
def returnCursor():#PassTag
    u"""
        *   功能
            *   返回数据库游标
            *   因为不准备在Epub模块中对数据库进行写操作，所以不提供conn
        *   输入
            *   无
        *   返回
            *   数据库游标
            *   若数据库不存在，打印错误信息并返回None
     """
    if  os.path.isfile('./ZhihuDateBase.db'):
        conn    =   sqlite3.connect("./ZhihuDateBase.db")
        conn.text_factory = str
        cursor  =   conn.cursor()
        return  cursor
    else:
        ErrorReturn(u'抱歉，没有找到数据库，请先运行知乎助手')
        return  None

def CreateMimeType():#PassTag
    u"""
        *   功能
            *   创建mimetype文件
        *   输入
            *   无
        *   返回
            *   无
     """
    f   =   open('mimetype','w')
    f.write('application/epub+zip')
    f.close()
def CreateContainer_XML():#PassTag
    u"""
        *   功能
            *   创建container.xml文件
        *   输入
            *   无
        *   返回
            *   无
     """
    f   =   open('META-INF/container.xml','w')      
    f.write('''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf"
     media-type="application/oebps-package+xml" />
  </rootfiles>
</container>''')
    f.close()

def closeimg(text='',ImgList=[],PicDownload=1):#PassTag#若有大图直接下载之#为图片添加点击框
    u"""
        *   功能
            *   图片处理主函数
            *   负责提取出答案内容中的所有图片，并将下载地址传入ImgList中
            *   同时，将图片链接替换为内部链接
        *   输入
            *   text
                *   待处理答案内容
            *   ImgList
                *   图片链接存放列表
        *   输出
            *   无
     """
    if  not PicDownload:
        text    =   removeTag(text=text,tagname=["img"])
    elif    PicDownload==1:
        for t   in  re.findall(r'<img.*?>',text):
            text    =   text.replace(t,fixPic(removeAttibute(t,['data-rawwidth','data-original']).replace("data-rawheight",'height')[:-1]+u'  alt="知乎图片"/>',ImgList))#使用小图
    else:
        for t   in  re.findall(r'<img.*?>',text):#有可能没有data-original属性
            try :
                t.index('data-original')
            except  ValueError:
                text    =   text.replace(t,fixPic(removeAttibute(t,['data-rawwidth','data-original']).replace("data-rawheight",'height')[:-1]+u'  alt="知乎图片"/>',ImgList))
            else:
                text    =   text.replace(t,fixPic(removeAttibute(t,['data-rawwidth','src'])\
                                .replace('data-original','src').replace("data-rawheight",'height')[:-1]\
                                +u'  alt="知乎图片"/>',ImgList))#将data-original替换为src即为原图
    return text
def PixName(t):#PassTag
    return  re.search(r'[^/"]*?\.jpg',t).group(0)
def fixPic(t='',ImgList=[]):#PassTag#添加多看扩展
    for k   in  re.findall(r'(?<=src=")http://[/\w\.^"]*?zhimg.com[/\w^"]*?.jpg',t):
        t   =   t.replace(k,'../images/'+PixName(k))
        ImgList.append(k)
    return  '<div class="duokan-image-single">'+t+'</div>'
def DownloadImg(imghref='',ErrorList=[],successprint=""):#下载失败时应报错或重试#文件已成功下载时也添加到ErrorList中#newCommitTag
    u"""
        *   功能
            *   下载图片，将下载失败的图片存入ErrorList中
            *   会先检测图片池中有没有对应的图片
                *   若有，直接将图片池内图片复制至目标文件夹中
                *   若无
                    *   下载图片至图片池中
                    *   将图片复制到目标文件夹内
        *   输入
            *   imghref
                *   图片网址
            *   ErrorList
                *   下载失败时将链接存入此处
        *   返回
            *   无
    """
    try :
        CheckName   =   u'../知乎图片池/'
        try :
            MetaName    =     PixName(imghref)
        except  AttributeError:#需要编写测试用例
            raise       ValueError(u'程序出现错误，未能成功提取出图片下载地址'+u'目标网址'+imghref)
        imgfilename =   './OEBPS/images/'+MetaName   
        if  not os.path.isfile(CheckName+MetaName):
            k   =   OpenUrl(urllib2.Request(imghref),Timeout=10)#这里会返回IOError
            if  len(k)==0:
                print   u'Download image '+MetaName+' error ,will try again soon'
                return 0
            imgfile     =   open(CheckName+MetaName,"wb")
            imgfile.write(k)
            imgfile.close()
        if  not os.path.isfile(imgfilename):
            imgfile     =   open(imgfilename,"wb")
            imgpoolfile =   open(CheckName+MetaName,"rb")
            imgfile.write(imgpoolfile.read())
            imgfile.close()
            imgpoolfile.close()
    except  ValueError  as  e   :
        print   e
        ErrorList.append(imghref)
        PrintInOneLine( u'图片{}下载失败\r'.format(MetaName))
        ErrorReportText(u'图片下载错误\t:\t'+str(e))
    except  IOError     as  e   :
        print   e
        ErrorList.append(imghref)
        PrintInOneLine( u'图片{}下载失败\r'.format(MetaName))
        ErrorReportText(u'图片下载错误\t:\t'+str(e))
    else    :
        PrintInOneLine( u'图片{}下载成功\r'.format(MetaName)+successprint)
    return 0
def CreateOPF(OPFInfoDict={},Mainfest='',Spine=''):#生成文件函数均假定当前目录为电子书根目录#PassTag
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
               <dc:publisher>知乎</dc:publisher>
               <meta name="cover" content="cover-image" />
               </metadata>
               <!-- Content Documents -->
               <manifest>
               <item id="main-css" href="stylesheet.css" media-type="text/css"/> <!--均与OPF处同一文件夹内，所以不用写绝对路径-->
               <item id="ncx"   href="toc.ncx"      media-type="application/x-dtbncx+xml"/>
               <item id="cover" href="html/cover.html"   media-type="application/xhtml+xml"/>
               <item id="title" href="html/title.html"   media-type="application/xhtml+xml"/>'''%OPFInfoDict +   Mainfest+                '''
               <item id="cover-image" href="images/BookCover.png" media-type="image/png"/>
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
def CreateNCX(NCXInfoDict={},Ncx=''):#PassTag
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

def ZipToEpub(EpubName = 'a.epub'):#newCommitTag
    u"""
        *   功能
            *   将目标文件夹压缩成epub(zip)文件
        *   输入
            *   EpubName
                *   目标文件名
        *   返回
            *   无

    """
    epub    =   zipfile.ZipFile(os.path.abspath('../../'+os.curdir+u'/知乎答案集锦/'+EpubName),'w')
    epub.write('mimetype', compress_type=zipfile.ZIP_STORED)
    def Help_ZipToEpub(Dir='.'):
        for p   in  os.listdir(Dir):
            if  p   ==  EpubName    or  p   ==  'mimetype':
                PrintInOneLine(u'该文件已添加，自动跳过')
                continue
            filepath    =   os.path.join(Dir,p)
            if  not os.path.isfile(filepath):
                if  p   ==  '.' or  p   ==  '..':
                    continue
                Help_ZipToEpub(Dir=filepath)
            else:
                PrintInOneLine(   u'将{}添加至电子书内'.format(filepath))
                epub.write(filepath, compress_type=zipfile.ZIP_STORED)
    Help_ZipToEpub()
    epub.close()
##########################################################新开始
def DealAnswerDict(cursor=None,AnswerDict={},ImgList=[],PicDownload=1):#必须是符合规定的Dict，规定附后
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
        Dict['AnswerContent']   =   closeimg(AnswerContent.replace('<hr>','<hr />').replace('<br>','<br />'),ImgList,PicDownload)
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
                <img align="right" src="%(UserIDLogoAdress)s" alt=""/><a style="color:black;font:blod" href="http://www.zhihu.com/people/%(ID)s">%(UserName)s</a>
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
        <meta name="builder" content="ZhihuHelpv1.6"/>
        <meta name="right" content="该文档由ZhihuHelp_v1.6生成。ZhihuHelp为姚泽源为知友提供的知乎答案收集工具，仅供个人交流与学习使用。在未获得知乎原答案作者的商业授权前，不得用于任何商业用途。"/>
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
                        <meta name="builder" content="ZhihuHelpv1.6"/>
                        <meta name="right" content="该文档由ZhihuHelp_v1.6生成。ZhihuHelp为姚泽源为知友提供的知乎答案收集工具，仅供个人交流与学习使用。在未获得知乎原答案作者的商业授权前，不得用于任何商业用途。"/>
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
    Dict    =   {}#稳定的修复应该是对所有项均做closeimg处理，但只对描述做了两处修改，应该啥事吧~
    if  TargetFlag==1:
        Dict['BookTitle']       =   InfoDict['Name']+u'的知乎回答集锦'
        Dict['AuthorAddress']   =   InfoDict['ID']
        Dict['AuthorName']      =   InfoDict['Name']
        Dict['Description']     =   InfoDict['Name']+u'的知乎回答集锦'
    if  TargetFlag==2:
        Dict['BookTitle']       =   u'知乎收藏之'+InfoDict['Title']
        Dict['AuthorAddress']   =   InfoDict['CollectionID']
        Dict['AuthorName']      =   InfoDict['AuthorName']
        Dict['Description']     =   closeimg(InfoDict['Description'].replace('<hr>','<hr />').replace('<br>','<br />'),[],1)
    if  TargetFlag==4:
        Dict['BookTitle']       =   u'知乎话题精华之'+InfoDict['Title']
        Dict['AuthorAddress']   =   InfoDict['TopicID']
        Dict['AuthorName']      =   u'知乎'
        Dict['Description']     =   closeimg(InfoDict['Description'].replace('<hr>','<hr />').replace('<br>','<br />'),[],1)
    for r   in  '< > / \ | : " * ?'.split(' '):#去除非法字符
        Dict['BookTitle']   =   Dict['BookTitle'].replace(r,'')
    return Dict   


def EpubBuilder(MaxThread=20,FReadList=[],PicDownload=1):
    cursor  =   returnCursor()
    #FReadList   =   open('ReadList.txt','r')
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
        shutil.rmtree(BufDir,True)#移除之前的缓存目录
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
            PrintInOneLine(u'正在处理第{}个提问共{}个'.format(DictNo,DictCountNo))
            DealAnswerDict(cursor=cursor,ImgList=ImgList,AnswerDict=AnswerDict[t],PicDownload=PicDownload)
            SortList.append((t,AnswerDict[t]['AgreeCount']))
        #开始输出目录与文件
        print   u'\n答案处理完成，开始输出文件'
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
                     <center><h1>目录</h1></center><hr/><br />\n<ol>''')
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
            TitleHtml.write(u"""<li><a style="text-decoration:none" href="chapter{No}.html">{Title}</a></li>\n""".format(No=No,Title=TitleStr))#添加了一条隐藏下划线的设定
            f   =   open(u'./OEBPS/html/chapter{}.html'.format(No),'wb')#直接作为数据流写入试试，直接写入数据刘应该不会再出现编码错误了，实在不行就换codec模块
            f.write(AnswerDict[t[0]]['HtmlStr'])
            f.close()
        Ncx +="</navMap>"
        
        TitleHtml.write(u"""</ol></body></html>\n""")
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
           
        if(InfoDict['Description']==''):
            Description =''+"</center>"
        else:
            Description ='''<br />                   
            <h4>%(Description)s</h4></center>'''%InfoDict
        coverHtmlStr    =   '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
             <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
             <head>
         <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
         <meta name="provider" content="www.zhihu.com"/>
         <meta name="builder" content="ZhihuHelpv1.4"/>
         <meta name="right" content="该文档由ZhihuHelp_v1.6.2生成。ZhihuHelp为姚泽源为知友提供的知乎答案收集工具，仅供个人交流与学习使用。在未获得知乎原答案作者的商业授权前，不得用于任何商业用途。"/>
         <link rel="stylesheet" type="text/css" href="stylesheet.css"/>
         <title>%(BookTitle)s</title>
         </head>
         <body>
         <center>
         <img  class="cover" src="../images/cover.png"/>
         <br />
      
        <h1>%(BookTitle)s</h1>
        <br />
        <h4>%(AuthorName)s</h4>'''%InfoDict+Description+'''
        <center><a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/cn/">
        <img alt="知识共享许可协议" style="border-width:0" src="../images/88x31.png" />
        </a>
        </center>
        <center>本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/cn/">知识共享署名-非商业性使用-禁止演绎 3.0 中国大陆许可协议</a>进行许可。</center>
        </body>
        </html>
        '''%InfoDict
        f.write(coverHtmlStr)
        f.close()
        print   u'\n答案生成完毕'
        #输出链接，反正最多就三四万个。。。
        print   u'开始下载图片'
        #复制CSS与cover两个文件到临时文件夹中
        
        for root,target,flag in  [
                    (os.path.abspath('../../'+os.curdir+u'/电子书制作资源文件夹/BookCover.png') ,u'OEBPS/images/BookCover.png'  ,False)
                ,   (os.path.abspath('../../'+os.curdir+u'/电子书制作资源文件夹/cover.png')     ,u'OEBPS/images/cover.png'      ,False)
                ,   (os.path.abspath('../../'+os.curdir+u'/电子书制作资源文件夹/88x31.png')     ,u'OEBPS/images/88x31.png'      ,False)
                ,   (os.path.abspath('../../'+os.curdir+u'/电子书制作资源文件夹/stylesheet.css'),u'OEBPS/stylesheet.css'        ,True)]:
            CopyFile(root=root,TargetFile=target,flag=flag)
        
        DownloadPicWithThread(ImgList,MaxThread=MaxThread)
        ZipToEpub(EpubName = InfoDict['BookTitle']+'.epub')
        os.chdir('..')
        os.chdir('..')#回到元目录
        EpubToHtml(u'%(BookTitle)s(%(AuthorAddress)s)'%InfoDict)
        PrintInOneLine('')
        PrintInOneLine( u'\n%(BookTitle)s制作完成\n'%InfoDict+'\n')
