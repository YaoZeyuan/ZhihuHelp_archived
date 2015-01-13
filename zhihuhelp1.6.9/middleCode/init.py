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
        if os.path.isfile('./zhihuDB.db'):
            self.conn              = sqlite3.connect("./zhihuDB.db")
            self.conn.text_factory = str
        else:
            self.conn              = sqlite3.connect("./zhihuDB.db")
            self.conn.text_factory = str
            cursor                 = self.conn.cursor()
            #没有数据库就新建一个出来
            cursor.execute("""create table VarPickle(Var varchar(255), Pickle varchar(50000), primary key (Var))""")
            cursor.execute("""create table AnswerContent( 
                            authorID            varchar(255)    not Null, 
                            authorSign          varchar(2000)   not Null,
                            authorLogo          varchar(255)    not Null,
                            authorName          varchar(255)    not Null,
        
                            answerAgreeCount    int(8)          not Null, 
                            answerContent       longtext        not Null, 
                            questionID          int(8)          not Null,
                            answerID            int(8)          not Null,
                            commitDate          date            not Null,
                            updateDate          date            not Null,
                            answerCommentCount  int(8)          not Null,
                            noRecordFlag        int(1)          not Null,
                            
                            answerHref          varchar(255)    not Null,
                            primary key(answerHref))""")
            
            cursor.execute("""create table QuestionInfo( 
                            questionID           int(8)         not Null,
                            questionCommentCount int(8)         not Null, 
                            questionFollowCount  int(8)         not Null,
                            questionAnswerCount  int(8)         not Null,
                            questionViewCount    int(8)         not Null,
                            questionTitle        varchar(200)   not Null, 
                            questionDesc         longtext       not Null, 
                            questionCollapsedAnswerCount int(8) not Null,

                            primary key(questionID))""")
            
            u'''
            cursor.execute("""
                            create  table   CollectionIndex(
                            collectionID        varchar(50)     not Null,
                            questionHref        varchar(255)    not Null,
                            primary key(CollectionID, questionHref))""")#负责永久保存收藏夹链接，防止丢收藏
            cursor.execute("""
                            CREATE TABLE IDInfo (
                            iDLogoAdress        varchar(255)    default "http://p1.zhimg.com/da/8e/da8e974dc_m.jpg",
                            ID                  varchar(255)    not Null,
                            sign                varchar(255)    default '',
                            name                varchar(255)    default '',
                            ask                 varchar(255)    default '',
                            answer              int             default 0,
                            post                int             default 0,
                            collect             int             default 0,
                            edit                int             default 0,
                            agree               int             default 0,
                            thanks              int             default 0,
                            followee            int             default 0,
                            follower            int             default 0,
                            watched             int             default 0,
                            primary key(ID))""")#负责保存ID信息
            cursor.execute("""
                            create table CollectionInfo(
                            collectionID        varchar(50)     not Null,
                            title               varchar(255),
                            description         varchar(1000),
                            authorName          varchar(255),
                            authorID            varchar(255),
                            authorSign          varchar(255),
                            followerCount       int(20)         not Null,
                            primary key(CollectionID))""")#负责保存收藏夹信息
            cursor.execute("""create table TopicInfo (
                            title               varchar(255),
                            adress              varchar(255),
                            logoAddress         varchar(255),
                            description         varchar(3000),
                            topicID             varchar(50),
                            primary key (TopicID))""")#负责保存话题信息
            '''
            self.conn.commit()
