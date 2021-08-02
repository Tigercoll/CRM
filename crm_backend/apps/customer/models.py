from django.db import models

# Create your models here.

class Customer(models.Model):
    hospital_code= models.CharField(max_length=32,verbose_name='医院编码')
    hospital_name= models.CharField(max_length=32,verbose_name='医院名称')
    hospital_contacts = models.CharField(max_length=32,verbose_name='医院联系人',null=True,blank=True)
    hospital_lis = models.CharField(max_length=32,verbose_name='医院lis厂商')
    salesman = models.IntegerField(verbose_name='业务员',default=None,null=True,blank=True)
    use_type = models.CharField(verbose_name='状态',max_length=32)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')

    class Meta:
        db_table = 't_customer'

class CustomerDetail(models.Model):
    '''扩展，到时候再加'''
    pass