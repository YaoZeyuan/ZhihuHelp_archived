# -*- coding: utf-8 -*-
import os
import sqlite3
class Init(object):
    def __init__(self):
        self.initDataBase()
        self.cursor = self.conn.cursor()

    def getConn(self):
        return self.conn

    def getCursor(self):
        return self.cursor

    def initDataBase(self):
        databaseFile = r'./zhihuDB.db'
        if os.path.isfile(databaseFile):
            self.conn              = sqlite3.connect(databaseFile)
            self.conn.text_factory = str
        else:
            self.conn              = sqlite3.connect(databaseFile)
            self.conn.text_factory = str
            cursor                 = self.conn.cursor()
            #没有数据库就新建一个出来
            cursor.execute("""create table VarPickle(Var varchar(255), Pickle varchar(50000), primary key (Var))""")
            cursor.execute("""create table LoginRecord(
                    account     varchar(255)    default '',
                    password    varchar(255)    default '', 
                    recordDate  date            default '2000-01-01', 
                    cookieStr   varchar(50000)  default '', 
                    primary key (account))""")
            #核心:答案数据
            cursor.execute("""create table AnswerContent( 
                            authorID            varchar(255)    not Null    default '', 
                            authorSign          varchar(2000)   not Null    default '',
                            authorLogo          varchar(255)    not Null    default '',
                            authorName          varchar(255)    not Null    default '',
        
                            answerAgreeCount    int(8)          not Null    default 0, 
                            answerContent       longtext        not Null    default '', 
                            questionID          int(8)          not Null    default 0,
                            answerID            int(8)          not Null    default 0,
                            commitDate          date            not Null    default '2000-01-01',
                            updateDate          date            not Null    default '2000-01-01',
                            answerCommentCount  int(8)          not Null    default 0,
                            noRecordFlag        int(1)          not Null    default 0,
                            
                            answerHref          varchar(255)    not Null    default '',
                            primary key(answerHref))""")
            #核心:问题信息数据
            cursor.execute("""create table QuestionInfo( 
                            questionIDinQuestionDesc     int(8)       not Null    default 0,
                            questionCommentCount         int(8)       not Null    default 0, 
                            questionFollowCount          int(8)       not Null    default 0,
                            questionAnswerCount          int(8)       not Null    default 0,
                            questionViewCount            int(8)       not Null    default 0,
                            questionTitle                varchar(200) not Null    default '', 
                            questionDesc                 longtext     not Null    default '', 
                            questionCollapsedAnswerCount int(8)       not Null    default 0,

                            primary key(questionIDinQuestionDesc))""")
            #核心:专栏信息数据
            cursor.execute("""create table ColumnInfo(
                            creatorID           varchar(255)    not Null    default '', 
                            creatorHashID       varchar(2000)   not Null    default '',
                            creatorName         varchar(255)    not Null    default '',
                            creatorSign         varchar(255)    not Null    default '',
                            creatorLogo         varchar(255)    not Null    default '',
                            
                            columnID
                            )

                           """)
            #核心:专栏文章数据
            #新数据表
            #收藏夹内容表
            cursor.execute("""
                            create  table       CollectionIndex(
                            collectionID        varchar(50)     not Null,
                            answerHref          varchar(255)    not Null,
                            primary key(collectionID, answerHref))""")#负责永久保存收藏夹链接，防止丢收藏

            #话题内容表
            cursor.execute("""
                            create  table       TopicIndex(
                            topicID             varchar(50)     not Null,
                            answerHref          varchar(255)    not Null,
                            primary key(topicID, answerHref))""")#负责保存话题链接，每次获取话题内容时都要重新更新之

            #圆桌内容表
            cursor.execute("""
                            create  table       TableIndex(
                            tableID             varchar(50)     not Null,
                            answerHref          varchar(255)    not Null,
                            primary key(tableID, answerHref))""")#负责保存圆桌内的答案链接，每次获取圆桌内容时都要重新更新之

            #用户信息表
            cursor.execute("""
                            CREATE TABLE AuthorInfo (
                            authorLogoAddress   varchar(255)    default "http://p1.zhimg.com/da/8e/da8e974dc_m.jpg",
                            authorID            varchar(255)    not Null default 'null',
                            dataID              varchar(255)    default '',
                            sign                varchar(255)    default '',
                            desc                varchar(10000)  default '',
                            name                varchar(255)    default '',
                            ask                 varchar(255)    default '',
                            answer              int             default 0,
                            post                int             default 0,
                            collect             int             default 0,
                            edit                int             default 0,
                            agree               int             default 0,
                            thanks              int             default 0,
                            collected           int             default 0,
                            shared              int             default 0,
                            followee            int             default 0,
                            follower            int             default 0,
                            watched             int             default 0,
                            weiboAddress        varchar(255)    default '',
                            primary key(authorID))""")#负责保存ID信息

            #收藏夹信息表
            cursor.execute("""
                            create table CollectionInfo(
                            collectionID        varchar(50)     not Null,
                            title               varchar(255),
                            description         varchar(1000),
                            authorName          varchar(255),
                            authorID            varchar(255),
                            authorSign          varchar(255),
                            followerCount       int(20)         not Null    default 0,
                            commentCount        int(20)         not Null    default 0,
                            primary key(collectionID))""")#负责保存收藏夹信息

            #话题信息表
            cursor.execute("""create table TopicInfo (
                            title               varchar(255),
                            logoAddress         varchar(255),
                            description         varchar(3000),
                            topicID             varchar(50),
                            followerCount       int(20)         default 0,
                            primary key (topicID))""")#负责保存话题信息

            #圆桌信息表
            cursor.execute("""create table TableInfo (
                            title               varchar(255),
                            logoAddress         varchar(255),
                            description         varchar(3000),
                            activeCount         int             default 0,
                            questionCount       int             default 0,
                            commentCount        int             default 0,
                            tableID             varchar(50),
                            primary key (tableID))""")#负责保存圆桌信息
            
            #专栏内容
            #用户关注问题表
            #用户赞同回答表
            #用户赞同专栏文章表

            self.conn.commit()
