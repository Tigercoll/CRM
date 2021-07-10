from rest_framework.views import APIView
from utils import status_code,response_format
from .serializers import UserInfoSerializers
from .models import UserInfo
from base.pagination import MyPagination
from django.db.models import Q
# Create your views here.


class UserInfoListView(APIView):

    def get(self,request,*args,**kwargs):

        p = MyPagination()
        user_obj = UserInfo.objects.all()
        user_list_obj = p.paginate_queryset(user_obj,request)

        ser = UserInfoSerializers(instance=user_list_obj,many=True)
        return response_format.render_data(status_code.OK,{'user_list':ser.data,
                                                           'total':user_obj.count(),
                                                            'current_page':p.page.number
        },'获取用户列表成功')

    def post(self,request):
        data = request.data

        ser = UserInfoSerializers(data=data)
        if ser.is_valid():
            ser.save()
            return response_format.render_data(status_code.OK,'','用户添加成功')
        return response_format.render_data(status_code.FAILED_2_ADD,'','用户添加失败')
