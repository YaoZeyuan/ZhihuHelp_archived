# -*- coding: utf-8 -*-
from codes.parser.answer import *

content = open('./unit_html/single_answer.html', 'r').read()
parse = ParseAnswer(content)

questionInfoDictList, answerDictList = parse.getInfoDict()

for question in questionInfoDictList:
    BaseClass.printDict(question)

print '=========================='

for answer in answerDictList:
    BaseClass.printDict(answer)
