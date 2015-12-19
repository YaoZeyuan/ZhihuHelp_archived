# -*- coding: utf-8 -*-
from .epub_config import EpubConfig


class Base(object):
    def __init__(self):
        self.content = ''
        return

    def get_template(self, template_kind, template_name):
        template_uri = '{}_{}_uri'.format(template_kind, template_name)
        with open(getattr(EpubConfig, template_uri)) as template:
            content = template.read()
        return content

    def get_content(self):
        return self.content
