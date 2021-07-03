# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：    serializers
   Description :
   Author :        tiger
   date :          2021/7/2 下午5:08
-------------------------------------------------
"""
from rest_framework import serializers
from userinfo.models import *

class LoginSerializer(serializers.ModelSerializer):



    class Meta:
        model = UserInfo
        fields = ['user_name','user_pwd']