# -*- coding: utf-8 -*-
import  json
from    ZhihuEpub   import  CheckImgFileExist, DownloadPicWithThread , returnCursor ,  CreateMimeType , CreateContainer_XML , returnTagContent , removeTag , removeAttibute , closeimg , PixName , fixPic , DownloadImg , CreateOPF , CreateNCX ,  ZipToEpub #复用。。。
from    ZhihuLib    import  CheckUpdate,PrintDict ,Mkdir ,PrintInOneLine,CopyFile,OpenUrl,ErrorReportText,setMaxThread,ErrorReturn,EpubToHtml
import  sys
reload( sys )
sys.setdefaultencoding('utf-8')
###############头文件

import  re
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
#数据库部分
import  pickle
import  socket#捕获Timeout错误
import  shutil#删除文件夹
###########################################################


####################
def ChooseTarget(url=''):#选择
    try :
        return  re.search(r'(?<=zhuanlan.zhihu.com/)[^/#\n\r]*',url).group(0)
    except  AttributeError:
        print   u'未能匹配到专栏名'
        return  ''
######新修改
def DealAnswerDict(JsonDict=[],ImgList=[],JsonDictList=[]):#必须是符合规定的Dict，规定附后
    for k in JsonDict:
        t                    =   k
        Dict={}
        Dict['ColumnID']     =   t["column"]["slug"]#专栏ID
        Dict['ColumnName']   =   t["column"]["name"]#专栏名
        Dict['ArticleLink']  =   t['links']['comments']
        Dict['TitleImage']   =   t["titleImage"]
        Dict['ArticleTitle'] =   t["title"]
        Dict['AuthorName']   =   t['author']['name']
        Dict['AuthorIDLink'] =   t['author']['profileUrl']#全地址
        Dict['PublishedTime']=   t["publishedTime"]
        Dict['Commit']       =   t["commentsCount"]
        Dict['Agree']        =   t["likesCount"]
        Dict['Content']      =   t["content"]
        Buf_AuthorID         =   t['author']['avatar']['id']
        Buf_AuthorTemplete   =   t['author']['avatar']['template']
        Dict['AuthorIDLogo'] =   Buf_AuthorTemplete.format(id=Buf_AuthorID,size='s')     
        
        HtmlStr =u"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
            <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="provider" content="www.zhihu.com"/>
        <meta name="builder" content="ZhihuHelpv1.4"/>
        <meta name="right" content="该文档由ZhihuHelp_v1.4生成。ZhihuHelp为姚泽源为知友提供的知乎答案收集工具，仅供个人交流与学习使用。在未获得知乎原答案作者的商业授权前，不得用于任何商业用途。"/>
        <link rel="stylesheet" type="text/css" href="../stylesheet.css"/>
        <title>%(ArticleTitle)s</title>
        </head>
        <body>
        <div    align="center"   class="TitleImage">
        <img    src="%(TitleImage)s"    alt=""/>
        </div>
        <div    align="center"   class="Title">
        <h3 align="left">%(ArticleTitle)s</h3>
        </div>
        <div    class="answer-body">
            <div    class="answer-content">
                <img align="right" src="%(AuthorIDLogo)s" alt=""/><a style="color:black;font:blod" href="%(AuthorIDLink)s">%(AuthorName)s</a>
            <br /><br />
                %(Content)s    
            </div>
            <div    class='zm-item-comment-el'>
                <div  class='update' >
                    赞同：%(Agree)s
                </div>
                <p  class='comment'   align   ="right">           
                    评论：%(Commit)s 
                </p>
            </div>
        </div>
        <div>
        <h2> </h2>
        </div>
        </body></html>
        """%Dict
        Dict['HtmlStr'] =   closeimg(text=HtmlStr.replace('<hr>','<hr />').replace('<br>','<br />'),ImgList=ImgList,PicDownload=1).replace('alt=""/', '')#需要进一步处理#testTag
        JsonDictList.append(Dict)#按发布顺序排序

def MakeInfoDict(ColumnInfoDict={}):
    Dict    =   {}
    Dict['BookTitle']       =   u'知乎专栏之'+ColumnInfoDict['Name']
    Dict['AuthorAddress']   =   ColumnInfoDict['Href']
    Dict['AuthorName']      =   ColumnInfoDict['Name']
    Dict['Description']     =   ColumnInfoDict['Description']
    for r   in  '< > / \ | : " * ?'.split(' '):#去除非法字符
        Dict['BookTitle']   =   Dict['BookTitle'].replace(r,'')
    return Dict   

def OpenUrl_Zhuanlan(url=""):
    Time    =   0
    Content =   ''   
    while   Time<10:
        Content =   OpenUrl(urllib2.Request(url=url),Timeout=30)#捕捉IOError错误的任务放在外层，以便及时跳出循环
        if  Content ==  '':
            Time+=1
            time.sleep(1)#休息一秒后再尝试打开
            print   u'第({}/10)次尝试打开页面'.format(Time)
        else    :
            return Content
    print   u'10次尝试全部失败，目标网址={} ，请检查网络链接或网址是否正确'.format(url)
    return  Content

def ZhihuHelp_Epub(Hook={},MaxThread=20):
    ErrorReportText(flag=False)
    FReadList   =   open('ReadList.txt','r')
    Mkdir(u"电子书制作临时资源库")
    Mkdir(u'电子书制作临时资源库/知乎图片池')
    Mkdir(u"知乎答案集锦")
    ErrorUrlList    =   []
    for url in  FReadList:
        Hook[0] =   url
        ImgList     =   []#清空ImgList
        InfoDict    =   {}
        JsonDict    =   []#初始化
        print   u'待抓取链接:',url
        url =   url.replace("\r",'').replace("\n",'')
        Target      =   ChooseTarget(url)
        if  Target!='':
            TargetUrl   =   'http://zhuanlan.zhihu.com/api/columns/'+Target+'/posts?limit=100&offset=0'
            InfoTargetUrl   =   'http://zhuanlan.zhihu.com/api/columns/'+Target
        else:
            continue
        #专栏信息
        print   u'开始获取专栏信息'
        try:
            t           =   OpenUrl_Zhuanlan(url=InfoTargetUrl)
            if  t=='':
                print   u'获取专栏信息失败'
                ErrorReportText(u'获取专栏信息失败'+InfoTargetUrl)
                continue
        except  IOError as  e:
            print   u'解析专栏内容时出错'
            ErrorReportText(u'解析专栏内容时出错'+str(e))
            continue
        except  ValueError  as e:
            print   u'专栏不存在或知乎服务器拒绝访问'
            ErrorReportText(u'专栏不存在或知乎服务器拒绝访问'+str(e))
            continue

        InfoDict    =   json.loads(t)
        ColumnInfoDict  =   {}
        ColumnInfoDict["FollowersCount"]    =   InfoDict["followersCount"]
        ColumnInfoDict["Description"]       =   InfoDict["description"]
        ColumnInfoDict["Name"]              =   InfoDict["name"]
        ColumnInfoDict["Href"]              =   Target
        InfoDict    =   MakeInfoDict(ColumnInfoDict)
        
        #专栏全文
        print   u'开始获取专栏内容'
        try:
            t           =   OpenUrl_Zhuanlan(url=TargetUrl)#在专栏内容过多时会失效（有效下载时间只有3s左右，200k网速下只能下载300篇文章）
            if  t=="":
                print   u'专栏内容没有抓到'+InfoTargetUrl
                ErrorReportText(u'错误原因:专栏内容没有抓到'+InfoTargetUrl)
                continue
        except  IOError as  e:
            print   u'解析专栏内容时出错'
            ErrorReportText(u'解析专栏内容时出错'+str(e))
            continue
        except  ValueError  as e:
            print   u'专栏不存在或知乎服务器拒绝访问'
            ErrorReportText(u'专栏不存在或知乎服务器拒绝访问'+str(e))
            continue

        JsonDict    =   json.loads(t)
        JsonDictList=   []
        DealAnswerDict(JsonDict=JsonDict,ImgList=ImgList,JsonDictList=JsonDictList)       
       
       
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
        DictCountNo =   len(JsonDictList)
        for t   in  JsonDictList:
            DictNo      +=   1
            if  DictNo%10==0:
                print   u'正在输出第{}个文件，共{}个'.format(DictNo,DictCountNo)
            No+=1
            TitleStr    =   t['ArticleTitle']
            Ncx     +=u'<navPoint id="chapter{No}" playOrder="{No}"> <navLabel> <text>{title}</text> </navLabel> <content src="html/chapter{No}.html"/> </navPoint> \n'.format(title=TitleStr,No=No)
            Mainfest+=u'<item id="chapter{No}" href="html/chapter{No}.html" media-type="application/xhtml+xml"   />\n'.format(No=No)
            Spine   +=u'<itemref idref="chapter{No}" linear="yes"/>\n'.format(No=No)
        
            TitleHtml.write(u"""<li><a style="text-decoration:none" href="chapter{No}.html">{Title}</a></li>\n""".format(No=No,Title=TitleStr))
            f   =   open(u'./OEBPS/html/chapter{}.html'.format(No),'wb')
            f.write(t['HtmlStr'])
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
            Description =''
        else:
            Description ='''<br />                   
            <h4>%(Description)s</h4></center>'''%InfoDict
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
                     <img  class="cover" src="../images/cover.png"/>
                     <br />\n
        <h1>%(BookTitle)s</h1>
        <br />
        <h4>%(AuthorName)s</h4>'''%InfoDict+Description+'''
        <center><a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/cn/">
        <img alt="知识共享许可协议" style="border-width:0" src="../images/88x31.png"/>
        </a>
        </center>
        <center>本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/cn/">知识共享署名-非商业性使用-禁止演绎 3.0 中国大陆许可协议</a>进行许可。</center>
        </body>
        </html>
        '''%InfoDict
        f.write(coverHtmlStr)
        f.close()
        print   u'文集生成完毕'
        #输出链接，反正最多就三四万个。。。
        ImgList =   list(set(ImgList))
        #复制CSS与cover两个文件到临时文件夹中
        #print os.path.abspath('../../'+os.curdir+'/电子书制作资源文件夹/cover.jpg')
        for root,target,flag in  [

                    (os.path.abspath('../../'+os.curdir+u'/电子书制作资源文件夹/BookCover.png') ,u'OEBPS/images/BookCover.png'  ,False)
                ,   (os.path.abspath('../../'+os.curdir+u'/电子书制作资源文件夹/cover.png')     ,u'OEBPS/images/cover.png'  ,False)
                ,   (os.path.abspath('../../'+os.curdir+u'/电子书制作资源文件夹/88x31.png')     ,u'OEBPS/images/88x31.png'  ,False)
                ,   (os.path.abspath('../../'+os.curdir+u'/电子书制作资源文件夹/stylesheet.css'),u'OEBPS/stylesheet.css'    ,True)]:
            CopyFile(root=root,TargetFile=target,flag=flag)
        print   u'开始下载图片'
        DownloadPicWithThread(ImgList,MaxThread=MaxThread)
        ZipToEpub(InfoDict['BookTitle']+'.epub')
        os.chdir('..')
        os.chdir('..')#回到元目录
        
        EpubToHtml(u'%(BookTitle)s(%(AuthorAddress)s)'%InfoDict)
        PrintInOneLine('\n'+u'%(BookTitle)s制作完成'%InfoDict+'\n')
    print   u'恭喜，所有电子书制作完成\n未成功打开的页面已输出至『未成功打开的页面.txt』中\n点按回车退出'
    raw_input()

Hook={}
if  __name__ == '__main__' :
    try:
        pass
        CheckUpdate()
        print   u'请设置下载图片时的最大线程数\n线程越多速度越快，但线程过多会导致知乎服务器故障导致图片下载失败，默认最大线程数为20\n请输入一个数字（1~50），回车确认'
        MaxThread   =   setMaxThread()
        ZhihuHelp_Epub(Hook=Hook,MaxThread=MaxThread)
    except  (KeyboardInterrupt, SystemExit):
        pass#正常退出
    except  Exception , e:
        print   u'程序异常退出，快上知乎上@姚泽源反馈下bug\n或者把bug和『错误信息_未能成功打开的页面.txt』一块发给yaozeyuan93@gmail.com也行，谢谢啦~\n错误信息如下:\n'
        print   e
        print   "\n-----------------------\n"
        import traceback
        f   =   open("ErrorReport.txt","ab+")#应该使用错误报告文件，不应该动ReadList
        f.write(u"\n#-----------------------\n"+u"发生时间:\n"+time.strftime("%Y-%m-%d  %H:%M:%S",time.gmtime()))
        f.write(u"\n*    "+u"专栏助手异常网址:\n"+str(Hook))
        f.write(u"\n*    "+u"专栏助手异常信息:\n"+str(e))
        f.write(u"\n*    "+u"专栏助手异常栈:\n")
        traceback.print_tb(sys.exc_traceback)
        traceback.print_tb(sys.exc_traceback,file=f)
        f.write(u"\nover"+u"\n-----------------------\n")
        f.close()
        print   u'错误信息显示完毕，已记录至『错误信息_未能成功打开的页面.txt』文件中\n点按回车退出'
        raw_input()
else:
    print   "Zhuanlan Mode"
    #ZhihuHelp(Hook=Hook)
