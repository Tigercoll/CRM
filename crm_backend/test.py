# # -*- coding: utf-8 -*-
# """
# -------------------------------------------------
#    File Name ：    test
#    Description :
#    Author :        tiger
#    date :          2021/7/20 下午1:57
# -------------------------------------------------
# """
# import pandas as pd
# import pymssql
# #
# import os
# import sys
# import django
#
# # 获取项目的根目录
# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # 添加到系统环境变量
# sys.path.append(base_dir)
# # 加载项目的配置文件
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm_backend.settings")
# # 启动django
# django.setup()
#
# from customer.models import CUstomer
#
# conn = pymssql.connect(host='192.168.20.154',user='lisuser',password='lisuser',database='CZHospitalinfo',charset ='utf8')
#
# sql = """
# select * from hospital
# """
# df = pd.read_sql(sql,conn)
# for i in df.values:
#     CUstomer.objects.create(
#         hospital_code=i[0],
#         hospital_name=i[1],
#         hospital_contacts = i[12],
#         hospital_lis = i[3],
#         use_type = i[9],
#     )



