import httpLib

import cookielib
cookieJarInMemory = cookielib.CookieJar();
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJarInMemory));
urllib2.install_opener(opener);

def Login(account='', password=''):
    if httpLib.openUrl('www.zhihu.com') == '':
        return oldCookie(account='');
    else:
          LoginData   =   urllib.quote('{0}&email={1}&password={2}'.format(xsrf,UserID,UserPassword)+'&rememberme=y',safe='=&')#编码Post请求
          request     =   urllib2.Request(url='http://www.zhihu.com/login',data=LoginData,headers=header)

