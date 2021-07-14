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
from rest_framework.exceptions import APIException

from utils import status_code
from .models import *
class PermissionSerializers(serializers.ModelSerializer):

    def validate(self, attrs):
        permission_level = attrs.get('permission_level')
        if permission_level>3:
            raise ValidationError({'permission_level':'权限等级不得大于3级'})

        return attrs

    class Meta:
        model = Permissions
        fields='__all__'

class RoleSerializers(serializers.ModelSerializer):
    role_desc = serializers.CharField()

    def validate_role_name(self,data):
        exists = Roles.has_exists(data)
        if not exists:
            raise APIException({'code':status_code.DUPLICATE_ROLE_NAME,'msg':'角色名重复'})

        return data



    class Meta:
        model = Roles
        fields=['role_name','role_desc']