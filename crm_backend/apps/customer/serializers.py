# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：    serializers
   Description :
   Author :        tiger
   date :          2021/7/27 下午2:49
-------------------------------------------------
"""
from rest_framework import serializers
from .models import Customer,LinkMan


class CustomerSerializers(serializers.ModelSerializer):
    salesman_name = serializers.SerializerMethodField(required=False)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'salesman_name': {'read_only': True},
                        }
    def get_salesman_name(self,obj):
        return obj.salesman_name(obj.salesman)


class CustomerSearchSerializers(serializers.Serializer):
    customer_id = serializers.IntegerField()
    customer_name = serializers.CharField()



class LinkmanSerializers(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    gender_name = serializers.SerializerMethodField()
    class Meta:
        model = LinkMan
        fields = '__all__'
        extra_kwargs = {
            'customer_name': {'read_only': True},
            'gender_name': {'read_only': True},
        }

    def get_customer_name(self,obj):

        if not obj.customer:
            return ''
        return obj.customer.customer_name

    # 获取性别
    def get_gender_name(self,obj):
        return obj.get_gender_display()



