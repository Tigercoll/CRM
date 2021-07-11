# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：    serializers
   Description :
   Author :        tiger
   date :          2021/7/8 上午8:43
-------------------------------------------------
"""

from rest_framework import serializers
from .models import UserInfo
from utils import status_code

class UserInfoSerializers(serializers.ModelSerializer):
    user_status = serializers.SerializerMethodField(read_only=True)
    user_pwd = serializers.CharField(write_only=True)
    user_pwd_r = serializers.CharField(write_only=True)
    class Meta:
        model = UserInfo
        fields = ['id','user_name','user_email','create_time','user_status','user_pwd','user_pwd_r']

    def get_user_status(self,obj):
        return {'id':obj.user_status,
               'status':obj.get_user_status_display()}

    def validate(self,attrs):
        user_pwd = attrs.get('user_pwd')
        user_pwd_r = attrs.pop('user_pwd_r')
        if user_pwd !=user_pwd_r:
            raise serializers.ValidationError('两次密码不一致')
        return attrs