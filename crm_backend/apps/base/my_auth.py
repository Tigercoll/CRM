# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：    my_auth
   Description :
   Author :        tiger
   date :          2021/7/3 下午3:41
-------------------------------------------------
"""
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from utils import jwt_token,status_code
from userinfo.models import UserInfo
from rest_framework import status
class MyAuth(BaseAuthentication):
    def authenticate(self,request):
        token = request.META.get('HTTP_AUTHORIZATION')
        jwt = jwt_token.JwtToken()
        data = jwt.check_token(token)
        if not data:
            raise AuthenticationFailed({
                'code':status_code.AUTH_FAIL,
                'data':'',
                'msg':'认证失败'
            },status.HTTP_401_UNAUTHORIZED)
        user_id = data.get('user_id')
        user = UserInfo.objects.filter(id = user_id).first()
        if not user:
            raise AuthenticationFailed({
                'code': status_code.AUTH_FAIL,
                'data': '',
                'msg': '认证失败'
            },status.HTTP_401_UNAUTHORIZED)
        return (user,None)