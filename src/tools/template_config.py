# -*- coding: utf-8 -*-
from src.tools.path import Path


class TemplateConfig(object):
    template_path = Path.base_path + u'/www/template'
    content_template_path = template_path + u'/content'
    content_info_template_path = content_template_path + u'/info'
    content_question_template_path = content_template_path + u'/question'
    front_page_template_path = template_path + u'/front_page'
    front_page_info_template_path = front_page_template_path + u'/info'

    content_base_uri = template_path + u'/base.html'

    # content
    ##info
    info_author_uri = content_info_template_path + u'/author.html'
    info_comment_uri = content_info_template_path + u'/comment.html'
    info_title_uri = content_info_template_path + u'/title.html'
    ##question
    question_answer_uri = content_question_template_path + u'/answer.html'
    question_question_uri = content_question_template_path + u'/question.html'

    # front_page
    front_page_author_uri = front_page_info_template_path + u'/author.html'
    front_page_collection_uri = front_page_info_template_path + u'/collection.html'
    front_page_column_uri = front_page_info_template_path + u'/column.html'
    front_page_topic_uri = front_page_info_template_path + u'/topic.html'
    front_page_question_uri = front_page_info_template_path + u'/question.html'
    front_page_answer_uri = front_page_info_template_path + u'/answer.html'
    front_page_article_uri = front_page_info_template_path + u'/article.html'

    front_page_base_uri = front_page_template_path + u'/base.html'
