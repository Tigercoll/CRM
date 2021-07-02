from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer
from userinfo.models import UserInfo
# Create your views here.

class Login(APIView):
    def get(self,request):
        user = UserInfo.objects.all()
        ser = LoginSerializer(instance=user,many=True)
        return Response(ser.data)
