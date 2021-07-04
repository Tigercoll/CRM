# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：    serializers
   Description :
   Author :        tiger
   date :          2021/7/3 下午10:52
-------------------------------------------------
"""
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import *
class PermissionSerializers(serializers.ModelSerializer):

    def validate(self, attrs):
        permission_level = attrs.get('permission_level')
        if permission_level>2:
            raise ValidationError({'permission_level':'权限等级不得大于3级'})
        return attrs

    class Meta:
        model = Permissions
        fields='__all__'

class RoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields='__all__'