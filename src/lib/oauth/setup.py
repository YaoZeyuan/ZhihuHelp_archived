#!/usr/bin/env python
# coding=utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import zhihu_oauth

setup(
    name='zhihu_oauth',
    keywords=['zhihu', 'network', 'http', 'OAuth', 'JSON'],
    version=zhihu_oauth.__version__,
    packages=['zhihu_oauth', 'zhihu_oauth.oauth', 'zhihu_oauth.zhcls'],
    url='https://github.com/7sDream/zhihu-oauth',
    license='MIT',
    author='7sDream',
    author_email='7seconddream@gmail.com',
    description='尝试解析出知乎官方未开放的 OAuth2 接口，并提供优雅的使用方式，'
                '作为 zhihu-py3 项目的替代者',
    install_requires=[
        'requests',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
