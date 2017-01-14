# -*- coding: utf-8 -*-
from src.container.data.author import Author
from src.tools.db import DB
from src.tools.match import Match
from src.tools.path import Path


class Article(object):
    u"""
    文章容器
    """
    def __init__(self, data):
        self.article_id = data['article_id']
        self.title = data['title']
        self.updated_time = data['updated_time']
        self.voteup_count = data['voteup_count']
        self.image_url = data['image_url']
        self.column_id = data['column_id']
        self.content = data['content']
        self.comment_count = data['comment_count']
        self.author_id = data['author_id']
        self.author_name = data['author_name']
        self.author_headline = data['author_headline']
        self.author_avatar_url = data['author_avatar_url']
        self.author_gender = data['author_gender']

        self.total_img_size_kb = 0
        self.img_filename_list = []
        return

    def download_img(self):
        from src.container.image_container import ImageContainer
        img_container = ImageContainer()
        img_src_dict = Match.match_img_with_src_dict(self.content)
        self.img_filename_list = []
        for img in img_src_dict:
            src = img_src_dict[img]
            filename = img_container.add(src)
            self.img_filename_list.append(filename)
            self.content = self.content.replace(img, Match.create_img_element_with_file_name(filename))

        #   下载文章封面图像
        filename = img_container.add(self.image_url)
        self.img_filename_list.append(filename)
        self.image_url = Match.create_local_img_src(filename)

        #   下载用户头像
        filename = img_container.add(self.author_avatar_url)
        self.img_filename_list.append(filename)
        self.author_avatar_url = Match.create_local_img_src(filename)

        img_container.start_download()

        #   下载完成后，更新图片大小
        for filename in self.img_filename_list:
            self.total_img_size_kb += Path.get_img_size_by_filename_kb(filename)
        return