# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：    serializers
   Description :
   Author :        tiger
   date :          2021/7/3 下午10:52
-------------------------------------------------
"""

from rest_framework import serializers
from .models import *
class PermissionSerializers(serializers.ModelSerializer):

    class Meta:
        model = Permissions
        fields='__all__'
