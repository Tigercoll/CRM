from django.db import models
from userinfo.models import UserInfo
# Create your models here.

class Customer(models.Model):



    customer_id = models.IntegerField(verbose_name='客户编号',unique=True)
    customer_name = models.CharField(verbose_name='客户名称',max_length=128)
    customer_desc = models.CharField(verbose_name='客户描述',max_length=128,null=True,blank=True)
    salesman = models.IntegerField(verbose_name='销售人员',null=True,blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True,null=True,blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间',auto_now=True,null=True,blank=True)
    customer_status = models.IntegerField(verbose_name='客户状态',default=1)
    # 联系人   一对多
    @property
    def customer_linkman(self):
        linkman_list = []
        if not hasattr(self,'_linkman_obj'):
            self._linkman_obj = LinkMan.objects.filter(customer_id=self.id)
        for linkman in self._linkman_obj:
            linkman_list.append(linkman.to_dict())
        return  linkman_list

    class Meta:
        db_table = 't_customer'

    def salesman_obj(self):
        if not hasattr(self,'_salesman'):
            self._salesman = UserInfo.objects.filter(id=self.salesman).first()
        return self._salesman

    def salesman_name(self,id):
        salesman_obj = UserInfo.objects.filter(id = id).first()
        if not salesman_obj:
            return ''
        return salesman_obj.user_name



class LinkMan(models.Model):
    gender_list=(
        (1,'男'),
        (2,'女'),
        (3,'其他')
    )
    name = models.CharField(max_length=32,verbose_name='联系人名称')
    phone = models.CharField(max_length=16,verbose_name='手机号',null=True,blank=True)
    gender = models.IntegerField(choices=gender_list,verbose_name='性别',default=3)
    QQ = models.CharField(max_length=32,verbose_name='QQ',null=True,blank=True)
    likes = models.CharField(max_length=64,verbose_name='喜好',null=True,blank=True)
    remark = models.CharField(max_length=128,verbose_name='备注',null=True,blank=True)
    customer_id = models.IntegerField(verbose_name='客户id',null=True,blank=True)
    position = models.CharField(max_length=32,verbose_name='职务',default='')

    def to_dict(self):
        return {
            'name':self.name,
            'phone ':self.phone ,
            'QQ ':self.QQ ,
            'likes':self.likes,
            'remark ':self.remark ,
            'customer_id':self.customer_id,
            'position':self.position,
            'gender':self.get_gender_display()
        }

    class Meta:
        db_table = 't_linkman'