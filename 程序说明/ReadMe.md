#程序说明
##2014年3月31日23:51:40
##def	returnPostHeader(UserID='mengqingxue2014@qq.com',Password='131724qingxue'，LoginSuccessFlag=True)
###	函数说明
	*	传入UserID与Password,返回一个携带Cookie的Http头字典
	*	默认登陆ID为@孟晴雪
	*	网络故障或登陆失败时打印错误信息，需要依次输入帐号密码重新登陆
##class	HtmlParser(HTMLParser.HTMLParser)
###类说明
	*	使用feed(HtmlContent)传入网页内容
	*	使用returnAnswerList()返回提取出的答案链接列表
	*	格式：['/question/21354/answer/15488',]
##def PictureReload(Content=''):
###函数说明
	*	知乎网页中的图片采用懒加载模式，处理后才能返回正确的图片链接
	*	传入网页内容，返回带图片链接的网页内容
##def ReturnRealAnswerContent(text=''):
###函数说明
	*	传入目标网页
	*	返回答案内容
##def ReadPersonInfo(k="")
###函数说名
	*	传入用户答案页内容，返回一个字典，字典内为提取出的用户信息
	*	字典内容：      
    *   Dict['ID_Asks']	        
    *   Dict['ID_Answers']	    
    *   Dict['ID_Posts']	    
    *   Dict['ID_Collections']	
    *   Dict['ID_Logs']	        
    *   Dict['ID_Followees']	
    *   Dict['ID_Followers']	
    *   Dict['ID_Visit']	    
    *   Dict['ID_ID']	        
    *   Dict['ID_Name']	        
    *   Dict['ID_Sign']	        
##def ReadCollectionInfo(k="")
###函数说明
	*	传入收藏夹主页页面内容，返回一个字典，字典内为提取出的收藏夹信息
	*	字典内容
    *   Dict['title']     
    *   Dict['AuthorID']  
    *   Dict['AuthorName']
	*	Dict['followerCount']
##def FetchMaxAnswerPageNum(Content="")
###函数说明
	*	输入收藏夹或用户答案首页内容，返回答案页面最大值
##def ReadAnswer(k='',url="",ID="",Name="")
###函数说明
	*	k为答案内容，由returnRealAnswerContent()返回。url为答案地址，ID、Name为答主ID与用户名，校验用，置空意为答案页面由收藏夹传入
	*	返回一个字典，字典内为提取出的答案信息
	*	字典内容
		*	说明：当用户为匿名用户时ID置为404nofFound!，Name=匿名用户
		*	PS：404nouFound这个ID都能存在是要闹那样？
    *   Dict["ID"]              
    *   Dict["Sign"]            
    *   Dict["AgreeCount"]      
    *   Dict["CollectionCount"] 
    *   Dict["CommitCount"]     
    *   Dict["QuestionID"]      
    *   Dict["AnswerID"]        
    *   Dict["UpdateTime"]      
    *   Dict["QuestionTitle"]   
    *   Dict["Questionhref"]    
    *   Dict["AnswerContent"]   
    *   Dict["UserName"]        
    *   Dict["QuestionTitle"]   
    *   Dict["Questionhref"]    
    *   Dict["AnswerID"]        
    *   Dict["QuestionID"]      
##OpenUrl(Request)
###函数说明
	*传入一个网页Request，返回网页内容，报错返回空字符串，如若网页打开失败会自动重读，超时重读3次，400系列错误直接返回空字符串，其余错误重读10次
	*返回两个字典，Dict为文件信息，用于生成回答集锦的头部，RequestDict为待抓取答案页面字典
	*Request请求使用urllib2.Request()进行制作
##WorkForFetchFrontPageInfo(ID='',Collect='',PostHeader={})
###函数说明
	*传入ID或Collection序号，都为空值报错退出，均有值则只读取ID。需要传入一个PostHeader字典，由returnPostHeader给出
	*读取首页信息，返回待抓取答案链接的网页字典RequestDict，键为从0开始递增的数字，值为一个列表，第一项是Request，第二项为待读取标记，默认为False
	*若网页打不开则抛出一个NameError，直接退出
##WorkForFetchUrl(RequestDict={},Page=0)
###函数说明
	*抓取RequestDict[Page]中的答案链接，抓完后将待读取的列表存入RequestDict[Page][0]中，RequestDict[Page][1]置True
##WorkForGetAnswer(RequestDict={},Page=0,ID='',Name="")
###函数说明
	*抓取RequestDict[Page]上的答案，抓完后将答案Dict置入RequestDict[Page][0]中，RequestDict[Page][1]置True
	*ID用于区别收藏夹与用户，ID为空即为读取的是收藏夹内的内容
##WorkForSuitUrl(RequestDict={},PostHeader={})
###函数说明
	*将WorkForFetchUrl()返回的RequestDict处理为适合WorkForGetAnswer（）读取的格式
	*返回一个答案Request字典，键为数字升序，值为答案所在网页的Request
	*答案Request按读取时的页面顺序排列,1为第一页第一条，2为第一页第二条，21为第二页第一条，22为第二页第二条，41为第三页第一条，63为第四页第三条e.g.
##ThreadWorker_FetchUrl(MaxThread=5,RequestDict={})
###函数说明
	*分线程抓取RequestDict中的全部答案链接，MaxThread为最大线程数
	*为任务调配函数，无返回值
##ThreadWorker_GetAnswer(MaxThread=5,RequestDict={},PostHeader={},ID="",Name="")
###函数说明
	*类似ThreadWorker_FetchUrl（）
	*分线程抓取RequestDict中的全部答案内容，MaxThread为最大线程数
	*为任务调配函数，无返回值
##CheckUpdate()
###函数说明
	*读取http://zhihuhelpbyyzy-zhihu.stor.sinaapp.com/ZhihuHelpUpdateTime.txt上的版本信息，发现新版本时打开url进行更新
##ChooseTarget()
###函数说明
	*首屏
	*输入用户主页地址或收藏夹地址，返回
		*True，ID
		*False,Collect
	*识别失败直接退出
##ShaoErBuYi(InfoDict={},IDFlag=True)
###函数说明
	*太长了，少儿不宜。。。
	*输入InfoDict和IDFlag，
		*True为ID内容，
		*False为收藏夹内容
	*返回根据InfoDict生成的Html文档头，内含MarkDown样式
## WriteHtmlFile(Dict={},InfoDict={},IDFlag=True)
###函数说明
	*Dict为答案字典，InfoDict为用户信息字典，IDFlag=True为用户答案集锦，False为收藏夹
	*将答案写入到[用户名]的知乎回答集锦.html或[收藏夹名].html文件中
	*文件位置位于程序所在文件夹内

