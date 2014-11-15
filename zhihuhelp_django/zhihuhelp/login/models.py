from django.db import models
from django.contrib import admin

class User(models.Model):
    account   = models.CharField(max_length=150, unique=True)
    password  = models.CharField(max_length=20)
    cookies   = models.CharField(max_length=255, blank=True)
    loginDate = models.DateField(auto_now=True)

admin.site.register(User)
