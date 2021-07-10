from django.db import models
from base.basemodel import BaseModel
from rbac.models import Roles,UserRoleRelation
import datetime
# Create your models here.

class UserInfo(BaseModel):
    '''用户基础模块'''

    status = (
        (1,'启用'),
        (2,'删除'),
    )
    user_name = models.CharField(max_length=32,verbose_name='用户名',unique=True)
    user_pwd = models.CharField(max_length=64,verbose_name='密码')
    user_email = models.CharField(max_length=32,verbose_name='邮箱')
    user_status = models.IntegerField(choices=status,verbose_name='用户状态',default=1)
    last_login_time = models.DateTimeField(verbose_name='最后一次登录时间',null=True)




    # 用户一对一关联扩展模块
    @property
    def userprofile(self):
        if not hasattr(self,'_userprofile'):
            self._userprofile,_ = UserProfile.objects.get_or_create(id=self.id)
        return self._userprofile

    # 重新定义表名称
    class Meta:
        db_table = 't_userinfo'
    def __str__(self):
        return '%s'%self.user_name

    @property
    def roles(self):
        '''获取用户角色'''
        if not hasattr(self,'_roles'):
            # 获取该用户下的角色ID
            relations = UserRoleRelation.objects.filter(user_id=self.id)
            role_id_list = [r.role_id for r in relations]
            self._roles = Roles.objects.filter(id__in=role_id_list)
        return self._roles



class UserProfile(models.Model):
    '''用户扩展表'''
    full_name = models.CharField(max_length=32,verbose_name='姓名')
    birthday_year = models.IntegerField(verbose_name='出生年',default=1900)
    birthday_month = models.IntegerField(verbose_name='出生月',default=1)
    birthday_day = models.IntegerField(verbose_name='出生日',default=1)

    # 计算年龄
    @property
    def age(self):
        today = datetime.date.today()
        birthday = datetime.date(year=self.birthday_year,month=self.birthday_month,day=self.birthday_day)
        return (today-birthday).days//365
    # 表名
    class Meta:
        db_table = 't_userprofile'
    # 关联userinfo表
    @property
    def userinfo(self):
        if not hasattr(self,'_userinfo'):
            self._userinfo,_ = UserInfo.objects.get_or_create(id=self.id)
        return self._userinfo


    def __str__(self):
        return '%s'%self.full_name


