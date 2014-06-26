# -*- coding: utf-8 -*-
import  urllib2
import  re
import  zlib
import  threading
import  time
import  datetime
import  HTMLParser#HTML解码&lt;
import  json#在returnPostHeader中解析Post返回值
import  os#打开更新页面

import  urllib#编码请求字串，用于处理验证码


import  sys#修改默认编码
reload( sys )
sys.setdefaultencoding('utf-8')



import  sqlite3#数据库！

###########################################################
#数据库部分
import  pickle
import  socket#捕获Timeout错误
##################Epub########################################
###########################################################
#所有可复用的函数均已转移至Epub文件内
######################网页内容分析############################
#个人答案页面、收藏夹页面答案连接提取
for k   in  range(10):
    for p   in  os.listdir(str(k+1)):
        f   =   open(str(k+1)+'/'+p,'r')
        try :
            print   re.search(r'(?<=<refhref=").*?(?=/>)',f.read().replace("\r",'').replace("\n",'').replace(' ','')).group(0)
        except  :
            pass
print   'over'
