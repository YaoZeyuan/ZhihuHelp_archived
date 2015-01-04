# -*- coding: utf-8 -*-
u"""
这个类的目的是建立一个符合Epub规范的文件夹，将传入的电子书内容按规范整理至文件夹内，确保再经一步压缩就能输出为电子书

提供简单的接口

"""
class Ncx                            
class NavMap                         
class NavPoint                       
class PageList                       
class PageTarget                     
class NavList                        
class NavTarget                      

class Opf
class Metadata():
    def __init__(self):
        self.content = ''
        self.attr    = {}
        self.metadateList = ['title', 'indentifier', 'language', 'creator', 'description', 'rights', 'publisher']
        return 

    def addTitle(self, title):
        self.attr['title'] = title 
        return
    
    def addIdentifier(self, id):
        self.arrt['identifier'] = id
        return

    def addLanguage(self, lang):
        self.attr['language'] = lang
        return
    
    def addCreator(self, creator):
        self.attr['creator'] = creator
        return

    def addDesc(self, desc):
        self.attr['description'] = desc
        return

    def addRight(self, right):
        self.attr['rights'] = right
        return

    def addPublisher(self, publisher):
        self.attr['publisher'] = publisher
        return

    def addCover(self, coversrc):#需要和mainfest同步执行
        self.attr['cover'] = coversrc
        return
    
    def getString(self):#返回根据设定数据产生的metadata字符串
        content = '<metadata>\n'
        for key in self.metadateList:
            if key in self.attr:
                if key != 'identifier':
                    content += "<dc:{0}>{1}</dc:{0}>\n".format(key, self.attr[key])
                else:
                    content += "<dc:{0} id='{1}'>{1}</dc:{0}>\n".format(key, self.attr[key])
        content += "</metadata>\n"
        return content


class Manifest
class ManifestItem
class Spine
class Guide

def init(booktitle):
    mkdir('./' + (str)booktitle)
    chdir('./' + (str)booktitle)
    writeMimetype()

    mkdir('./META-INF')
    chdir('./META-INF')
    writeContentXml()
    chdir('../')

    mkdir('./OEBPS')
    mkdir('./OEBPS/html')
    mkdir('./OEBPS/image')
    chdir('./OEBPS')

def writeMimetype():
    f = fopen('mimetype', 'wb')
    f.write('application/epub+zip')
    f.close()
    return

def writeContentXml():
    f = fopen('mimetype', 'wb')
    f.write(u'''
<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" 
    media-type="application/oebps-package+xml" />
  </rootfiles>
</container>
''')
    f.close()
    return


#工具函数
import os
def mkdir(path):
    try:
        os.mkdir(path)
    except OSError:
        print u'指定目录已存在'
    return 

def chdir(path):
    try:
        os.chdir(path)
    except OSError:
        print u'指定目录不存在，自动创建之'
        mkdir(path)
        os.chdir(path)
    return
