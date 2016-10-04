# coding=utf-8

from __future__ import unicode_literals

import os

from ..exception import MyJSONDecodeError, UnexpectedResponseException

try:
    # Py3
    # noinspection PyCompatibility
    from html.parser import HTMLParser
except ImportError:
    # Py2
    # noinspection PyCompatibility,PyUnresolvedReferences
    from HTMLParser import HTMLParser

__all__ = ["INVALID_CHARS", "remove_invalid_char", 'add_serial_number',
           'SimpleHtmlFormatter']


def can_get_from(name, data):
    return name in data and not isinstance(data[name], (dict, list))

DEFAULT_INVALID_CHARS = {':', '*', '?', '"', '<', '>', '|', '\r', '\n'}
EXTRA_CHAR_FOR_FILENAME = {'/', '\\'}


def remove_invalid_char(dirty, invalid_chars=None, for_path=False):
    if invalid_chars is None:
        invalid_chars = set(DEFAULT_INVALID_CHARS)
    else:
        invalid_chars = set(invalid_chars)
        invalid_chars.update(DEFAULT_INVALID_CHARS)
    if not for_path:
        invalid_chars.update(EXTRA_CHAR_FOR_FILENAME)

    return ''.join([c for c in dirty if c not in invalid_chars]).strip()


def add_serial_number(file_path, postfix):
    full_path = file_path + postfix
    if not os.path.isfile(full_path):
        return full_path
    serial = 1
    while os.path.isfile(full_path):
        # noinspection PyUnboundLocalVariable
        try:
            # noinspection PyCompatibility,PyUnresolvedReferences
            serial_str = unicode(str(serial))
        except NameError:
            serial_str = str(serial)
        full_path = file_path + ' - ' + serial_str.rjust(3, '0') + '.' + postfix
        serial += 1
    return full_path


BASE_HTML_HEADER = """<meta name="referrer" content="no-referrer" />
<meta charset="utf-8" />
"""


# TODO: 测试 SimpleHtmlFormatter 对各种文章的兼容性


class SimpleHtmlFormatter(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._level = 0
        self._last = ''
        self._in_code = False
        self._prettified = [BASE_HTML_HEADER]

    def handle_starttag(self, tag, attrs):
        if not self._in_code:
            self._prettified.extend(['\t'] * self._level)
        self._prettified.append('<' + tag)
        for name, value in attrs:
            self._prettified.append(' ' + name + '="' + value + '"')
        self._prettified.append('>')
        if not self._in_code:
            self._prettified.append('\n')
        if tag != 'br' and tag != 'img':
            self._level += 1
        if tag == 'code':
            self._in_code = True
        self._last = tag

    def handle_endtag(self, tag):
        if tag != 'br' and tag != 'img':
            self._level -= 1
        if not self._in_code:
            self._prettified.extend(['\t'] * self._level)
        self._prettified.append('</' + tag + '>')
        if not self._in_code:
            self._prettified.append('\n')
        self._last = tag
        if tag == 'code':
            self._in_code = False

    def handle_startendtag(self, tag, attrs):
        if not self._in_code:
            self._prettified.extend(['\t'] * self._level)
        self._prettified.append('<' + tag)
        for name, value in attrs:
            self._prettified.append(' ' + name + '="' + value + '"')
        self._prettified.append('/>')
        self._last = tag

    def handle_data(self, data):
        if not self._in_code:
            self._prettified.extend(['\t'] * self._level)
            if self._last == 'img':
                self._prettified.append('<br>\n')
                self._prettified.extend(['\t'] * self._level)
        self._prettified.append(data)
        if not self._in_code:
            self._prettified.append('\n')

    def handle_charref(self, name):
        self._prettified.append('&#' + name)

    def handle_entityref(self, name):
        self._prettified.append('&' + name + ';')

    def error(self, message):
        self._prettified = ['error when parser the html file.']

    def prettify(self):
        return ''.join(self._prettified)


class SimpleEnum(set):
    def __getattr__(self, item):
        if item in self:
            return item
        raise AttributeError("No {0} in this enum class.".format(item))


def get_result_or_error(url, res):
    try:
        json_dict = res.json()
        if 'error' in json_dict:
            return False, json_dict['error']['message']
        elif 'success' in json_dict:
            if json_dict['success']:
                return True, ''
            else:
                return False, 'Unknown error'
        else:
            return True, ''
    except (KeyError, MyJSONDecodeError):
        raise UnexpectedResponseException(
            url, res, 'a json contains voting result or error message')


def common_save(path, filename, content, default_filename, invalid_chars):
    filename = filename or default_filename
    filename = remove_invalid_char(filename, invalid_chars)
    filename = filename or 'untitled'

    path = path or '.'
    path = remove_invalid_char(path, invalid_chars, True)
    path = path or '.'

    if not os.path.isdir(path):
        os.makedirs(path)
    full_path = os.path.join(path, filename)
    full_path = add_serial_number(full_path, '.html')
    formatter = SimpleHtmlFormatter()
    formatter.feed(content)
    with open(full_path, 'wb') as f:
        f.write(formatter.prettify().encode('utf-8'))
