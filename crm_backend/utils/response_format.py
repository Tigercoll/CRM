# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：    response_format
   Description :
   Author :        tiger
   date :          2021/7/3 上午12:04
-------------------------------------------------
"""
from rest_framework.response import Response
def render_data(code,data,msg):
    return Response({
        'code':code,
        'data':data,
        'msg':msg
    } )