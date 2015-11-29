# -*- coding: utf-8 -*-
from baseClass import SqlClass, SettingClass
from codes.epubBuilder.image_container import ImageContainer
import re

class Filter(object):
    u"""
    负责在数据库中提取数据和对数据进行处理,返回处理完毕的html信息和所有待下载图片的imgContainer
    """

    def __init__(self, raw_book_info):
        self.raw_info = raw_book_info
        self.imgContainer = ImageContainer()
        self.book = {}
        self.init_book()
        return

    def init_book(self):
        self.book['info'] = ''
        self.book['kind'] = self.raw_info['kind']
        self.book['article_list'] = []
        return

    def get_raw_question_list(self):
        question_list = [SqlClass.wrap('question', x) for x in self.get_result_list(self.raw_info['question'])]
        answer_list = [SqlClass.wrap('answer', x) for x in self.get_result_list(self.raw_info['answer'])]

        def merge_answer_into_question():
            question_dict = {x['question_id']: {'question': x.copy(), 'answer_list': [], 'agree': 0} for x in
                             question_list}
            for answer in answer_list:
                question_dict[answer['question_id']]['answer_list'].append(answer)
            return question_dict.values()

        def add_property(question):
            agree_count = 0
            char_count = 0
            for answer in question['answer_list']:
                answer['char_count'] = len(answer['content'])
                answer['agree_count'] = answer['agree']
                answer['update_date'] = answer['edit_date']
                agree_count += answer['agree']
                char_count += answer['char_count']
            question['answer_count'] = len(question['answer'])
            question['agree_count'] = agree_count
            question['char_count'] = char_count
            return question

        question_list = [add_property(x) for x in merge_answer_into_question()]
        return question_list

    def get_raw_article_list(self):
        def add_property(article):
            article['char_count'] = len(article['content'])
            article['agree_count'] = article['agree']
            article['update_date'] = article['publish_date']
            article['answer_count'] = 1
            return article
        article_list = [SqlClass.wrap('article', x) for x in self.get_result_list(self.raw_info['answer'])]
        article_list = [add_property(x) for x in article_list]
        return article_list

    def get_result_list(self, sql):
        result = SqlClass.cursor.execute(sql).fetchall()
        return result

    def get_book(self):
        self.book['info'] = self.create_info_dict(self.raw_info['kind'], self.raw_info['info'])
        if self.raw_info['kind'] in ['article', 'column']:
            self.book['article_list'] = self.get_raw_question_list()
        else:
            self.book['article_list'] = self.get_raw_article_list()
        return self.book

    def get_image_container(self):
        return self.imgContainer

    def create_info_dict(self, kind, raw):
        info = {}

        def init_property():
            info['base_image_path'] = './image/'
            info['logo_liu_kan_shan'] = './image/kanshan.png'
            return

        def add_css():
            info['markdown_css'] = './markdown.css'
            info['front_css'] = './front.css'
            return

        def add_article_info():
            info['title'] = u'知乎专栏文章集锦'
            info['author_name'] = u'知乎网友'
            return

        def add_answer_info():
            info['title'] = u'知乎回答集锦'
            info['author_name'] = u'知乎网友'
            return

        def add_question_info():
            info['title'] = u'知乎问题集锦'
            info['author_name'] = u'知乎网友'
            return

        def add_topic_info():
            info.update(raw)
            info['logo'] = self.imgContainer.add(raw['logo'])
            return

        def add_collection_info():
            info.update(raw)
            return

        def add_column_info():
            info.update(raw)
            return

        add_customer_info = {'answer': add_answer_info, 'question': add_question_info, 'topic': add_topic_info,
                             'collection': add_collection_info, 'article': add_article_info,
                             'column': add_column_info, }

        init_property()
        add_css()
        add_customer_info[kind]()
        return info

    def create_info_page(self, kind, info_sql):
        with open('./html_template/info/{}.html'.format(kind)) as file:
            template = file.read()
        result = SqlClass.cursor.execute(info_sql).fetchone()
        info = self.create_info_dict(kind, SqlClass.wrap(kind, result))
        return template.format(info)


class HtmlTranslator(object):
    def __init__(self, book, ImageContainer):
        self.book = book
        self.imageContainer = ImageContainer
        self.book_list = []
        return

    def start(self):
        self.pre_process()
        self.split_book()
        page_list = self.create_book()
        return page_list

    def get_image_container(self):
        return self.imageContainer

    def pre_process(self):
        if self.book['kind'] in ['article', 'column']:
            self.sort_article()
        else:
            self.sort_question()
        return

    def sort_article(self):
        article_list = self.book['article_list']
        article_list.sort(key=lambda x: x[SettingClass.ARTICLEORDERBY], reverse=SettingClass.ARTICLEORDERBYDESC)
        return

    def sort_question(self):
        def sort_answer(answer_list):
            answer_list.sort(key=lambda x: x[SettingClass.ANSWERORDERBY], reverse=SettingClass.ANSWERORDERBYDESC)
            return

        article_list = self.book['article_list']
        article_list.sort(key=lambda x: x[SettingClass.ARTICLEORDERBY], reverse=SettingClass.ARTICLEORDERBYDESC)
        for item in self.book['article_list']:
            sort_answer(item['answer_list'])
        return

    def split_book(self):
        article_list = self.book['article_list']

        def split_article():
            package = []
            pack = []
            counter = 0
            for item in article_list:
                if counter < SettingClass.MAXARTICLE:
                    pack.append(item)
                    counter += 1
                else:
                    counter = 0
                    package.append(pack)
                    pack = []
            return package

        def split_answer():
            package = []
            pack = []
            counter = 0
            for item in article_list:
                if counter < SettingClass.MAXANSWER:
                    pack.append(item)
                    counter += item['answer_count']
                else:
                    counter = 0
                    package.append(pack)
                    pack = []
            return package

        if self.book['kind'] in ['article', 'column']:
            article_list = split_article(article_list)
        else:
            article_list = split_answer(article_list)

        if len(article_list) > 1:
            index = 1
            for package in article_list:
                book = self.book.copy()
                book['info']['title'] += '_({})'.format(index)
                book['article_list'] = package
                self.book_list.append(book)
        else:
            self.book_list.append(self.book)
        return

    def create_books(self):
        self.book_list = [self.create_book(x) for x in self.book_list]
        return

    def create_book(self, book):
        def fix_image(content):
            def image_quality(href):
                return

            for img in re.findall(r'<img.*?>', content):
                src = re.search(r'(?<=src=").*?(?=")', img)
                if not src:
                    continue
                else:
                    src = src.group(0)
                    if src.replace(' ', '') == '':
                        continue
                src_download = src
                if 'https' in src_download[:5]:
                    src_download = 'http' + src_download[5:]  # 去除图片中的https
                filename = self.imageContainer.add(src_download)
                content = content.replace('"{}"'.format(src), '"{}"'.format('../images/' + filename))
            return content

        def create_question(question):
            def create_answer(answer):
                with open('./html_template/content/answer.html') as answer_temp:
                    template = answer_temp.read()
                return template.format(**answer)

            answer_content = ''.join([create_answer(answer) for answer in question['article_list']])
            question['answer_content'] = answer_content
            with open('./html_template/content/question.html') as question_temp:
                template = question_temp.read()
            return template.format(**question)

        def create_article(article):
            with open('./html_template/content/article.html') as article_temp:
                template = article_temp.read()
            return template.format(**article)

        page_list = [{'filename': 'info.html', 'content': book['info']}]
        if book['kind'] in ['article', 'column']:
            for article in book['article_list']:
                page_list.append({'filename': article['article_id'] + '.html', 'title': article['title'],
                                  'content': fix_image(create_article(article))})
        else:
            for question in book['article_list']:
                page_list.append({'filename': question['question_id'] + '.html', 'title': question['title'],
                                  'content': fix_image(create_question(question))})
        return page_list
