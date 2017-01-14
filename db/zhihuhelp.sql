
CREATE TABLE `Answer` (
  `answer_id` int(11) NOT NULL , ---- COMMENT '答案id，唯一值',
  `question_id` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '问题id,用于到问题表里连表查询',
  `author_id` varchar(500) NOT NULL DEFAULT 'nimingyonghu' , ---- COMMENT '作者的hash_id',
  `author_name` varchar(500) NOT NULL DEFAULT '匿名用户' , ---- COMMENT '作者名字',
  `author_headline` varchar(500) NOT NULL DEFAULT '' , ---- COMMENT '作者签名档',
  `author_avatar_url` varchar(500) NOT NULL DEFAULT 'http://pic4.zhimg.com/bfcef853fba8140581eeede4ea7a0c33_s.jpg' , ---- COMMENT '作者头像:示例http://pic4.zhimg.com/bfcef853fba8140581eeede4ea7a0c33_s.jpg',
  `author_gender` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '作者性别0:女,1:男,-1:未设置',
  `comment_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '评论数',
  `content` text NOT NULL , ---- COMMENT '答案内容',
  `created_time` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '答案创建时间',
  `updated_time` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '答案更新时间',
  `is_copyable` int(11) NOT NULL DEFAULT '1' , ---- COMMENT '是否允许转载0:不允许,1:允许',
  `thanks_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '感谢数',
  `voteup_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '赞同数',
  PRIMARY KEY (`answer_id`)
) ; ---- ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='答案表，分为answer和author两部分';


CREATE TABLE `Article` (
  `article_id` varchar(100) NOT NULL  , ---- COMMENT '文章id',
  `title` varchar(200) NOT NULL , ---- COMMENT '文章标题',
  `updated_time` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '更新时间戳',
  `voteup_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '赞同数',
  `column_id` varchar(200) NOT NULL , ---- COMMENT '专栏id',
  `image_url` varchar(500) NOT NULL , ---- COMMENT '封面题图',
  `content` text NOT NULL , ---- COMMENT '文章内容(html形式)',
  `comment_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '评论数',

  ----以下同answer中的设置
  `author_id` varchar(500) NOT NULL DEFAULT 'nimingyonghu' , ---- COMMENT '作者的hash_id',
  `author_name` varchar(500) NOT NULL DEFAULT '匿名用户' , ---- COMMENT '作者名字',
  `author_headline` varchar(500) NOT NULL DEFAULT '' , ---- COMMENT '作者签名档',
  `author_avatar_url` varchar(500) NOT NULL DEFAULT 'http://pic4.zhimg.com/bfcef853fba8140581eeede4ea7a0c33_s.jpg' , ---- COMMENT '作者头像:示例http://pic4.zhimg.com/bfcef853fba8140581eeede4ea7a0c33_s.jpg',
  `author_gender` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '作者性别0:女,1:男,-1:未设置',
  PRIMARY KEY (`article_id`)
) ; ---- ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `Author` (
  `author_id` varchar(100) NOT NULL DEFAULT '' , ---- COMMENT 'hash_id',
  `author_page_id` int(11) NOT NULL , ---- COMMENT '用户主页id.随时可能会更换',
  `answer_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '回答数',
  `articles_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '文章数',
  `avatar_url` varchar(500) NOT NULL DEFAULT 'http://pic4.zhimg.com/bfcef853fba8140581eeede4ea7a0c33_s.jpg' , ---- COMMENT '头像，示例:http://pic4.zhimg.com/bfcef853fba8140581eeede4ea7a0c33_s.jpg',
  `columns_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '专栏数',
  `description` varchar(500) NOT NULL DEFAULT '' , ---- COMMENT '描述',
  `favorite_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '创建的收藏夹数',
  `favorited_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '收藏数',
  `follower_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '粉丝数',
  `following_columns_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '关注专栏数',
  `following_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '关注人数',
  `following_question_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '关注问题数',
  `following_topic_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '关注话题数',
  `gender` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '性别=>0:女,1:男',
  `headline` varchar(500) NOT NULL DEFAULT '' , ---- COMMENT '签名档',
  `name` varchar(500) NOT NULL DEFAULT '' , ---- COMMENT '用户名',
  `question_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '提问数',
  `shared_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '被分享数',
  `is_bind_sina` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '是否绑定新浪微博',
  `thanked_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '被感谢数',
  `sina_weibo_name` varchar(500) NOT NULL DEFAULT '' , ---- COMMENT '新浪微博用户名',
  `sina_weibo_url` varchar(500) NOT NULL DEFAULT '' , ---- COMMENT '新浪微博地址',
  `voteup_count` int(11) NOT NULL DEFAULT '0',  ---- COMMENT '被赞同数'
  PRIMARY KEY (`author_id`)
) ; ---- ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `Collection` (
  `collection_id` int(11) NOT NULL , ---- COMMENT '收藏夹id',
  `answer_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '答案数',
  `comment_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '评论数',
  `created_time` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '创建时间',
  `follower_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '关注人数',
  `description` varchar(200) NOT NULL DEFAULT '' , ---- COMMENT '描述',
  `title` varchar(200) NOT NULL DEFAULT '' , ---- COMMENT '收藏夹名',
  `updated_time` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '最后更新时间',
  `creator_id` varchar(200) NOT NULL DEFAULT '' , ---- COMMENT '创建者的hashid',
  `creator_name` varchar(200) NOT NULL DEFAULT '' , ---- COMMENT '创建者名字',
  `creator_headline` varchar(200) NOT NULL DEFAULT '' , ---- COMMENT '创建者签名档',
  `creator_avatar_url` varchar(200) NOT NULL DEFAULT '' , ---- COMMENT '创建者头像',
  `collected_answer_id_list` text NOT NULL,  ---- COMMENT '收藏夹下以逗号分隔的答案id列表'
  PRIMARY KEY (`collection_id`)
) ; ---- ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `Column` (
  `column_id` varchar(200) NOT NULL , ---- COMMENT '专栏id',
  `title` varchar(200) NOT NULL , ---- COMMENT '专栏名',
  `article_count` int(11) NOT NULL , ---- COMMENT '专栏内文章数',
  `follower_count` int(11) NOT NULL , ---- COMMENT '关注人数',
  `description` varchar(5000) NOT NULL , ---- COMMENT '专栏描述',
  `image_url` varchar(5000) NOT NULL , ---- COMMENT '专栏封面',
  PRIMARY KEY (`column_id`)
) ; ---- ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `Question` (
  `question_id` int(11) NOT NULL , ---- COMMENT '问题id',
  `answer_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '回答数',
  `comment_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '评论数',
  `follower_count` int(11) NOT NULL DEFAULT '0' , ---- COMMENT '关注数',
  `title` varchar(200) NOT NULL DEFAULT '' , ---- COMMENT '问题',
  `detail` varchar(200) NOT NULL DEFAULT '' , ---- COMMENT '问题详情',
  `updated_time` int(11) NOT NULL DEFAULT '0',  ---- COMMENT '更新时间'
  PRIMARY KEY (`question_id`)
) ; ---- ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `Topic` (
  `topic_id` int(11) NOT NULL , ---- COMMENT '话题id',
  `avatar_url` varchar(300) NOT NULL , ---- COMMENT '话题图片',
  `best_answerers_count` int(11) NOT NULL , ---- COMMENT '最佳回答的作者数',
  `best_answers_count` int(11) NOT NULL , ---- COMMENT '最佳回答数',
  `excerpt` text NOT NULL , ---- COMMENT '简介(无html标签)',
  `followers_count` int(11) NOT NULL , ---- COMMENT '关注者人数',
  `introduction` text NOT NULL , ---- COMMENT '介绍，含html标签',
  `name` varchar(200) NOT NULL , ---- COMMENT '话题名称',
  `questions_count` int(11) NOT NULL , ---- COMMENT '话题下的问题数量',
  `unanswered_count` int(11) NOT NULL , ---- COMMENT '话题下等待回答的问题数量',
  `best_answer_id_list` text NOT NULL,  ---- COMMENT '逗号分隔形式的话题下精华答案id列表'
  PRIMARY KEY (`topic_id`)
) ; ---- ENGINE=InnoDB DEFAULT CHARSET=utf8;
