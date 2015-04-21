# -*- coding: utf-8 -*-
import os
import re
import shutil

from htmlTemplate import *
from imgDownloader import *
from epub import *
from dict2Html import dict2Html

class Zhihu2Epub():
    u'''
    初版只提供将Question-Answer格式的数据转换为电子书的功能
    预计1.7.3版本之后再提供将专栏文章转换为电子书的功能
    '''
    def __init__(self, contentPackage):
        self.package = contentPackage
        self.imgSet  = set()#用于储存图片地址，便于下载
        self.trans   = dict2Html(contentPackage)

        self.kindDict = {
                'question'   : u'问题',
                'answer'     : u'问答',
                'topic'      : u'话题',
                'collection' : u'收藏夹',
                'table'      : u'圆桌',
                'author'     : u'作者',
                'column'     : u'专栏',
                'article'    : u'文章',
                'merge'      : u'合并',
                } 

        self.initBasePath()
        self.info2Title()
        self.trans2Tree()
        self.imgDownload()
        self.epubCreator()

        return
    
    def initBasePath(self):
        basePath = u'./知乎助手临时资源库/'
        targetPath = u'./助手生成的电子书/'
        self.mkdir(targetPath)
        self.mkdir(basePath)
        self.chdir(basePath)
        self.baseImgPath = u'./知乎图片池/'
        self.mkdir(self.baseImgPath)
        self.baseContentPath = u'./{}/'.format(u'知乎网页内容缓存库')
        self.rmdir(self.baseContentPath)
        self.mkdir(self.baseContentPath)
        return

    def trans2Tree(self):
        u'''
        将电子书内容转换为一系列文件夹+html网页
        '''
        self.contentList = self.trans.getResult()
        self.imgSet      = self.trans.getImgSet()
        for content in self.contentList:
            fileIndex = self.baseContentPath + content['fileName'] + '.html'
            htmlFile  = open(fileIndex, 'wb')
            htmlFile.write(content['fileContent'])
            htmlFile.close()
        return

    def info2Title(self):
        self.fileTitle = u'{kind}_{title}({ID})_知乎回答集锦'.format(kind=self.kindDict[self.package['kind']], title=self.package['title'], ID=self.package['ID'])
        illegalCharList = ['\\', '/', ':', '*', '?', '<', '>', '|', '"']
        for illegalChar in illegalCharList:
            self.fileTitle = self.fileTitle.replace(illegalChar, '')
        return

    def imgDownload(self):
        downloader  = ImgDownloader(targetDir = self.baseImgPath, imgSet = self.imgSet)
        self.downloadedImgSet = downloader.leader()
        return
    
    def epubCreator(self):
        book = Book(self.fileTitle, '27149527')
        for content in self.contentList:
            htmlSrc = '../../' + self.baseContentPath + content['fileName'] + '.html'
            title   = content['contentName']
            book.addHtml(src = htmlSrc, title = title)
        for src in self.downloadedImgSet:
            imgSrc = '../../' + self.baseImgPath + src
            if src == '':
                continue
            book.addImg(imgSrc)
        #add property
        book.addLanguage('zh-cn')
        book.addCreator('ZhihuHelp1.7.0')
        book.addDesc(u'该电子书由知乎助手生成，知乎助手是姚泽源为知友制作的仅供个人使用的简易电子书制作工具，源代码遵循WTFPL，希望大家能认真领会该协议的真谛，为飞面事业做出自己的贡献 XD')
        book.addRight('CC')
        book.addPublisher('ZhihuHelp')
        book.addCss(u'../../../epubResource/markdownStyle.css')
        book.addCss(u'../../../epubResource/userDefine.css')

        print u'开始制作电子书'
        book.buildingEpub()
        return

    def printCurrentDir(self):
        print os.path.realpath('.')
        return

    def mkdir(self, path):
        try:
            os.mkdir(path)
        except OSError:
            pass
        return 
    
    def chdir(self, path):
        try:
            os.chdir(path)
        except OSError:
            print u'指定目录不存在，自动创建之'
            mkdir(path)
            os.chdir(path)
        return

    def rmdir(self, path):
        shutil.rmtree(path = path, ignore_errors = True)
        return
