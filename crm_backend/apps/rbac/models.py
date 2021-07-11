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
    # 获取权限列表
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

    # 获取该角色下的权限树
    @classmethod
    def get_role_has_permissions(cls,role_id):
        role_obj = cls.objects.filter(id=role_id).first()
        if not role_obj:
            return ''
        # 获取所有的权限
        per_1_dict = {}
        per_objs = role_obj.permissions
        for per_1 in per_objs:
            if per_1.permission_level==1:
                    per_1_dict[per_1.id] = per_1.to_dict()
                    per_1_dict[per_1.id]['children'] = []
        # 存放二级权限
        per_2_dict = {}
        for per_2 in per_objs:
            if per_2 .permission_level==2:
                tmp = per_2.to_dict()
                tmp.update({'children':[]})
                per_2_dict[per_2.id]=tmp
                per_1_dict[per_2.permission_parent_id]['children'].append(tmp)

        for per_3 in per_objs:
            if per_3.permission_level==3:
                per_2_dict[per_3.permission_parent_id]['children'].append(per_3.to_dict())

        return per_1_dict.values()


class Permissions(models.Model):
    '''权限表'''
    permission_name = models.CharField(max_length=32,verbose_name='权限名',unique=True)
    permission_url = models.CharField(max_length=32,verbose_name='权限URL')
    permission_parent_id = models.IntegerField(verbose_name='权限父ID',null=True)
    permission_level = models.IntegerField(verbose_name='权限等级')
    permission_icon = models.CharField(verbose_name='图标',null=True,default='',max_length=32)
    # 转化为字典
    def to_dict(self):
        return {
            'id':self.id,
            'permission_name':self.permission_name,
            'permission_url':self.permission_url,
            'permission_level':self.permission_level,
            'permission_parent_id':self.permission_parent_id,
            'permission_icon':self.permission_icon
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

    @classmethod
    def add_user_role(cls,user_id,roles_id_list):
        # 先把有的角色全删除
        # 可以优化查出来做差集,多的删除,少的添加
        cls.objects.filter(user_id=user_id).delete()
        cls_list=[]
        for roles_id in roles_id_list:
            cls_list.append(cls(user_id=user_id,role_id=roles_id))
        cls.objects.bulk_create(cls_list)
