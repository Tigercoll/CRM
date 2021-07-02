# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：    basemodel
   Description :
   Author :        tiger
   date :          2021/7/1 下午5:07
-------------------------------------------------
"""

from django.db import models

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Set this model as Abstract