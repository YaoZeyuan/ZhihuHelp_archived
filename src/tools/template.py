# -*- coding: utf-8 -*-

class Template(object):
    """
    文件模版
    """
    #   type : str
    #   interface : title, body
    base = open('./www/template/base.html', 'r').read()

    #   type : str
    book_info = base.format(
        **{
            'title': '{title}',
            'body': open('./www/template/info_page/book.html', 'r').read()
        }
    )
    #   type : str
    question_info = base.format(
        **{
            'title': '{title}',
            'body': open('./www/template/info_page/question.html', 'r').read()
        }
    )

    #   type : str
    author_info = base.format(
        **{
            'title': '{title}',
            'body': open('./www/template/info_page/author.html', 'r').read()
        }
    )

    #   type : str
    topic_info = base.format(
        **{
            'title': '{title}',
            'body': open('./www/template/info_page/topic.html', 'r').read()
        }
    )

    #   type : str
    collection_info = base.format(
        **{
            'title': '{title}',
            'body': open('./www/template/info_page/collection.html', 'r').read()
        }
    )

    #   type : str
    column_info = base.format(
        **{
            'title': '{title}',
            'body': open('./www/template/info_page/column.html', 'r').read()
        }
    )

    #   type : str
    article_info = base.format(
        **{
            'title': '{title}',
            'body': open('./www/template/info_page/article.html', 'r').read()
        }
    )

    #   type : str
    question = base.format(
        **{
            'title': '{title}',
            'body': open('./www/template/content/question/question.html', 'r').read()
        }
    )

    #   type : str
    answer = open('./www/template/content/question/answer.html', 'r').read()