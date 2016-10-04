# -*- coding: utf-8 -*-
#   使用该文件测试oauth的使用方法
# 放置于首位
import sys  # 修改默认编码
import os  # 添加系统路径

base_path = unicode(os.path.abspath('.').decode(sys.stdout.encoding))
sys.path.append(base_path + u'/src/lib')

reload(sys)
sys.setdefaultencoding('utf-8') # 强制使用utf-8编码

from oauth.zhihu_oauth  import  ZhihuClient

from oauth.zhihu_oauth.exception import NeedCaptchaException

client = ZhihuClient()

try:
    client.login('email_or_phone', 'password')
except NeedCaptchaException:
    # 保存验证码并提示输入，重新登录
    with open('a.gif', 'wb') as f:
        f.write(client.get_captcha())
    captcha = input('please input captcha:')
    client.login('email_or_phone', 'password', captcha)