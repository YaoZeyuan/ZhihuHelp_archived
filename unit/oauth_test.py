# -*- coding: utf-8 -*-
#   使用该文件测试oauth的使用方法
# 放置于首位
import sys  # 修改默认编码
import os  # 添加系统路径
import json

base_path = unicode(os.path.abspath('.').decode(sys.stdout.encoding))
sys.path.append(base_path + u'/src/lib')
sys.path.append(base_path + u'/src/lib/oauth')

reload(sys)
sys.setdefaultencoding('utf-8') # 强制使用utf-8编码

from zhihu_oauth  import  ZhihuClient

from zhihu_oauth.exception import NeedCaptchaException

client = ZhihuClient()

test_email = 'mengqingxue2014@qq.com'
test_password = '131724qingxue'
token_file = './token.pkl'

if os.path.lexists(token_file):
    client.load_token(token_file)
    print 'load token success'
else:
    try:
        login_result = client.login(test_email, test_password)
    except NeedCaptchaException:
        # 保存验证码并提示输入，重新登录
        print u'登录失败，需要输入验证码'
        with open('a.gif', 'wb') as f:
            f.write(client.get_captcha())
        captcha = raw_input(u'please input captcha:')
        login_result = client.login(test_email, test_password, captcha)
    print 'login result => '
    print login_result
    client.save_token(token_file)
    print 'save token success'

# question
response_file_uri = './question_response.html' # 将json输出到网页中，chrome下按F12选preview能看见浏览器渲染出的json数据结构
question_id = 35005800
question = client.question(question_id)
data = question.pure_data
response_json = json.dumps(data)
response_file = open(response_file_uri, 'w+')
response_file.write(response_json)
print u"数据保存完成"

response_file_uri = './people_response.html' # 将json输出到网页中，chrome下按F12选preview能看见浏览器渲染出的json数据结构
people_id = '404-Page-Not-found'
people = client.people(people_id)
for i in people.answers:
    data = i.pure_data
    response_json = json.dumps(data)
response_file = open(response_file_uri, 'w+')
response_file.write(response_json)
print u"数据保存完成"