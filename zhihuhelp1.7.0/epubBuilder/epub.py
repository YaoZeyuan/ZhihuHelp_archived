# -*- coding: utf-8 -*-
u"""
这个类的目的是建立一个符合Epub规范的文件夹，将传入的电子书内容按规范整理至文件夹内，确保再经一步压缩就能输出为电子书

提供简单的接口

"""
class Metadata():
    def __init__(self):
        self.content = ''
        self.coverImg= ''
        self.attr    = {}
        self.metadateList = ['title', 'identifier', 'language', 'creator', 'description', 'rights', 'publisher']
        return 

    def addTitle(self, title = ''):
        self.attr['title'] = title 
        return
    
    def setUID(self, id):
        self.attr['identifier'] = id
        return

    def addLanguage(self, lang = ''):
        self.attr['language'] = lang
        return
    
    def addCreator(self, creator = ''):
        self.attr['creator'] = creator
        return

    def addDesc(self, desc = ''):
        self.attr['description'] = desc
        return

    def addRight(self, right = ''):
        self.attr['rights'] = right
        return

    def addPublisher(self, publisher = ''):
        self.attr['publisher'] = publisher
        return

    def addCoverImg(self, id = ''):#需要和mainfest同步执行
        self.coverImg += '<meta name="cover" content="{0}" />\n'.format(id)
        return

    def getString(self):#返回根据设定数据产生的metadata字符串
        content = '<metadata>\n'
        for key in self.metadateList:
            if key in self.attr:
                if key != 'identifier':
                    content += "<dc:{0}>{1}</dc:{0}>\n".format(key, self.attr[key])
                else:
                    content += "<dc:identifier id='{0}'>{0}</dc:identifier>\n".format(self.attr['identifier'])
        content += self.coverImg
        content += "</metadata>\n"
        return content

import shutil
import zipfile
import os

class Book():
    u'假定制作电子书添加文件时为线性添加'
    def __init__(self, bookTitle, bookID):
        self.mainfest    = Mainfest()
        self.spine       = Spine()
        self.guide       = Guide() 
        self.metaData    = Metadata() 
        self.ncx         = Ncx()
        self.bookID      = bookID
        self.bookTitle   = bookTitle
        self.identifier = 1 #用于生成递增ID
        self.index       = ''#用于生成目录 
        
        rmdir(u'./' + str(self.bookTitle))
        mkdir(u'./' + str(self.bookTitle))
        chdir(u'./' + str(self.bookTitle))
        self.__writeMimetype()
        self.addTitle(self.bookTitle)
        self.addIdentifier(self.bookID)

        mkdir('./META-INF')
        chdir('./META-INF')
        self.__writeContentXml()
        chdir('../')

        mkdir('./OEBPS')
        mkdir('./OEBPS/html')
        mkdir('./OEBPS/images')
        chdir('./OEBPS')
        self.createIndex()
        return

    def __writeMimetype(self):
        f = open('mimetype', 'wb')
        f.write('application/epub+zip')
        f.close()
        return
    
    def __writeContentXml(self):
        f = open('container.xml', 'wb')
        f.write(u'''<?xml version="1.0"?>
                <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
                  <rootfiles>
                    <rootfile full-path="OEBPS/content.opf" 
                    media-type="application/oebps-package+xml" />
                  </rootfiles>
                </container>
                ''')
        f.close()
        return

    def __getFileName(self, src):
        return os.path.split(src)[1]

    def addHtml(self, src, title, linear=True):
        u'章节之间使用文件名区隔，而不是使用文件夹形式进行区隔，html文件夹中只有一层目录'
        shutil.copy(src, './html/')
        fileName = self.__getFileName(src)
        self.identifier += 1 
        id = self.identifier
        self.mainfest.addHtml(fileName, id)
        self.spine.addFile(id, linear=True)
        self.ncx.addFile(fileName, id, title)
        self.index += '<li><a href="{0}">{1}</a></li>'.format(fileName, title)#test此处尚欠考虑，待测试时再监测
        return

    def addImg(self, src):
        shutil.copy(src, './images/')
        fileName = self.__getFileName(src)
        self.identifier += 1 
        id = self.identifier
        self.mainfest.addImg(fileName, id)
        return

    def addCss(self, src):
        shutil.copy(src, './')
        fileName = self.__getFileName(src)
        self.identifier += 1 
        id = self.identifier
        self.mainfest.addCss(fileName, id)
        return

    def addCoverHtml(self, src, title):
        u"""
        cover只能是html网页
        """
        shutil.copy(src, './html')
        fileName = self.__getFileName(src)
        self.identifier += 1 
        id = self.identifier
        self.mainfest.addHtml(fileName, id)
        self.spine.addFile(id, linear=False)
        self.ncx.addFile(fileName, id, title)
        self.guide.addCoverHtml(fileName, title)
        self.index += '<li>{0}</li>'.format(title)
        return

    def addInfoPage(self, src, title):
        u"""
        cover只能是html网页
        """
        shutil.copy(src, './html')
        fileName = self.__getFileName(src)
        self.identifier += 1 
        id = self.identifier
        self.mainfest.addHtml(fileName, id)
        self.spine.addFile(id, linear=True)
        self.ncx.addFile(fileName, id, title)
        self.guide.addInfoPage(fileName, title)
        self.index += '<li>{0}</li>'.format(title)
        return

    def addCoverImg(self, src):
        shutil.copy(src, './images/')
        fileName = self.__getFileName(src)
        self.identifier += 1 
        id = self.identifier
        self.mainfest.addImg(fileName, id)
        self.metaData.addCoverImg(id)
        return

    def createChapter(self, src, id, title):
        shutil.copy(src, './html')
        fileName = self.__getFileName(src)
        self.identifier += 1 
        id = self.identifier
        self.ncx.addChapter(fileName, id, title)
        self.index += '<li>{0}</li>'.format(title)
        self.index += '<ol>'
        return

    def endChapter(self):
        self.ncx.endChapter()
        self.index += '</ol>'
        return

    def addTitle(self, title):
        self.metaData.addTitle(title)
        self.ncx.addBookTitle(title)
        return
    
    def addIdentifier(self, id):
        self.bookID = id
        self.metaData.setUID(id)
        self.ncx.setUID(id)
        return

    def addLanguage(self, lang):
        self.metaData.addLanguage(lang)
        return
    
    def addCreator(self, creator):
        self.metaData.addCreator(creator)
        return

    def addDesc(self, desc):
        self.metaData.addDesc(desc)
        return

    def addRight(self, right):
        self.metaData.addRight(right)
        return

    def addPublisher(self, publisher):
        self.metaData.addPublisher(publisher)
        return

    def createIndex(self):
        content = ''
        src = './html/index.html'
        f = open(src, 'w')
        f.write(content)
        f.close()

        fileName = self.__getFileName(src)
        self.identifier += 1 
        id = self.identifier
        self.mainfest.addHtml(fileName, id)
        self.spine.addFile(id, linear=False)
        self.guide.addIndex(src, fileName)
        self.ncx.addFile(fileName, id, fileName)
        return 
    
    def writeIndex(self):
        content = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="provider" content="www.zhihu.com"/>
    <meta name="builder" content="ZhihuHelpv1.7"/>
    <meta name="right" content="该文档由ZhihuHelp_v1.7生成。ZhihuHelp为姚泽源为知友提供的知乎答案收集工具，仅供个人交流与学习使用。在未获得知乎原答案作者的商业授权前，不得用于任何商业用途。"/>
    <link rel="markdownStyle.css" type="text/css" href="../markdownStyle.css"/>
    <link rel="userDefine.css" type="text/css" href="../userDefine.css"/>
    <title>目录</title>
  </head>
  <body>
    <div class="text-center">
      <h1>目录</h1>
    </div>
    <hr/>
    <br />
    <ol>
    {0}
    </ol>
  </body>
  </html>
    """.format(self.index)
        src = './html/index.html'
        f = open(src, 'w')
        f.write(content)
        f.close()
        return

    def buildingEpub(self):
        opf = open('../OEBPS/content.opf', 'w')
        opf.write(
u"""<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://www.idpf.org/2007/opf" 
xmlns:dc="http://purl.org/dc/elements/1.1/" 
unique-identifier="{0}" version="2.0">
{1}
{2}
{3}
{4}
</package>""".format(self.bookID, self.metaData.getString(), self.mainfest.getString(), self.spine.getString(), self.guide.getString())
        )
        opf.close()
        ncx = open('../OEBPS/toc.ncx', 'w')
        ncx.write(self.ncx.getString())
        ncx.close()
        self.writeIndex()
        #应当再加上生成目录的功能
        
        #直接使用的旧版函数，应当予以更新
        chdir('../../')
        filePath = u'./../助手生成的电子书/' + self.bookTitle + u'.epub'
        epub = zipfile.ZipFile(file = filePath, mode = 'w', compression = zipfile.ZIP_STORED, allowZip64=True)
        chdir(u'./' + self.bookTitle + u'/')
        epub.write('./mimetype')
        targetFileName = self.bookTitle + '.epub'
        def Help_ZipToEpub(Dir='.'):
            for p in os.listdir(Dir):
                if p == targetFileName or p == 'mimetype':
                    print u'该文件已添加，自动跳过'
                    continue
                filepath = os.path.join(Dir,p)
                if  not os.path.isfile(filepath):
                    if  p == '.' or p == '..':
                        continue
                    Help_ZipToEpub(Dir=filepath)
                else:
                    print u'将{}添加至电子书内'.format(filepath)
                    epub.write(filepath, compress_type=zipfile.ZIP_STORED)
        Help_ZipToEpub()
        epub.close()
        #test
        print u'恭喜，电子书{}制作完成'.format(self.bookTitle)
        return

class Mainfest():
    u'规定，所有img都应放在在images文件夹中，所有html内容都应放在html中'
    def __init__(self):
        self.img  = u''
        self.html = u''
        self.css  = u''
        self.imgType = {'jepg' : 'jpg', 'jpg' : 'jpg', 'png' : 'png', 'svg' : 'svg', 'gif' : 'gif'}
        return

    def addImg(self, fileName, id):
        u"图像文件只能是png,jpg,gif和svg四种类型"
        fileExt  =  os.path.splitext(fileName)[1][1:]
        fileType =  'image/' + self.imgType.get((fileExt).lower(), 'png')
        href     =  'images/' + fileName
        self.img += """<item id='{0}' href='{1}' media-type="{2}"/>\n""".format(str(id), href, fileType)
        return

    def addHtml(self, fileName, id):
        href = 'html/' + fileName
        self.html += """<item id='{0}' href='{1}' media-type="application/xhtml+xml"/>\n""".format(str(id), href)
        return

    def addCss(self, fileName, id):
        self.css  += u"""<item id="{0}" href="{1}" media-type="text/css"/>\n""".format(str(id), fileName)
        return
    
    def getString(self):
        content = u"""
          <manifest>
          <item id="ncx" href="toc.ncx" media-type="text/xml"/>
          {0}
          {1}
          {2}
          </manifest>
        """.format(self.img, self.html, self.css)
        return content

class Spine():
    def __init__(self):
        self.spine = u''
        return

    def addFile(self, id, linear=True):
        if linear:
            linear = 'yes'
        else:
            linear = 'no'
        self.spine += u"""<itemref idref="{0}" linear="{1}"/>\n""".format(str(id), linear)
        return
    
    def getString(self):
        content = u"""
        <spine toc="ncx">
          {0}
        </spine>
        """.format(self.spine)
        return content

class Guide():
    def __init__(self):
        self.guide = u""
        return

    def addCoverHtml(self, fileName, title):
        self.guide += u"""<reference href="{0}" type="cover" title="{1}"/>\n""".format(fileName, title) 
        return

    def addInfoPage(self, fileName, title):
        self.guide += u"""<reference href="{0}" type="title-page" title="{1}"/>\n""".format(fileName, title) 
        return

    def addIndex(self, fileName, title):
        self.guide += u"""<reference href="{0}" type="toc" title="{1}"/>\n""".format(fileName, title) 
        return

    def getString(self):
        content = u"""
        <guide>
          {0}
        </guide>
        """.format(self.guide)
        self.guide
        return content

class Ncx():
    def __init__(self):
        self.bookTitle = ''
        self.metaData  = ''
        self.depth     = -1
        self.ncx       = ''
        return

    def addFile(self, fileName, id, title):
        self.ncx += u"""
        <navPoint id="{0}" playOrder="{0}">
          <navLabel>
             <text>{1}</text>
          </navLabel>
          <content src="html/{2}"/>
        </navPoint>
        """.format(str(id), title, fileName)
        return

    def addChapter(self, fileName, id, title):
        self.ncx += u"""
        <navPoint id="{0}" playOrder="{0}">
          <navLabel>
             <text>{1}</text>
          </navLabel>
          <content src="html/{2}"/>
        """.format(str(id), title, fileName)
        return 

    def endChapter(self):
        self.ncx += u"""</navPoint>\n"""
        return

    def addBookTitle(self, title):
        self.bookTitle += u"""
        <docTitle>
           <text>{0}</text>
        </docTitle>
        """.format(title)
        return

    def setUID(self, uid):
        self.metaData += u"""
        <head>
          <meta name="dtb:uid" content="{0}"/>
          <meta name="dtb:depth" content="-1"/>
          <meta name="dtb:totalPageCount" content="0"/>
          <meta name="dtb:maxPageNumber" content="0"/>
        </head>
        """.format(str(uid))
        return
    
    def getString(self):
        content = u"""<?xml version='1.0' encoding='utf-8'?>
        <!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" 
          "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
        <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
        {0}
        {1}
        <navMap>
        {2}
        </navMap>
        </ncx>
        """.format(self.metaData, self.bookTitle, self.ncx)
        return content

#工具函数
import os
import re
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

def rmdir(path):
    shutil.rmtree(path = path, ignore_errors = True)
    return

