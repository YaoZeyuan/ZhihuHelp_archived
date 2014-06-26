import  ZhihuHelp
#ZhihuHelp部分
###################ZhihuHelp############################
def PrintDict(Dict={}):
#   函数说明
    *   调试用函数，用于将字典按键值顺序树型输出
    *   键值与字典内容均会被编码为utf-8
#   改进方向
    *   使用复杂字典对函数进行测试
def FetchMaxAnswerPageNum(Content=""):
#   函数说明
    *   输入知乎答案网页内容
    *   匹配答案最大页码数
    *   返回一个最大页码数，当答案页数为0时或没有匹配到页码数时返回1
#   改进方向
    *   无
def OpenUrl(Request):#打开网页,只尝试一次，失败时返回空字符串，错误信息中包含未打开网址。话说字符串分割对空列表还有效否？
#   函数说明
    *   输入一个Request，由urllib2.Request生成，打开这个网页并返回字符串格式的网页内容
    *   网页超时时间：5s
    *   异常处理
        *   服务器返回网页内容时    
            *   当网页报40X错误时，报IOError
            *   IOError内容：
            *   u"404 Not Found"+u"错误页面\t：\t"+Request.get_full_url()
            *   当网页报50X错误时，打印u"知乎正在紧张的撰写答案,服务器繁忙ing，稍后重试"
            *   其他网页错误：打印u'打开网页时出现未知错误'
            *   当网页为gzip格式时
                *   解压缩之
                *   当解压缩失败时
                *   打印u'解压缩出错'，u'错误信息：'，错误信息
                *   抛出 IOError(u"解压缩错误"+u"错误页面\t：\t"+Request.get_full_url())
        *   urllib2.URLError 
            *   打印错误网址u'错误网址：'+Request.get_full_url() 
            *   与          u'打开网页异常#稍后重试'
        *   socket.timeout 
            *   打印错误消息内容与u"打开网页超时"
#   改进方向
    *   已成熟，无
def ThreadLiveDetect(ThreadList=[]):
#函数说明
    *   工具类函数
    *   当所有线程均已结束时返回
#改进方向
    *   无
def ThreadWorker(cursor=None,ErrorTextDict={},MaxThread=200,RequestDict={},Flag=1)
#   函数说明
    *   输入
        *   输入数据库链接，错误信息字典，最大线程数，待处理Request字典，标志
        *   错误信息字典用于收集打开网页时所报的错误信息
        *   标志用于区分话题与其他，在将网页分割为答案列表时，话题的答案分割标志符为'<div class="content"'，其余为'<div class="zm-item"'
    *   工作内容
        *   针对RequestDict中的每一个Request生成线程，将Request交付与WorkForFetchUrl，针对打开网页失败的网页重复执行10遍，执行完毕后读取答案内容，读取完毕后存入数据库中
        *   为主要函数
#   改进方向
    *   待全部软件说明编写完成后优化程序结构，让代码更为易懂些
def SaveCollectionIndexIntoDB(RequestDict={},CollectionID=0,cursor=None):
#   函数说明
    *   更新收藏夹列表，将新加入收藏夹的链接存入数据库中
#   改进方向
    *   无
def AppendDictIntoDataBase(cursor=None,Dict={}) 
#   函数说明
    *   将答案数据存入数据库中
#   改进方向
    *   无
def CheckUpdate():
#   函数说明
    *   检查更新
#   改进方向
    *   增加显示更新说明模块
def ChooseTarget(url=''):#选择
#   函数说明
    *   输入目标链接
    *   返回类别与代号
        *   ID      ：代号1   返回    1，ID
        *   Collect ：代号2   返回    2，CollectID
        *   Topic   ：代号4   返回    4，TopicID
        *   没有匹配到任何数据：    代号0，返回 0，''
#   改进方向
    *   为之添加单元测试
def WriteHtmlFile(cursor=None,IndexList=[],InfoDict={},TargetFlag=0):
#   函数说明
    *   将IndexList中的链接输出为Html文件
    *   已废弃
#   改进方向
    *   1.  可以取消
        2.  增加更多选项，比如按答案长度排序、按评论数排序、按指定公式排序（例如赞/评论）
        4.  为答案添加ID
        5.  添加目录
def returnHtml_FrontPage(cursor=None,Flag=0,InfoDict={}):#兼职把Info存到数据库里
#   函数说明
    *   返回待生成网页的首页内容
    *   已废弃
#   改进方向
    *   增加个人信息、内容介绍
    *   将css
    *   修正当网页过大时网页面积爆炸的CSS_bug
def returnReDict():#返回编译好的正则字典
#   函数说明
    *   返回编译好的正则字典，便于分析答案内容
#   改进方向
    *   添加单元测试
def ErrorReturn(ErrorInfo=""):#返回错误信息并退出，错误信息要用unicode编码
#   函数说明
    *   返回错误信息并返回
    *   工具类函数
#   改进方向
    *   调整函数位置，让程序更易读
def ReadAnswer(ReDict,html_parser,LastDict,text="",Flag=1):
#   函数说明
    *   读取答案内容
    *   返回一个答案字典
    *   当检测到禁止转载标记时停止读取直接返回
    *   提取信息顺序
    *   Dict["AgreeCount"]          #int
    *   Dict["QuestionID"]          
    *   Dict["AnswerID"]            
    *   Dict["Questionhref"]        
    *   Dict["AnswerContent"]       
    *   Dict['UserIDLogoAdress']    
    *   Dict["UpdateTime"]          
    *   Dict["CommitCount"]         #int
    *   Dict["QuestionTitle"]       
    *   Dict["ID"]                  
    *   Dict["Sign"]                
    *   Dict["UserName"]            
#   改进方向
    *   添加单元测试
    *   增加图片清晰度，直接将图片变为原图大小是否可行？#修改完这一轮再改
def WorkForFetchUrl(ErrorTextDict={},ReDict={},html_parser=None,RequestDict={},Page=0,AnswerDictList=[],Flag=1):#抓取回答链接#注意，Page是字符串
#   函数说明
    *   主要的工作函数
    *   打开网页，将网页切分后交由ReadAnswer处理，成功或网页40x错误后将RequestDict[Page][1]标为True，将答案链接存于AnswerList中，再内置于RequestDict[Page][0]内，答案字典（包含了答案内容）存储于『全局变量』AnswerDictList里
    *   其他情况直接返回，错误信息储存于ErrorTextDict[Page]中
#   改进方向
    *   可否取消ErrorTextDict？
def Login(cursor=None,UserID='mengqingxue2014@qq.com',UserPassword='131724qingxue'):
#   函数说明
    *   登陆函数，负责返回一个可用的cookie
    *   在
        1.  知乎首页打不开
        2.  登陆请求发送失败
        3.  连续三次登陆失败
        时，直接调用OldPostHeader()
    *   正常登陆则将cookie存入数据库中，返回带cookie的header头
#   改进方向
    *   存入数据库时记录登陆帐号与登陆日期（需要修改数据库结构，不建议采用）
    *   待检查代码逻辑
    *   优化提示
def OldPostHeader(cursor=None)
#   函数说明
    *   返回最新的可用cookie与距离失效的时间长度
        1.  当数据库内有记录时直接返回数据库内的记录
        2.  当数据库中无记录时返回内嵌在代码中的记录
#   改进方向
    *   暂无
def InputUserNameandPassword():
#   函数说明
    *   校验用户名密码是否正确，若正确则返回用户名与密码
    *   辅助类函数
#   改进方向
    *   优化提示
def  returnConnCursor():
#   函数说明
    *   返回数据库链接
    *   若数据库文件不存在则新建一个
#   改进方向
    *   无
def CatchFrontInfo(ContentText='',Flag=0,Target=''):
#   函数说明
    *   读取首页信息，返回InfoDict
    *   对不同的类型返回不同的InfoDict
    *   ID
        *   InfoDict['IDLogoAdress']  
        *   InfoDict['ID']   
        *   InfoDict['Sign']   
        *   InfoDict['Name'] 
        *   InfoDict['Ask']          
        *   InfoDict['Answer']       
        *   InfoDict['Post']         
        *   InfoDict['Collect']      
        *   InfoDict['Edit']         
        *   InfoDict['Agree']
        *   InfoDict['Thanks'] 
        *   InfoDict['Followee']       
        *   InfoDict['Follower']    
        *   InfoDict['Watched']     
    *   Collect
        *   InfoDict['CollectionID']    
        *   InfoDict['Title']           
        *   InfoDict['Description'] 
        *   InfoDict['AuthorName'] 
        *   InfoDict['AuthorID'] 
        *   InfoDict['AuthorSign'] 
        *   InfoDict['FollowerCount'] 
    *   Topic
        *   InfoDict['TopicID']         
        *   InfoDict['Title']           
        *   InfoDict['Adress']          
        *   InfoDict['LogoAddress']     
        *   InfoDict['Description'] 
#   改进方向
    *
def CreateWorkListDict(PostHeader,TargetFlag,Target):
#   函数说明
    *   读取答案首页信息，生成RequestDict
    *   返回InfoDict，RequestDict
#   改进方向
    *   无
def returnIndexList(cursor=None,Target='',Flag=0,RequestDict={}):
#   函数说明
    *   返回一个答案索引列表
#   改进方向
    *   无
def SaveToDB(cursor=None,NeedToSaveDict={},primarykey='',TableName=''):
#   函数说明
    *   一个简易的数据库框架，将传入的字典中的每一个键值存入/更新至数据库中
    *   辅助类函数
#   改进方向
    *   暂无
def setMaxThread():
#   函数说明
    *   设定最大线程数
    *   工具类函数
#   改进方向
    *   暂无
###################ZhihuEpub############################
import  ZhihuEpub
def PrintInOneLine(text=''):
#   函数说明
    *   在一行内输出内容
    *   工具类函数
#   改进方向
    *   无
def OpenHttpPage(url=''):#打开网页,负责下载图片或者打开json列表,只尝试一次，失败时返回空字符串，错误信息中包含未打开网址。#
#   函数说明
    *   同OpenUrl
#   改进方向
    *   直接用OpenUrl替换之
    *   不要重复造轮子
def CheckImgFileExist(CheckList=[],ErrorList=[]):
#   函数说明
    *   检测CheckList中的文件是否存在
    *   不存在时添加到ErrorList中
#   改进方向
    *   考虑是否要将文件名修改为『知乎网页目录_知乎图片』的格式    
def DownloadPicWithThread(ImgList=[],MaxThread=20):#添加图片池功能#当图片下载完成时在ImgList中删除之
#   函数说明
    *   用于分线程下载图片
    *   将下载失败的链接添加进『./下载失败的图片列表.txt』中
#   改进方向
    *   无
def returnCursor():
#   函数说明
    *   返回一个数据库连接
    *   数据库不存在时直接退出
#   改进方向
    *   无
def  Mkdir(DirName=u''):
#   函数说明
    *   创建一个目录
#   改进方向
    *   无
def CreateMimeType():
#   函数说明
    *   创建MimeType文件
    *   此文件为固定文件，无需改进
#   改进方向
    *   独立到一个文件中，避免占用主程序代码行数
def CreateContainer_XML():
#   函数说明
    *   创建container.xml文件
    *   此文件为固定文件，无需改进
#   改进方向
    *   独立到一个文件中，避免占用主程序代码行数
def returnTagContent(text='',tagname=''):
#   函数说明
    *   返回制定标签内的文字内容
    *   没有在程序中用到
#   改进方向
    *   如果没用的话，可以移除掉
    *   或者用于生成无格式电子书
def removeTag(text='',tagname=[]):
#   函数说明
    *   移除指定Tag
    *   没有用到
#   改进方向
    *   可以考虑移除
def removeAttibute(text='',AttList=[]):
#   函数说明
    *   移除text元素中AttList里指定的属性
#   改进方向
    *   无
def closeimg(text='',ImgList=[]):
#   函数说明
    *   用于关闭图片标签
    *   同时移除'data-rawwidth','data-original'，"data-rawheight"属性，添加'alt'，'height'属性
    *   属于为使知乎网页符合XHTML标准所添加的一系列函数中的一部分
#   改进方向
    *   对于答案内容可否直接将替换为原图？而不是_m.jpg
    *   功能建议via@
def PixName(t):
#   函数说明
    *   提取图片名
#   改进方向
    *   直接改成匿名函数完了
def fixPic(t='',ImgList=[]):
#   函数说明
    *   将src替换为正确的位置，同时讲图片链接提交到ImgList中
#   改进方向
    *   无
def DownloadImg(imghref='',ErrorList=[]):
#   函数说明
    *   下载图片
#   改进方向
    *   对于40X错误的图片应该直接忽略掉
def CreateOPF(OPFInfoDict={},Mainfest='',Spine='')
#   函数说明
    *   生成OPF文件
#   改进方向
    *   无
    *   传入的Mainfest与Spine待改进
def CreateNCX(NCXInfoDict={},Ncx=''):
#   函数说明
    *   生成NCX文件
#   改进方向
    *   无
    *   传入的Ncx待改进
def PrintDict(Dict={}):
#   函数说明
    *   输出字典   
#   改进方向
    *   与ZhihuHelp内的PrintDict雷同，应去除
def  ZipToEpub(EpubName='a.epub'):
#   函数说明
    *   生成Epub电子书
    *   将文件夹内容压缩为一个Zip包
#   改进方向
    *   实现递归压缩
    *   美化输出内容
def ChooseTarget(url=''):#选择
#   函数说明
    *   匹配代号
#   改进方向
    *   与ZhihuHelp类似，可取消
def DealAnswerDict(cursor=None,AnswerDict={},ImgList=[]):#必须是符合规定的Dict，规定附后
#   函数说明
    *   处理答案内容并输出   
#   改进方向
    *   
def MakeInfoDict(InfoDict={},TargetFlag=0):
#   函数说明
    *   生成首页信息  
#   改进方向
    *   应添加更多内容
###################ZhihuEpub############################



def 
#   函数说明
    *   
#   改进方向
    *   
def 
#   函数说明
    *   
#   改进方向
    *   
def 
#   函数说明
    *   
#   改进方向
    *   



def 源码Tag说明：
    #PassTag        :   校验无误且无需进一步改进
    #newCommitTag   :   本次新提交
    #UnitTest       :   需编写单元测试
    #









