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

class UserInfoSerializers(serializers.ModelSerializer):
    user_status = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserInfo
        fields = ['id','user_name','user_email','create_time','user_status']

    def get_user_status(self,obj):
        return {'id':obj.user_status,
               'status':obj.get_user_status_display()}