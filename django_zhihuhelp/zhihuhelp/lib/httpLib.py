# -*- coding: utf-8 -*-
import  urllib2
import  urllib#编码请求字串，用于处理验证码
import  socket#用于捕获超时错误
import  zlib

def decodeGZip(rawPageData):
    u"""返回处理后的正常网页内容
 
    判断网页内容是否被压缩，无则直接返回，若被压缩则使用zlip解压后返回
    
    参数:
        rawPageData   urlopen()传回的fileLike object
    返回:
        pageContent   页面内容，字符串或二进制数据|解压缩失败时则返回空字符串
    报错:
        无
    """
    if rawPageData.info().get(u"Content-Encoding") == "gzip":
        try:
            pageContent = zlib.decompress(rawPageData.read(), 16 + zlib.MAX_WBITS)
        except zlib.error as ziperror:
            print u'解压出错'
            print u'出错解压页面:' + rawPageData.geturl()
            print u'错误信息：'
            print zliberror
            return ''
    else:
        pageContent = rawPageData.read()
        return pageContent

def getHttpContent(url='', header={} , data=None, timeout=5):
    u"""获取网页内容
 
    获取网页内容, 打开网页超过设定的超时时间则报错
    
    参数:
        url         一个字符串,待打开的网址
        header      一个简单字典,需要添加的http头信息
        data        需传输的数据,默认为空
        timeout     int格式的秒数，打开网页超过这个时间将直接退出，停止等待
    返回:
        pageContent 打开成功时返回页面内容，字符串或二进制数据|失败则返回空字符串
    报错:
        IOError     当解压缩页面失败时报错
    """
    if data == None:
        request = urllib2.Request(url = url)
    else:
        request = urllib2.Request(url = url, data = data)
    for headerKey in header.keys():
        request.add_header(headerKey, header[headerKey])
    try: 
        rawPageData = urllib2.urlopen(request, timeout = timeout)
    except  urllib2.HTTPError as error:
        print u'网页打开失败'
        print u'错误页面:' + url
        if hasattr(error, 'code'):
            print u'失败代码:' + str(error.code)
        if hasattr(error, 'reason'):
            print u'错误原因:' + error.reason
    except  urllib2.URLError as error:
        print u'网络连接异常'
        print u'错误页面:' + url
        print u'错误原因:'
        print error.reason
    except  socket.timeout as error:
        print u'打开网页超时'
        print u'超时页面' + url
    else:
        return decodeGZip(rawPageData)
    return ''
