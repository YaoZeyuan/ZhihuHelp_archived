# -*- coding: utf-8 -*-
import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 

import re
import ConfigParser
import os

def printDict(data = {}, key = '', prefix = ''):
    if isinstance(data, dict):
        for key in data.keys():
            printDict(data[key], key, prefix + '   ')
    else:
        print prefix + str(key) + ' => ' + str(data)

def getXsrf(content=''):
    xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', content)
    if xsrf == None:
        return ''
    else:
        return '_xsrf=' + xsrf.group(0)

def save2DB(cursor, data={}, primaryKey='', tableName=''):
    u"""
        *   功能
            *   提供一个简单的数据库储存函数，按照data里的设定，将值存入键所对应的数据库中
            *   若数据库中没有对应数据，执行插入操作，否则执行更新操作
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
    try:
        rowCount = cursor.execute('select count(%(primaryKey)s) from %(tableName)s where %(primaryKey)s = ?' % {'primaryKey' : primaryKey, 'tableName' : tableName}, (data[primaryKey], )).fetchone()[0]
        pass
    except Exception as error:
        print u'SQL runtime error'
        print error
        print u'SQL = ' + 'select count(%(primaryKey)s) from %(tableName)s where %(primaryKey)s = ?' % {'primaryKey' : primaryKey, 'tableName' : tableName} 
        print u'primaryKey = ' + str(data[primaryKey])
        printDict(data)
        exit()
    insertSql   = 'insert into '+ tableName +' ('
    updateSql   = 'update '+ tableName +' set '
    placeholder = ') values ('
    varTuple = []
    for columnKey in data:
        insertSql   += columnKey + ','
        updateSql   += columnKey + ' = ?,'
        placeholder += '?,'
        varTuple.append(data[columnKey])

    if rowCount == 0:
        #print 'sql测试'
        #print 'sql = ' + insertSql[:-1] + placeholder[:-1] + ')'
        cursor.execute(insertSql[:-1] + placeholder[:-1] + ')', tuple(varTuple))
    else:
        varTuple.append(data[primaryKey])
        #print 'sql测试'
        #print 'sql = ' + updateSql[:-1] + ' where ' + primaryKey + '= ?'
        #print varTuple
        cursor.execute(updateSql[:-1] + ' where ' + primaryKey + '= ?', tuple(varTuple))
    #print 'sql execute complete'
