# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：    pagination
   Description :
   Author :        tiger
   date :          2021/7/8 上午8:48
-------------------------------------------------
"""

from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    # 分页长度
    page_size = 1
    # 分页参数 ?size=2 来改变分页长度
    page_size_query_param = 'size'
    # 最大分页长度
    max_page_size = 100
    # Client can control the page using this query parameter.
    page_query_param = 'page'
    invalid_page_message = ('参数错误')