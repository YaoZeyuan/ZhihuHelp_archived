# coding=utf-8

from __future__ import unicode_literals

# ------- Zhihu API URLs --------

ZHIHU_API_ROOT = 'https://api.zhihu.com'

# ----- 用户相关 -----

# self - GET - 获取自身资料

SELF_DETAIL_URL = ZHIHU_API_ROOT + '/people/self'

# people - GET - 详情

PEOPLE_DETAIL_URL = ZHIHU_API_ROOT + '/people/{}'

# people.answers - GET - 回答

PEOPLE_ANSWERS_URL = PEOPLE_DETAIL_URL + '/answers'

# people.articles - GET - 文章

PEOPLE_ARTICLES_URL = PEOPLE_DETAIL_URL + '/articles'

# people.collections - GET - 收藏夹

PEOPLE_COLLECTIONS_URL = PEOPLE_DETAIL_URL + '/collections_v2'

# people.columns - GET - 专栏

PEOPLE_COLUMNS_URL = PEOPLE_DETAIL_URL + '/columns'

# people.followers - GET - 粉丝
# me.follow - POST - 关注用户

PEOPLE_FOLLOWERS_URL = PEOPLE_DETAIL_URL + '/followers'

# me.follow - DELETE - 取消关注用户

PEOPLE_CANCEL_FOLLOWERS_URL = PEOPLE_FOLLOWERS_URL + '/{}'

# me.following_collections - GET - 关注的收藏夹

PEOPLE_FOLLOWING_COLLECTIONS_URL = PEOPLE_DETAIL_URL + '/following_collections'

# people.following_columns - GET - 关注的专栏

PEOPLE_FOLLOWING_COLUMNS_URL = PEOPLE_DETAIL_URL + '/following_columns'

# people.following_questions - GET - 关注的问题

PEOPLE_FOLLOWING_QUESTIONS_URL = PEOPLE_DETAIL_URL + '/following_questions'

# people.following_topics - GET - 关注的话题

PEOPLE_FOLLOWING_TOPICS_URL = PEOPLE_DETAIL_URL + '/following_topics'

# people.followings - GET - 关注的人

PEOPLE_FOLLOWINGS_URL = PEOPLE_DETAIL_URL + '/followees'

# people.questions - GET - 用户提的问题

PEOPLE_QUESTIONS_URL = PEOPLE_DETAIL_URL + '/questions'

# people.activities - GET - 用户最近动态

PEOPLE_ACTIVITIES_URL = PEOPLE_DETAIL_URL + '/activities'

# ----- 答案相关 -----

# answer - GET - 详情
# me.delete - DELETE - 删除答案

ANSWER_DETAIL_URL = ZHIHU_API_ROOT + '/answers/{}'

# answer.collections - GET - 所在收藏夹

ANSWER_COLLECTIONS_URL = ANSWER_DETAIL_URL + '/collections'

# me.collect - PUT - 加入收藏夹

ANSWER_COLLECT_URL = ANSWER_DETAIL_URL + '/collections_v2'

# answer.comment - GET - 评论

ANSWER_COMMENTS_URL = ANSWER_DETAIL_URL + '/comments'

# answer.voters - GET - 点赞用户
# me.vote - POST - 给答案投票

ANSWER_VOTERS_URL = ANSWER_DETAIL_URL + '/voters'

# me.thanks - POST - 给答案点感谢

ANSWER_THANKS_URL = ANSWER_DETAIL_URL + '/thankers'

# me.thanks - DELETE - 取消感谢

ANSWER_CANCEL_THANKS_URL = ANSWER_THANKS_URL + '/{}'

# me.unhelpful - POST - 没有帮助

ANSWER_UNHELPFUL_URL = ANSWER_DETAIL_URL + '/nothelpers'

# me.unhelpful - DELETE - 取消没有帮助

ANSWER_CANCEL_UNHELPFUL_URL = ANSWER_UNHELPFUL_URL + '/{}'

# ----- 问题相关 -----

# question - GET - 详情

QUESTION_DETAIL_URL = ZHIHU_API_ROOT + '/questions/{}'

# question.answers - GET - 回答

QUESTION_ANSWERS_URL = QUESTION_DETAIL_URL + '/answers'

# question.comments - GET - 评论

QUESTION_COMMENTS_URL = QUESTION_DETAIL_URL + '/comments'

# question.answers - GET - 关注者
# me.follow - POST - 关注问题

QUESTION_FOLLOWERS_URL = QUESTION_DETAIL_URL + '/followers'

# me.follower - DELETE - 取消关注
QUESTION_CANCEL_FOLLOWERS_URL = QUESTION_FOLLOWERS_URL + '/{}'

# question.topics - GET - 所属话题

QUESTION_TOPICS_URL = QUESTION_DETAIL_URL + '/topics'

# ----- 话题相关 -----

# topic - GET - 详情

TOPIC_DETAIL_URL = ZHIHU_API_ROOT + '/topics/{}'

# topic.activities - GET - 动态

TOPIC_ACTIVITIES_URL = TOPIC_DETAIL_URL + '/activities_new'

# topic.best_answers - GET - 精华回答

TOPIC_BEST_ANSWERS_URL = TOPIC_DETAIL_URL + '/best_answers'

# topic.best_answerers - GET - 最佳回答者

TOPIC_BEST_ANSWERERS_URL = TOPIC_DETAIL_URL + '/best_answerers'

# topic.children - GET - 子话题

TOPIC_CHILDREN_URL = TOPIC_DETAIL_URL + '/children'

# topic.children - GET - 父话题

TOPIC_PARENTS_URL = TOPIC_DETAIL_URL + '/parent'

# topic.unanswered_questions - GET - 未回答的问题

TOPIC_UNANSWERED_QUESTION = TOPIC_DETAIL_URL + '/unanswered_questions'

# topic.followers - GET - 关注者
# me.follow - POST - 关注话题

TOPIC_FOLLOWERS_URL = TOPIC_DETAIL_URL + '/followers'

# me.follow - DELETE - 取消关注

TOPIC_CANCEL_FOLLOW_URL = TOPIC_FOLLOWERS_URL + '/{}'

# ----- 收藏夹相关 -----

# collection - GET - 详情
# me.delete - DELETE - 删除收藏夹

COLLECTION_DETAIL_URL = ZHIHU_API_ROOT + '/collections/{}'

# collection.answers - GET - 答案

COLLECTION_ANSWERS_URL = COLLECTION_DETAIL_URL + '/answers'

# collection.comments - GET - 评论

COLLECTION_COMMENTS_URL = COLLECTION_DETAIL_URL + '/comments'

# collection.followers - GET - 粉丝
# me.follow - POST - 关注专栏

COLLECTION_FOLLOWERS_URL = COLLECTION_DETAIL_URL + '/followers'

# me.follow - DELETE - 取消关注

COLLECTION_CANCEL_FOLLOW_URL = COLLECTION_FOLLOWERS_URL + '/{}'

# ----- 专栏相关 -----

# column - GET - 详情

COLUMN_DETAIL_URL = ZHIHU_API_ROOT + '/columns/{}'

# column.articles - GET - 文章

COLUMN_ARTICLES_URL = COLUMN_DETAIL_URL + '/articles'

# column.followers - GET - 关注者
# me.follow - POST - 关注专栏

COLUMN_FOLLOWERS_URL = COLUMN_DETAIL_URL + '/followers'

# me.follow - DELETE - 取消关注

COLUMN_CANCEL_FOLLOW_URL = COLUMN_FOLLOWERS_URL + '/{}'

# ----- 文章相关 -----

# article - GET - 详情
# me.delete - DELETE - 删除文章

ARTICLE_DETAIL_URL = ZHIHU_API_ROOT + '/articles/{}'

# article.vote - GET:  - 获取点赞用户（无效）
# me.vote - POST - 点赞

ARTICLE_VOTE_URL = ARTICLE_DETAIL_URL + '/voters'

# article.comments - GET - 评论

ARTICLE_COMMENTS_URL = ARTICLE_DETAIL_URL + '/comments'

# ----- 评论相关 -----

# me.delete - DELETE - 删除评论

COMMENT_DETAIL_URL = ZHIHU_API_ROOT + '/comments/{}'

# comment.replies - GET - 评论的回复

COMMENT_REPLIES_URL = COMMENT_DETAIL_URL + '/replies'

# comment.conversation - GET - 评论的对话

COMMENT_CONVERSION_URL = COMMENT_DETAIL_URL + '/conversation'

# me.vote - POST - 给评论点赞

COMMENT_VOTE_URL = COMMENT_DETAIL_URL + '/voters'

# me.vote - DELETE - 取消点赞

COMMENT_CANCEL_VOTE_URL = COMMENT_VOTE_URL + '/{}'

# ----- 其他操作 -----

# me.block - POST - 屏蔽用户

BLOCK_PEOPLE_URL = ZHIHU_API_ROOT + '/settings/blocked_users'

# me.block - DELETE - 取消屏蔽用户

CANCEL_BLOCK_PEOPLE_URL = BLOCK_PEOPLE_URL + '/{}'

# me.message - POST - 发送私信

SEND_MESSAGE_URL = ZHIHU_API_ROOT + '/messages'

# me.comment - POST - 发表评论

SEND_COMMENT_URL = ZHIHU_API_ROOT + '/comments'
