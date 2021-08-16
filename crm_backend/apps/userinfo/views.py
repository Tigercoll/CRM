from rest_framework.views import APIView
from utils import status_code,response_format
from .serializers import UserInfoSerializers
from .models import UserInfo
from rbac.models import UserRoleRelation
from base.pagination import MyPagination
import datetime
from django.db.models import Q
# Create your views here.


class UserInfoListView(APIView):

    def get(self,request,*args,**kwargs):
        user_query = request.GET.get('q','')
        p = MyPagination()
        if not user_query:
            user_obj = UserInfo.objects.all().order_by('id')
        else:
            user_obj = UserInfo.objects.filter(Q(user_name__contains=user_query)|Q(user_email__contains=user_query)).order_by('id')
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
        print(ser.errors)
        return response_format.render_data(status_code.FAILED_2_ADD,'',ser.errors)

class UserinfoView(APIView):
    def get(self,request,pk):
        user = UserInfo.objects.get(pk=pk)
        if not user:
            return response_format.render_data(status_code.PARAMETER_ERROR,'',msg='参数错误')
        return response_format.render_data(status_code.OK, user.to_dict(), '获取单条用户信息成功')

    def put(self,request,pk):
        user = UserInfo.objects.get(pk=pk)
        if not user:
            return response_format.render_data(status_code.PARAMETER_ERROR, '', msg='参数错误')
        data = request.data
        try:
            for k,v in data.items():
                if hasattr(user,k):
                    print(k,v)
                    setattr(user,k,v)

            user.save()
            UserRoleRelation.add_user_role(pk,data.get('roles_id'))
            return response_format.render_data(status_code.OK,user.to_dict(),'修改成功')
        except Exception as e:
            return response_format.render_data(status_code.FAILED_2_UPDATE,'','%s'%e)

    def delete(self,request,pk):
        user = UserInfo.objects.get(pk=pk)
        if not user:
            return response_format.render_data(status_code.PARAMETER_ERROR, '', msg='参数错误')
        # 2为删除
        user.user_status=2
        user.save()
        return response_format.render_data(status_code.OK,'' ,'删除成功')


class UserInfoAll(APIView):
    def get(self,request):
        salesman_list = UserInfo.get_salesman_list()
        return response_format.render_data(status_code.OK,salesman_list,'获取成功')

