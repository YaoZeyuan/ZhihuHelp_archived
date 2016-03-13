# -*- coding: utf-8 -*-
class Type(object):
    answer = 'answer'
    question = 'question'
    topic = 'topic'
    collection = 'collection'
    author = 'author'
    column = 'column'
    article = 'article'

    topic_index = 'topic_index'
    collection_index = 'collection_index'

    author_info = 'author_info'
    collection_info = 'collection_info'
    topic_info = 'topic_info'
    column_info = 'column_info'

    question_answer_type_list = ['answer', 'question']
    article_type_list = ['article', 'column', ]
    question_type_list = ['answer', 'question', 'author', 'collection', 'topic', ]
    type_list = question_type_list + article_type_list  # 文章必须放在专栏之前（否则检测类别的时候就一律检测为专栏了）
    info_table = {
        column: column_info,
        author: author_info,
        collection: collection_info,
        topic: topic_info,
    }
    pass
