from rest_framework.views import APIView

import userinfo.models
from .serializers import CustomerSerializers,LinkmanSerializers,CustomerSearchSerializers
from .models import Customer,LinkMan
from utils import status_code,response_format
from base.pagination import MyPagination
from django.db.models import Q
from django.db import transaction
from userinfo.models import UserInfo
# Create your views here.

class CustomerListView(APIView):

    def get(self,request):
        q = request.GET.get('q','')
        if not  q:
            customer_obj = Customer.objects.filter().order_by('id')
        else:
            salesman_list = UserInfo.objects.filter(user_name__contains=q).values_list('id')
            customer_obj = Customer.objects.filter(Q(customer_name=q)|Q(customer_desc=q)|Q(salesman__in=salesman_list)).order_by('id')
        p = MyPagination()
        customer_list_obj = p.paginate_queryset(customer_obj,request)
        ser = CustomerSerializers(many=True,instance=customer_list_obj)
        data = {
            'total':customer_obj.count(),
            'page':p.page.number,
            'customer_list':ser.data
        }
        return  response_format.render_data(status_code.OK, data,'获取成功')

    def post(self,request):
        data = request.data
        ser = CustomerSerializers(data=data)
        if ser.is_valid():
            ser.save()
            return response_format.render_data(status_code.OK,ser.data,'添加成功')
        return response_format.render_data(status_code.FAILED_2_ADD,ser.errors,'添加失败')

class CustomerView(APIView):
    authentication_classes = []
    def get(self,request,pk):
        customer_obj = Customer.objects.filter(id=pk).first()
        ser = CustomerSerializers(instance=customer_obj,many=False)
        return response_format.render_data(status_code.OK,ser.data,msg='获取成功')

    def put(self,request,pk):
        data  = request.data
        customer_obj = Customer.objects.filter(id=pk).first()
        ser = CustomerSerializers(instance=customer_obj,data=data)
        if ser.is_valid():
            ser.save()
            return response_format.render_data(status_code.OK, ser.data, '更新成功')
        return response_format.render_data(status_code.FAILED_2_ADD, ser.errors, '更新失败')

    def delete(self,request,pk):
        customer_obj = Customer.objects.filter(id=pk).first()
        if not customer_obj:
            return response_format.render_data(status_code.FAILED_2_DELETE, '', '删除失败')
        customer_obj.delete()
        return response_format.render_data(status_code.OK, '', '删除成功')
from django.db.models import CharField
from django.db.models.functions import Cast
class CustomerListSearch(APIView):
    def get(self,request):
        kw = request.GET.get('kw')
        if not kw:
            customer_list_obj = Customer.objects.all()
        else:
            customer_list_obj = Customer.objects.annotate(as_customer_id=Cast('customer_id',CharField())).filter(Q(customer_name__contains=kw)|Q(as_customer_id__contains=kw))
        ser = CustomerSearchSerializers(instance=customer_list_obj,many=True)
        return response_format.render_data(status_code.OK,ser.data,'获取成功')



class LinkmanListView(APIView):
    def get(self,request):
        q = request.GET.get('q')
        if not q:
            linkman_obj = LinkMan.objects.all().order_by('-id')
        else:
            customer_id_list = Customer.objects.filter(customer_name__contains=q).values_list('customer_id')
            linkman_obj = LinkMan.objects.filter(Q(name__contains=q)|Q(customer_id__in=customer_id_list)).order_by('-id')
        p = MyPagination()
        linkman_list_obj = p.paginate_queryset(linkman_obj, request)
        ser = LinkmanSerializers(instance=linkman_list_obj,many=True)
        data = {
            'total': linkman_obj.count(),
            'page': p.page.number,
            'linkman_list': ser.data
        }
        return response_format.render_data(status_code.OK,data,'获取成功')

    def post(self,request):
        data = request.data
        ser = LinkmanSerializers(data=data)
        if ser.is_valid():
            ser.save()
            return response_format.render_data(status_code.OK,ser.data,'添加成功')
        return response_format.render_data(status_code.FAILED_2_ADD,ser.errors,'添加失败')


class LinkmanView(APIView):
    def get(self,request,pk):
        linkman_obj = LinkMan.objects.filter(id=pk).first()
        if not linkman_obj:
            return response_format.render_data(status_code.PARAMETER_ERROR,'','参数错误')
        ser = LinkmanSerializers(instance=linkman_obj,many=False)
        return response_format.render_data(status_code.OK, ser.data, '获取成功')

    def put(self,request,pk):
        linkman_obj = LinkMan.objects.filter(id=pk).first()
        if not linkman_obj:
            return  response_format.render_data(status_code.PARAMETER_ERROR, '', '参数错误')
        data = request.data
        print(data)
        ser = LinkmanSerializers(instance=linkman_obj,data=data)
        if ser.is_valid():
            ser.save()
            return response_format.render_data(status_code.OK, ser.data, '修改成功')
        return response_format.render_data(status_code.FAILED_2_UPDATE, ser.errors, '修改失败')
    def delete(self,request,pk):
        linkman_obj = LinkMan.objects.filter(id=pk).first()
        if not linkman_obj:
            return response_format.render_data(status_code.PARAMETER_ERROR, '', '参数错误')
        try:
            linkman_obj.delete()
            return response_format.render_data(status_code.OK, '', '删除成功')
        except Exception as e:
            return response_format.render_data(status_code.FAILED_2_DELETE, e, '删除失败')