from django.conf.urls.defaults import *
from zhihuhelp.login.views import index, login, getCaptcha

urlpatterns = patterns("", 
    url(r"^$", index),
    url(r"^getCaptcha$", getCaptcha),
    url(r"^login$", login),   
)

