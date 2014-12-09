# -*- coding: utf-8 -*-
import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 

def printDict(data = {}, key = '', prefix = ''):
    if isinstance(data, dict):
        for key in data.keys():
            printDict(data[key], key, prefix + '   ')
    else:
        print prefix + str(key) + ' => ' + str(data)

def getXsrf(content=''):
    import re
    xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)',content)
    if xsrf == None:
        return ''
    else:
        return '_xsrf=' + xsrf.group(0)




def save2DB(cursor=None, data={}, primaryKey='', tableName=''):
    u"""
        *   功能
            *   提供一个简单的数据库储存函数，按照data里的设定，将值存入键所对应的数据库中
            *   表与主键由tableName ，primarykey指定
            *   注意，本函数不进行提交操作
        *   输入
            *   cursor
                *   数据库游标
            *   data
                *   需要存入数据库中的键值对
                *   键为数据库对应表下的列名，值为列值
            *   primarykey
                *   用于指定主键
            *   tableName
                *   用于指定表名
        *   返回
             *   无
     """
    rowCount = cursor.execute('select count(%{primaryKey}s) from %{tableName}s where %{primaryKey}s = ?' % {'primaryKey' : primaryKey, 'tableName' : tableName}, (data[primaryKey], )).fetchone()[0]
    insertSql   = 'insert into '+ tableName +' ('
    updateSql   = 'update '+ tableName +' set '
    placeholder = ') values ('
    varTuple = []
    for columnKey in data:
        insertSql   += columnKey + ','
        updateSql   += columnKey + ','
        placeholder += '?, '
        varTuple.append(data[t])

    if  rowCount==0:
        cursor.execute(insertSql[:-1] + placeholder[:-1] + ')', tuple(varTuple))
    else:
        varTuple.append(data[primaryKey])
        cursor.execute(updateSql[:-1] + ' where ' + primaryKey + '= ?', tuple(varTuple))

def getSetting(setting=[]):
    config = ConfigParser.SafeConfigParser()
    if not os.path.isfile('setting.ini'):
        f = open('setting.ini', 'w')
        f.close()
    config.read('setting.ini')
    
    data = {}
    if not config.has_section('ZhihuHelp'): 
        config.add_section('ZhihuHelp') 
    else:
        for key in setting:
          if config.has_option('ZhihuHelp', key):
              data[key] = config.get('ZhihuHelp', key, raw=True)
          else:
              data[key] = '';
    return data

def setSetting(setting={}):  
    config = ConfigParser.SafeConfigParser()
    if not os.path.isfile('setting.ini'):
        f   =   open('setting.ini','w')
        f.close()
    config.read('setting.ini')
    if not config.has_section('ZhihuHelp'): 
        config.add_section('ZhihuHelp') 
    for key in setting:
        config.set('ZhihuHelp', key, setting[key])
    config.write(open('setting.ini','w'))
    
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
