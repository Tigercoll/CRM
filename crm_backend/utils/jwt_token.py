# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：    jwt_token
   Description :
   Author :        tiger
   date :          2021/7/3 上午12:27
-------------------------------------------------
"""
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS
from django.conf import settings

class JwtToken(object):
    def __init__(self):
        self.s = TJWSS(secret_key=settings.SECRET_KEY, expires_in= settings.EXPIRES_TIME)

    def generate_token(self,data):
        token = self.s.dumps(data)
        return token.decode()

    def check_token(self,token):
        try:
            data = self.s.loads(token)
            return data
        except :
            return None
