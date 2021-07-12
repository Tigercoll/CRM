# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：    rendererresponse
   Description :
   Author :        tiger
   date :          2021/7/12 下午12:14
-------------------------------------------------
"""
'''
自定义返回处理
'''

# 导入控制返回的JSON格式的类
from rest_framework.renderers import JSONRenderer


class customrenderer(JSONRenderer):
    # 重构render方法

    def render(self, data, accepted_media_type=None, renderer_context=None):
        print(123)
        if renderer_context:
            print(data)
            if isinstance(data, dict):
                msg = data.pop('msg')
                message = ''
                if isinstance(msg,dict):

                    message=msg.values()

                elif isinstance(msg,list):
                    message=msg[0]
                else:
                    message=msg
                data.update({'msg': message})

            return super().render(data, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)