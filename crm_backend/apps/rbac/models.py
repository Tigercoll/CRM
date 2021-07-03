from django.db import models

# Create your models here.

class Roles(models.Model):
    '''角色表'''
    role_name = models.CharField(max_length=32,verbose_name='角色名')

    class Meta:
        db_table='t_roles'

    def __str__(self):
        return self.role_name

    @property
    def permissions(self):
        '''获取该角色下的所有权限'''
        if not hasattr(self,'_permissions'):
            # 从关系表获取权限ID
            relations = RolePermissionRelation.objects.filter(role_id=self.id)

            # 根据权限ID 获取权限
            permissions_id_list = [r.permission_id for r in relations]
            self._permissions = Permissions.objects.filter(id__in=permissions_id_list)
        return self._permissions


class Permissions(models.Model):
    '''权限表'''
    permission_name = models.CharField(max_length=32,verbose_name='权限名')
    permission_url = models.CharField(max_length=32,verbose_name='权限URL')
    permission_parent_id = models.IntegerField(verbose_name='权限父ID',null=True)
    permission_level = models.IntegerField(verbose_name='权限等级')

    @classmethod
    def get_permission_list(cls):
        '''获取所有权限列表'''
        per_list = []
        per_obj = cls.objects.all().order_by('permission_level')
        for per in per_obj:
            per_list.append({
                'id':per.id,
                'name':per.permission_name,
                'url':per.permission_url,
                'level':per.permission_level,
                'pid':per.permission_parent_id
            })
        return per_list
        return per_list
    @property
    def permission_parent(self):
        '''获取当前权限的父权限'''
        if not self.permission_parent_id:
            return None

        if not hasattr(self,'_permission_parent'):
            self._permission_parent = Permissions.objects.filter(id=self.permission_parent_id).first()

        return self._permission_parent

    @property
    def permissions(self):
        '''获取当前权限的子权限'''
        if not hasattr(self,'_permissions'):
            self._permissions = Permissions.objects.filter(permission_parent_id=self.id)

        return self._permissions

    class Meta:
        db_table='t_permissions'


class RolePermissionRelation(models.Model):
    '''权限角色关系表'''
    role_id = models.IntegerField(verbose_name='角色ID')
    permission_id = models.IntegerField(verbose_name='权限ID')

    class Meta:
        db_table='t_rolepermissionrelation'


class UserRoleRelation(models.Model):
    '''用户角色关系表'''
    user_id = models.IntegerField(verbose_name='用户ID')
    role_id = models.IntegerField(verbose_name='角色ID')

    class Meta:
        db_table='t_userrolerelation'