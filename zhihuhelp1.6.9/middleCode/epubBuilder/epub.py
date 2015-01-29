# -*- coding: utf-8 -*-

class EpubData(object):
    def __init__(self, info):
        if info['kind'] == 'question':
            """
            select * from AnswerContent where questionID == {questionID} 
            and answerAgreeCount > {minAgree} and answerAgreeCount < {maxAgree}
            and updateDate > {minDate} and updateDate < {maxDate}
            """

    
    
    
class EpubBuilder(object):
    u"""
    只负责对文件按既定规则进行处理
    传入字典,字典结构为
    {
        "index"     : "html文件地址"
        "index"     : {新的字典}
        "index"     : "html文件结构地址"
        ...
    }
        #然后有些关键属性自行添加
    关键属性
    *   "bookInfo" 
        *   title
        *   identifier
        *   language
        *   creator
        *   description
        *   right#版权声明
        *   publisher#出版人
    *   mainfest#资源列表
        *   可以自行添加
        *   自动判断文件类型或手工指定文件类型
    *   spine#显示顺序
        *   根据传入顺序自动生成
    *   NCX#目录结构
        *   根据传入字典自动生成
    
        传入缓存下来的图片地址,然后到图片地址去复制图片到images
        传入的html文件名中自带路径
    """
    def creator():
        self.bookInfo = ['title', 'indentifier', 'language', 'creator', 'description', 'right', 'publish']
        self.epub     = epubBuilder() 

    def __init__(self, rootPath = './', book = {}):
        self.mkDir(rootPath + book['title'])
        self.cdDir(rootPath + book['title'])
        self.createMimeType()
        self.mkDir('./META-INF')
        self.createContainer()
        self.mkDir('./OEBPS')
        self.cdDir(rootPath + book['title'] + '/OEBPS')
        self.mkDir('./html')
        self.mkDir('./images')
        
        self.initOPF()
        self.initNCX()
        
    def initOPF(self):
        self.OPF   = u'''<?xml version='1.0' encoding='utf-8'?>'''
        self.spine = u'<spine toc="ncx">\n'

    def initNCX(self):
        self.NCX = u'''<?xml version='1.0' encoding='utf-8'?>
                        <!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
                        <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
                   '''
    
    def addBookProperty(self, book = {}):
        #format OPF
        bookInfo = ['title', 'indentifier', 'language', 'creator', 'description', 'right', 'publish']
        self.OPF += '<package unique-identifier="{0}" version="2.0">\n'.format(book['indentifier'])
        self.OPF += '<metadata xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        for key in bookInfo:
            self.OPF += "<dc:{0}>{1}</dc:{0}>\n".format(key, book[key])
        self.OPF += "</metadata>\n"

        #format NCX
        self.NCX += u'''
        <head>
          <meta name="dtb:uid" content="{0}"/>
          <meta name="dtb:depth" content="-1"/>
          <meta name="dtb:totalPageCount" content="0"/>
          <meta name="dtb:maxPageNumber" content="0"/>
        </head>
        '''.format(book['indentifier'])
        self.NCX += u'''
        <docTitle>
          <text>{0}</text>
        </docTitle>
        <navMap>
        '''.format(book['title'])

    def addResourse2OPF(self, bookContent = {}):
        #for key in bookContent:
        #    if:
        #        chapter = bookContent[key]
        #        f = open(chapter['src'], 'wb')
        #        f.write(chapter['content'])
        #        f.close()
        #        
        return
    
    def copyFile(self):
        return
    
    def createMimeType(self):
        f = open('./mimetype','w')
        f.write('application/epub+zip')
        f.close()

    def createContainer(self):
        f   =   open('./META-INF/container.xml','w')      
        f.write('''<?xml version="1.0"?>
                     <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
                       <rootfiles>
                         <rootfile full-path="OEBPS/content.opf"
                          media-type="application/oebps-package+xml" />
                       </rootfiles>
                     </container>''')
        f.close()

    def CreateOPF(bookInfo={}, mainfest='', spine=''):
        f = open('./OEBPS/content.opf','w')
        f.write(u'''<?xml version='1.0' encoding='utf-8'?>
                      <package unique-identifier="%(bookID)s" version="2.0">
                        <metadata xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/"  >
                          <dc:title>%(bookTitle)s</dc:title>
                          <dc:identifier id="%(bookID)s">%(bookID)s</dc:identifier>
                          <dc:language>zh-CN</dc:language>
                          <dc:creator>%(author)s</dc:creator>
                          <dc:description>%(descripe)s</dc:description>
                          <dc:rights>本电子书由知乎助手制作生成，仅供个人阅读学习使用，严禁用于商业用途</dc:rights>
                          <dc:publisher>知乎</dc:publisher>
                          <meta name="cover" content="cover-image" />
                        </metadata>
                        <!-- Content Documents -->
                        <manifest>
                          <item id="main-css" href="stylesheet.css" media-type="text/css"/> <!--均与OPF处同一文件夹内，所以不用写绝对路径-->
                          <item id="ncx"   href="toc.ncx"           media-type="application/x-dtbncx+xml"/>
                          <item id="cover" href="html/cover.html"   media-type="application/xhtml+xml"/>
                          <item id="title" href="html/title.html"   media-type="application/xhtml+xml"/>'''%bookInfo + mainfest +
                u'''
                          <item id="cover-image" href="images/bookCover.png" media-type="image/png"/>
                        </manifest>
                        <spine toc="ncx" >
                          <itemref idref="cover" linear="yes"/>
                          <itemref idref="title" linear="yes"/>
                      
                ''' + spine + 
                u'''
                        </spine>
                        <guide>
                          <reference type="cover"  title="封面" href="html/cover.html"   />
                          <reference type="toc"    title="目录" href="html/title.html" />
                        </guide>
                      </package>
                ''')
        f.close()
    def CreateNCX(NCXInfoDict={},Ncx=''):#PassTag
        f   = open('./OEBPS/toc.ncx','w')
        f.write('''<?xml version='1.0' encoding='utf-8'?>
                   <!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
                     <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
                       <head>
                         <meta name="dtb:uid" content="%(AuthorAddress)s"/>
                         <meta name="dtb:depth" content="-1"/>
                         <meta name="dtb:totalPageCount" content="0"/>
                         <meta name="dtb:maxPageNumber" content="0"/>
                       </head>
                       <docTitle>
                         <text>%(BookTitle)s</text>
                       </docTitle>'''%NCXInfoDict + Ncx + ''' 
                     </ncx>''')
        f.close()
