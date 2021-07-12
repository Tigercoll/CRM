# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：    exception
   Description :
   Author :        tiger
   date :          2021/7/12 上午11:53
-------------------------------------------------
"""
# 自定义异常处理
from rest_framework.views import exception_handler
from rest_framework.views import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if isinstance(exc, APIException):
        response.data=exc.detail
        response.status_code=200
    return response
