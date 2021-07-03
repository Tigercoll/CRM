from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from utils.response_format import render_data
# Create your views here.

class PermissionsView(APIView):
    def get(self,request,):
        # 获取所有权限

        pass