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
            cursor.execute("""CREATE TABLE Answer(
                            author_id           VARCHAR(255)    NOT NULL    DEFAULT '',
                            author_sign         VARCHAR(2000)   NOT NULL    DEFAULT '',
                            author_logo         VARCHAR(255)    NOT NULL    DEFAULT '',
                            author_name         VARCHAR(255)    NOT NULL    DEFAULT '',

                            agree               INT(8)          NOT NULL    DEFAULT 0,
                            content             longtext        NOT NULL    DEFAULT '',
                            question_id         INT(8)          NOT NULL    DEFAULT 0,
                            answer_id           INT(8)          NOT NULL    DEFAULT 0,
                            commit_date         DATE            NOT NULL    DEFAULT '2000-01-01',
                            edit_date           DATE            NOT NULL    DEFAULT '2000-01-01',
                            comment             INT(8)          NOT NULL    DEFAULT 0,
                            no_record_flag      INT(1)          NOT NULL    DEFAULT 0,

                            href                VARCHAR(255)    NOT NULL    DEFAULT '',
                            PRIMARY KEY(href))""")

            # 核心:问题信息数据
            cursor.execute("""CREATE TABLE Question(
                            question_id     INT(8)       NOT NULL    DEFAULT 0,
                            comment         INT(8)       NOT NULL    DEFAULT 0,
                            views           INT(8)       NOT NULL    DEFAULT 0,
                            answers         INT(8)       NOT NULL    DEFAULT 0,
                            followers       INT(8)       NOT NULL    DEFAULT 0,
                            title           VARCHAR(200) NOT NULL    DEFAULT '',
                            description     longtext     NOT NULL    DEFAULT '',

                            PRIMARY KEY(question_id))""")

            # 新数据表
            # 收藏夹内容表
            cursor.execute("""
                            CREATE  TABLE       CollectionIndex(
                            collection_id       VARCHAR(50)     NOT NULL,
                            href                VARCHAR(255)    NOT NULL,
                            PRIMARY KEY(collectionID, answerHref))""")  # 负责永久保存收藏夹链接，防止丢收藏

            # 话题内容表
            cursor.execute("""
                            CREATE  TABLE       TopicIndex(
                            topic_id      VARCHAR(50)     NOT NULL,
                            href          VARCHAR(255)    NOT NULL,
                            PRIMARY KEY(topicID, answerHref))""")  # 负责保存话题链接，每次获取话题内容时都要重新更新之

            # 圆桌内容表
            cursor.execute("""
                            CREATE  TABLE       TableIndex(
                            table_id      VARCHAR(50)     NOT NULL,
                            href          VARCHAR(255)    NOT NULL,
                            PRIMARY KEY(tableID, answerHref))""")  # 负责保存圆桌内的答案链接，每次获取圆桌内容时都要重新更新之

            # 用户信息表
            cursor.execute("""
                            CREATE TABLE AuthorInfo (
                            logo              VARCHAR(255)    DEFAULT "http://p1.zhimg.com/da/8e/da8e974dc_m.jpg",
                            author_id         VARCHAR(255)    NOT NULL DEFAULT 'null',
                            hash              VARCHAR(255)    DEFAULT '',
                            sign              VARCHAR(255)    DEFAULT '',
                            description       VARCHAR(10000)  DEFAULT '',
                            name              VARCHAR(255)    DEFAULT '',
                            asks              VARCHAR(255)    DEFAULT '',
                            answers           INT             DEFAULT 0,
                            posts             INT             DEFAULT 0,
                            collections       INT             DEFAULT 0,
                            logs              INT             DEFAULT 0,
                            agree             INT             DEFAULT 0,
                            thanks            INT             DEFAULT 0,
                            collected         INT             DEFAULT 0,
                            shared            INT             DEFAULT 0,
                            followee          INT             DEFAULT 0,
                            follower          INT             DEFAULT 0,
                            followed_column   INT             DEFAULT 0,
                            followed_topic    INT             DEFAULT 0,
                            viewed            INT             DEFAULT 0,
                            gender            VARCHAR(255)    DEFAULT '',
                            weibo             VARCHAR(255)    DEFAULT '',
                            PRIMARY KEY(author_id))""")  # 负责保存ID信息

            # 收藏夹信息表
            cursor.execute("""
                            CREATE TABLE CollectionInfo(
                            collection_id       VARCHAR(50)     NOT NULL,
                            title               VARCHAR(255),
                            description         VARCHAR(1000),
                            follower            INT(20)         NOT NULL    DEFAULT 0,
                            comment             INT(20)         NOT NULL    DEFAULT 0,
                            PRIMARY KEY(collection_id))""")  # 负责保存收藏夹信息

            # 话题信息表
            cursor.execute("""CREATE TABLE TopicInfo (
                            title               VARCHAR(255),
                            logo                VARCHAR(255),
                            description         VARCHAR(3000),
                            topic_id            VARCHAR(50),
                            follower            INT(20)         DEFAULT 0,
                            PRIMARY KEY (topic_id))""")  # 负责保存话题信息

            # 圆桌信息表
            cursor.execute("""CREATE TABLE TableInfo (
                            title               VARCHAR(255),
                            logo                VARCHAR(255),
                            description         VARCHAR(3000),
                            active              INT             DEFAULT 0,
                            question            INT             DEFAULT 0,
                            comment             INT             DEFAULT 0,
                            table_id             VARCHAR(50),
                            PRIMARY KEY (table_id))""")  # 负责保存圆桌信息

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
