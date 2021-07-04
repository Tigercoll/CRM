from django.db import models

# Create your models here.

class Roles(models.Model):
    '''角色表'''
    role_name = models.CharField(max_length=32,verbose_name='角色名',unique=True)
    role_desc = models.CharField(max_length=128,verbose_name='角色说明',null=True)
    class Meta:
        db_table='t_roles'

    def __str__(self):
        return self.role_name

    def to_dict(self):
        return {
            'id':self.id,
            'role_name':self.role_name,
            'role_desc':self.role_desc
        }

    # 获取角色列表
    @classmethod
    def get_roles_list(cls):
        roles_list = []
        role_obj = cls.objects.all()
        for r in role_obj:
            roles_list.append(r.to_dict())
        return roles_list

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
    permission_name = models.CharField(max_length=32,verbose_name='权限名',unique=True)
    permission_url = models.CharField(max_length=32,verbose_name='权限URL')
    permission_parent_id = models.IntegerField(verbose_name='权限父ID',null=True)
    permission_level = models.IntegerField(verbose_name='权限等级')

    # 转化为字典
    def to_dict(self):
        return {
            'id':self.id,
            'permission_name':self.permission_name,
            'permission_url':self.permission_url,
            'permission_level':self.permission_level,
            'permission_parent_id':self.permission_parent_id
        }

    # 根据权限等级获取权限
    @classmethod
    def get_permission_by_level(cls,level):
        per_list=[]
        per_obj = cls.objects.filter(permission_level=level)
        for per in per_obj:
            per_list.append(
                per.to_dict()
            )

        return per_list

    # 获取权限列表结构
    @classmethod
    def get_permission_list(cls):
        '''获取所有权限列表'''
        per_list = []
        per_obj = cls.objects.all().order_by('permission_level')
        for per in per_obj:
            per_list.append(per.to_dict())
        return per_list

    # 获取权限树状结构
    @classmethod
    def get_permission_tree(cls):
        '''获取权限树结构'''

        per_list = []

        # 获取一级权限
        per_obj = cls.objects.filter(permission_parent_id=None)

        for per in per_obj:
            p_child_list = []
            for p_child in per.permissions:
                p_child_dict = p_child.to_dict()
                p_child_dict.update({
                    'children':[p_child_2.to_dict() for p_child_2 in p_child.permissions]
                })
                p_child_list.append(p_child_dict)
            per_dict = per.to_dict()
            per_dict.update({
                'children':p_child_list
            })
            per_list.append(per_dict)



        return per_list

    # 获取权限父节点
    @property
    def permission_parent(self):
        '''获取当前权限的父权限'''
        if not self.permission_parent_id:
            return None

        if not hasattr(self,'_permission_parent'):
            self._permission_parent = Permissions.objects.filter(id=self.permission_parent_id).first()

        return self._permission_parent

    # 获取权限子节点
    @property
    def permissions(self):
        '''获取当前权限的子权限'''
        if not hasattr(self,'_permissions'):
            self._permissions = Permissions.objects.filter(permission_parent_id=self.id)

        return self._permissions

    # 重命名 表名
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