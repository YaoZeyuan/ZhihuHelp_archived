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
        {
            'title': '{title}',
            'body': open('./www/template/info_page/book_info.html', 'r').read()
        }
    )
    #   type : str
    question_info = base.format(
        {
            'title': '{title}',
            'body': open('./www/template/info_page/question_info.html', 'r').read()
        }
    )

    #   type : str
    question = base.format(
        {
            'title': '{title}',
            'body': open('./www/template/content/question/question.html', 'r').read()
        }
    )

    #   type : str
    answer = open('./www/template/content/question/answer.html', 'r').read()