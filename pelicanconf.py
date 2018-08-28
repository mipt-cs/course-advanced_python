#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os

AUTHOR = 'Timofey Khirianov'
SITENAME = 'Продвинутое программирование на Python'
SITEURL = 'http://cs.mipt.ru/advanced_python'

PATH = 'content'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'ru'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MENUITEMS = (('Уроки курса', '/'))

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = False
FILENAME_METADATA = '(?P<slug>.*)'
ARTICLE_URL = 'lessons/{slug}.html'
ARTICLE_SAVE_AS = ARTICLE_URL


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = 'themes/the-theme'

ARTICLE_ORDER_BY = 'date'
DISPLAY_CATEGORIES_ON_MENU = False

PLUGIN_PATHS = ['plugins']
PLUGINS = ['pelican_youtube', 'code_include']

STATIC_PATHS = [
    'images',
    'code',
    'jslib',
    'pip'
]

EXTRA_PATH_METADATA = {
    'extra/favicon.png': {'path': 'favicon.png'}
}

extra = os.path.join(os.path.dirname(__file__), 'content', 'extra')
for root, directories, filenames in os.walk(extra):
    for filename in filenames:
        STATIC_PATHS.append(os.path.join(root,filename)[len(extra)-5:])

READERS = {'html': None, 'md': None}
