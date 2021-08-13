from rest_framework.views import APIView
from .serializers import CustomerSerializers
from .models import Customer
from utils import status_code,response_format
from base.pagination import MyPagination
from django.db.models import Q
# Create your views here.

class CustomerListView(APIView):

    def get(self,request):
        q = request.GET.get('q','')
        if not  q:
            customer_obj = Customer.objects.filter().order_by('id')
        else:
            customer_obj = Customer.objects.filter().filter(Q(hospital_code__contains=q)|Q(hospital_name__contains=q)|Q(hospital_contacts__contains=q)).order_by('id')
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