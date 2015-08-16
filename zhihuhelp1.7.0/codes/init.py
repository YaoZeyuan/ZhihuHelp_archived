# -*- coding: utf-8 -*-
import sqlite3

from   baseClass import *


class Init(object):
    def __init__(self):
        self.initDataBase()
        self.cursor = self.conn.cursor()

    def getConn(self):
        return self.conn

    def getCursor(self):
        return self.cursor

    def initDataBase(self):
        databaseFile = SettingClass.dataBaseFileName
        if os.path.isfile(databaseFile):
            self.conn = sqlite3.connect(databaseFile)
            self.conn.text_factory = str
        else:
            self.conn = sqlite3.connect(databaseFile)
            self.conn.text_factory = str
            cursor = self.conn.cursor()
            # 没有数据库就新建一个出来
            cursor.execute("""CREATE TABLE VarPickle(Var VARCHAR(255), Pickle VARCHAR(50000), PRIMARY KEY (Var))""")
            cursor.execute("""CREATE TABLE LoginRecord(
                    account     VARCHAR(255)    DEFAULT '',
                    password    VARCHAR(255)    DEFAULT '',
                    recordDate  DATE            DEFAULT '2000-01-01',
                    cookieStr   VARCHAR(50000)  DEFAULT '',
                    PRIMARY KEY (account))""")
            # 核心:答案数据
            cursor.execute("""CREATE TABLE AnswerContent(
                            authorID            VARCHAR(255)    NOT NULL    DEFAULT '',
                            authorSign          VARCHAR(2000)   NOT NULL    DEFAULT '',
                            authorLogo          VARCHAR(255)    NOT NULL    DEFAULT '',
                            authorName          VARCHAR(255)    NOT NULL    DEFAULT '',
        
                            answerAgreeCount    INT(8)          NOT NULL    DEFAULT 0,
                            answerContent       longtext        NOT NULL    DEFAULT '',
                            questionID          INT(8)          NOT NULL    DEFAULT 0,
                            answerID            INT(8)          NOT NULL    DEFAULT 0,
                            commitDate          DATE            NOT NULL    DEFAULT '2000-01-01',
                            updateDate          DATE            NOT NULL    DEFAULT '2000-01-01',
                            answerCommentCount  INT(8)          NOT NULL    DEFAULT 0,
                            noRecordFlag        INT(1)          NOT NULL    DEFAULT 0,
                            
                            answerHref          VARCHAR(255)    NOT NULL    DEFAULT '',
                            PRIMARY KEY(answerHref))""")

            cursor.execute(
                """CREATE INDEX idx_AnswerContent ON AnswerContent(authorID, questionID, answerID, answerHref);""")

            # 核心:问题信息数据
            cursor.execute("""CREATE TABLE QuestionInfo(
                            questionIDinQuestionDesc     INT(8)       NOT NULL    DEFAULT 0,
                            questionCommentCount         INT(8)       NOT NULL    DEFAULT 0,
                            questionFollowCount          INT(8)       NOT NULL    DEFAULT 0,
                            questionAnswerCount          INT(8)       NOT NULL    DEFAULT 0,
                            questionViewCount            INT(8)       NOT NULL    DEFAULT 0,
                            questionTitle                VARCHAR(200) NOT NULL    DEFAULT '',
                            questionDesc                 longtext     NOT NULL    DEFAULT '',
                            questionCollapsedAnswerCount INT(8)       NOT NULL    DEFAULT 0,

                            PRIMARY KEY(questionIDinQuestionDesc))""")

            # 新数据表
            # 收藏夹内容表
            cursor.execute("""
                            CREATE  TABLE       CollectionIndex(
                            collectionID        VARCHAR(50)     NOT NULL,
                            answerHref          VARCHAR(255)    NOT NULL,
                            PRIMARY KEY(collectionID, answerHref))""")  # 负责永久保存收藏夹链接，防止丢收藏

            # 话题内容表
            cursor.execute("""
                            CREATE  TABLE       TopicIndex(
                            topicID             VARCHAR(50)     NOT NULL,
                            answerHref          VARCHAR(255)    NOT NULL,
                            PRIMARY KEY(topicID, answerHref))""")  # 负责保存话题链接，每次获取话题内容时都要重新更新之

            # 圆桌内容表
            cursor.execute("""
                            CREATE  TABLE       TableIndex(
                            tableID             VARCHAR(50)     NOT NULL,
                            answerHref          VARCHAR(255)    NOT NULL,
                            PRIMARY KEY(tableID, answerHref))""")  # 负责保存圆桌内的答案链接，每次获取圆桌内容时都要重新更新之

            # 用户信息表
            cursor.execute("""
                            CREATE TABLE AuthorInfo (
                            authorLogoAddress   VARCHAR(255)    DEFAULT "http://p1.zhimg.com/da/8e/da8e974dc_m.jpg",
                            authorID            VARCHAR(255)    NOT NULL DEFAULT 'null',
                            dataID              VARCHAR(255)    DEFAULT '',
                            sign                VARCHAR(255)    DEFAULT '',
                            desc                VARCHAR(10000)  DEFAULT '',
                            name                VARCHAR(255)    DEFAULT '',
                            ask                 VARCHAR(255)    DEFAULT '',
                            answer              INT             DEFAULT 0,
                            post                INT             DEFAULT 0,
                            collect             INT             DEFAULT 0,
                            edit                INT             DEFAULT 0,
                            agree               INT             DEFAULT 0,
                            thanks              INT             DEFAULT 0,
                            collected           INT             DEFAULT 0,
                            shared              INT             DEFAULT 0,
                            followee            INT             DEFAULT 0,
                            follower            INT             DEFAULT 0,
                            watched             INT             DEFAULT 0,
                            weiboAddress        VARCHAR(255)    DEFAULT '',
                            PRIMARY KEY(authorID))""")  # 负责保存ID信息

            # 收藏夹信息表
            cursor.execute("""
                            CREATE TABLE CollectionInfo(
                            collectionID        VARCHAR(50)     NOT NULL,
                            title               VARCHAR(255),
                            description         VARCHAR(1000),
                            authorName          VARCHAR(255),
                            authorID            VARCHAR(255),
                            authorLogo          VARCHAR(255),
                            authorSign          VARCHAR(255),
                            followerCount       INT(20)         NOT NULL    DEFAULT 0,
                            commentCount        INT(20)         NOT NULL    DEFAULT 0,
                            PRIMARY KEY(collectionID))""")  # 负责保存收藏夹信息

            # 话题信息表
            cursor.execute("""CREATE TABLE TopicInfo (
                            title               VARCHAR(255),
                            logoAddress         VARCHAR(255),
                            description         VARCHAR(3000),
                            topicID             VARCHAR(50),
                            followerCount       INT(20)         DEFAULT 0,
                            PRIMARY KEY (topicID))""")  # 负责保存话题信息

            # 圆桌信息表
            cursor.execute("""CREATE TABLE TableInfo (
                            title               VARCHAR(255),
                            logoAddress         VARCHAR(255),
                            description         VARCHAR(3000),
                            activeCount         INT             DEFAULT 0,
                            questionCount       INT             DEFAULT 0,
                            commentCount        INT             DEFAULT 0,
                            tableID             VARCHAR(50),
                            PRIMARY KEY (tableID))""")  # 负责保存圆桌信息

            # 专栏信息
            cursor.execute("""CREATE TABLE ColumnInfo(
                        creatorID       VARCHAR(255)    NOT NULL    DEFAULT '',
                        creatorHash     VARCHAR(255)    NOT NULL    DEFAULT '',
                        creatorSign     VARCHAR(2000)   NOT NULL    DEFAULT '',
                        creatorName     VARCHAR(255)    NOT NULL    DEFAULT '',
                        creatorLogo     VARCHAR(255)    NOT NULL    DEFAULT '',

                        columnID        VARCHAR(255)    NOT NULL    DEFAULT '',
                        columnName      VARCHAR(255)    NOT NULL    DEFAULT '',
                        columnLogo      VARCHAR(255)    NOT NULL    DEFAULT '',
                        description     VARCHAR(3000)   NOT NULL    DEFAULT '',
                        articleCount    INT(20)         NOT NULL    DEFAULT 0,
                        followerCount  INT(20)         NOT NULL    DEFAULT 0,
                        PRIMARY KEY(columnID))""")

            # 专栏内容
            cursor.execute("""CREATE TABLE ArticleContent(
                        authorID        VARCHAR(255)    NOT NULL    DEFAULT '',
                        authorHash      VARCHAR(255)    NOT NULL    DEFAULT '',
                        authorSign      VARCHAR(2000)   NOT NULL    DEFAULT '',
                        authorName      VARCHAR(255)    NOT NULL    DEFAULT '',
                        authorLogo      VARCHAR(255)    NOT NULL    DEFAULT '',

                        columnID        VARCHAR(255)    NOT NULL    DEFAULT '',
                        columnName      VARCHAR(255)    NOT NULL    DEFAULT '',
                        articleID       VARCHAR(255)    NOT NULL    DEFAULT '',
                        articleHref     VARCHAR(255)    NOT NULL    DEFAULT '',
                        title           VARCHAR(2000)   NOT NULL    DEFAULT '',
                        titleImage      VARCHAR(255)    NOT NULL    DEFAULT '',
                        articleContent  longtext        NOT NULL    DEFAULT '',
                        commentCount    INT(20)         NOT NULL    DEFAULT 0,
                        likeCount      INT(20)         NOT NULL    DEFAULT 0,
                        publishedTime   DATE            NOT NULL    DEFAULT '2000-01-01',
                        PRIMARY KEY(articleHref))""")

            cursor.execute("""CREATE INDEX idx_ArticleContent ON ArticleContent(columnID, articleID, authorID);""")

            # 用户活动表
            # 其中，赞同的答案/专栏文章，关注的收藏夹/专栏/话题按时间顺序混排
            # 只记录活动类型，活动目标(比如点赞的答案地址，关注的问题的答案地址)与活动时间和活动者。
            # 其他信息根据活动类型和目标去对应表中查
            # 本表只做记录,不录入内容
            # avtiveType:关注/赞同
            # activeTarget:目标网址,使用时自行提取内容
            # TargetType:专栏/收藏夹/问题/专栏文章/答案
            cursor.execute("""CREATE TABLE userActive(
                        account         VARCHAR(255)    NOT NULL    DEFAULT '',
                        activeTarget    VARCHAR(255)    NOT NULL    DEFAULT '',
                        activeType      VARCHAR(255)    NOT NULL    DEFAULT '',
                        TargetType      vatchar(255)    NOT NULL    DEFAULT '',
                        dateTime        INT(20)         NOT NULL    DEFAULT 0,
                        table_id        INTEGER PRIMARY KEY AUTOINCREMENT
                        )""")

            # 我关注的问题表
            # 这个可以利用用户活动表实现，故不在单独列表


            self.conn.commit()
