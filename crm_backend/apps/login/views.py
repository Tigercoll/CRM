
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer
from userinfo.models import UserInfo
from utils import status_code,jwt_token
from utils.response_format import render_data
# Create your views here.

class Login(APIView):
    '''登录'''
    authentication_classes = []
    def get(self,request):
        user = UserInfo.objects.all()
        ser = LoginSerializer(instance=user,many=True)
        return Response(ser.data)


    def post(self,request):
        data = request.data
        user = UserInfo.objects.filter(**data).first()
        if user:
            # 状态保持
            data = {
                'user_id':user.id,
                'user_name':user.user_name
            }
            # 生成token
            jwt = jwt_token.JwtToken()
            token = jwt.generate_token(data)
            return render_data(status_code.OK,{'token':token,'user_id':user.id,'user_name':user.user_name},'登录成功')
        return render_data(status_code.LOGIN_ERROR,'','账号或密码错误')