# -*- coding: utf-8 -*-
#试图创建一个Epub类，用类生成电子书
class   MakeTocNcx(object):
    u"""
    #   NCX 描述->来自IBM
    *   DTD 要求 NCX <head> 标记中包含四个 meta 元素：
        *   uid： 数字图书的惟一 ID。该元素应该和 OPF 文件中的 dc:identifier 对应。
        *   depth：反映目录表中层次的深度。该例只有一层，因此是 1。
        *   totalPageCount 和 maxPageNumber：仅用于纸质图书，保留 0 即可。
        *   docTitle/text 的内容是图书的标题，和 OPF 中的 dc:title 匹配。
    *   NCX navMap
        navMap 是 NCX 文件中最重要的部分，定义了图书的目录。navMap 包含一个或多个 navPoint 元素。每个 navPoint 都要包含下列元素：
        *   playOrder 属性，说明文档的阅读顺序。和 OPF spine 中 itemref 元素的顺序相同。
        *   navLabel/text 元素，给出该章节的标题。通常是章的标题或者数字，如 “第一章”，或者 — 像这个例子一样 — “封面”。
        *   content 元素，它的 src 属性指向包含这些内容的物理资源。就是 OPF manifest 中声明的文件（也可使用片段标识符引用 XHTML 内容中的锚元素 — 比如 content.html#footnote1）。
    还可以有一个或多个 navPoint 元素。NCX 使用嵌套的导航点表示层次结构的文档。
    #   NCX实现目标
    *   设定uid 
    *   设定标题
    *   自动计算深度
    *   navMap
        *   设定nav导航点
            *   例如根据赞同数来设定
                *   例如100赞一分隔
            *   或者由上级类指定如何分隔
                *   例如根据XML生成电子书
        *   设定navPoint页面
            *   自动生成playOrder
    """

class   Epub(object):
    u"""
    *   以下为类构思，MarkDown格式
    *   Epub类设定
    *   功能
        *   根据传入的XML结构文档生成电子书，只负责生成，不负责其他
        *   要求
            *   获取指定专栏页面内容
            *   获取答案内容 
    *   初始参数
        *   根目录位置
            *   需要设定根目录以生成电子书临时目录与最终输出电子书的目录
        *   图片池位置
            *   用于存放图片
        *   图书内容
            *   答案列表与图片模式
            *   前言
            *   封面
        *   答案排序方式设定
            *   使用传入顺序进行排列
            *   按字数、回答时间、评论数、赞同数进行公式排列
            *   补记：该功能应当在排版模块中完成，不应在电子书类中进行
        *   首页图片
        *   封面图片
    *   所使用方法
        *   创建基本文件
            *   设置一个固定函数即可
                *   mimetype
                *   META*INF/container.xml
        *   可拓展文件输出
            *   每生成一个文件，即向其传输一个消息
            *   根据消息进行文件的增添处理
            *   可用类进行生成
            *   共两个
                *   OEBPS/toc.ncx
                *   OEBPS/content.opf
                    *   可以添加一个设定基本信息的方法
                        *   比如
                            *   出版社
                            *   出品人
                            *   出版日期
                            *   so on
        *   答案内容生成
            *   答案提取
                *   由数据库中获取
                *   或者由网络获取
                    *   专栏文章
            *   答案处理
                *   转为答案类?
            *   图片下载
            *   答案生成
    """
    

