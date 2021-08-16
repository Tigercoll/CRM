from rest_framework.views import APIView
from .serializers import *
from .models import *
from utils.response_format import render_data
from utils import status_code
# Create your views here.

class PermissionsListView(APIView):
    def get(self,request,type):
        # 获取所有权限
        if type=='list':
            per_list = Permissions.get_permission_list()
        elif type=='tree':
            per_list = Permissions.get_permission_tree()
        else:
            return render_data(status_code.PARAMETER_ERROR,'','参数错误')
        return render_data(status_code.OK,per_list,'获取权限列表成功')

class PermissionsView(APIView):
    def get(self,request,pk):
        per = Permissions.objects.filter(id=pk).first()
        if not per:
            return render_data(status_code.PARAMETER_ERROR, '', '参数错误')
        return render_data(status_code.OK,per.to_dict(),'获取权限成功')

    def post(self,request):
        # 添加权限
        data = request.data

        ser = PermissionSerializers(data=data)
        if ser.is_valid():
            ser.save()
            return render_data(status_code.OK,ser.data,'添加权限成功')
        return render_data(status_code.FAILED_2_ADD,ser.errors,'添加权限失败')

    def put(self,request,pk):
        # 更新权限
        data = request.data
        per = Permissions.objects.filter(id=pk).first()
        p_id = data.get('permission_parent_id')
        if str(pk)==str(p_id):
            return render_data(status_code.PARAMETER_ERROR, '', '父ID不能为自己')
        if not per:
            return render_data(status_code.PARAMETER_ERROR, '', '参数错误')
        ser = PermissionSerializers(instance=per,data=data)
        if ser.is_valid():
            ser.save()
            return render_data(status_code.OK, ser.data, '修改权限成功')
        return render_data(status_code.FAILED_2_UPDATE, ser.errors, '修改权限失败')

    def delete(self,request,pk):
        # 删除权限
        per = Permissions.objects.filter(id=pk).first()
        if not per:
            return render_data(status_code.PARAMETER_ERROR, '', '参数错误')
        is_cascade = request.GET.get('cascade')
        if is_cascade==1:
            self.cascade_delete(per)
        else:
            per.delete()
        return render_data(status_code.OK, '', '删除成功')

    def cascade_delete(self,per_obj):
        # 如果有子权限级联删除
        if per_obj.permissions:
            for per in per_obj.permissions:
                self.cascade_delete(per)
                per.delete()
        else:
            per_obj.delete()

class PermissionsLevelView(APIView):
    '''获取权限等级'''
    def get(self,request,level):
        '''根据等级获取权限'''
        per_list = Permissions.get_permission_by_level(level)
        if not per_list:
            return render_data(status_code.PARAMETER_ERROR,'','参数错误')
        
        return render_data(status_code.OK,per_list,'获取权限等级成功')

class RolesListView(APIView):
    # 获取角色列表
    def get(self,request):
        roles_list = Roles.get_roles_list()
        return render_data(status_code.OK,roles_list,'获取角色列表成功')

class RolesView(APIView):
    # 获取单个角色
    def get(self,request,pk):
        roles_obj = Roles.objects.filter(id=pk).first()
        if not roles_obj:
            return render_data(status_code.PARAMETER_ERROR, '', '参数错误')
        return render_data(status_code.OK,roles_obj.to_dict(),'获取角色成功')
    # 添加角色
    def post(self,request):
        data = request.data
        ser = RoleSerializers(data=data)
        if ser.is_valid():
            ser.save()
            return render_data(status_code.OK, ser.data, '添加角色成功')
        return render_data(status_code.FAILED_2_ADD, ser.errors, '添加角色失败')
    # 修改角色
    def put(self,request,pk):
        roles_obj = Roles.objects.filter(id=pk).first()
        data = request.data
        ser = RoleSerializers(instance=roles_obj,data=data)
        if ser.is_valid():
            ser.save()
            return render_data(status_code.OK, ser.data, '修改角色成功')
        return render_data(status_code.FAILED_2_UPDATE, ser.errors, '修改角色失败')
    def delete(self,request,pk):
        # 删除角色
        role_obj = Roles.objects.filter(id=pk).first()
        if not role_obj:
            return render_data(status_code.PARAMETER_ERROR, '', '参数错误')
        # 删除角色
        role_obj.delete()
        RolePermissionRelation.objects.filter(role_id=pk).delete()
        # 删除角色权限关系表
        return render_data(status_code.OK, '', '删除成功')

class RolesHasPermissionView(APIView):
    def get(self,request,pk):
        roles_per_list =Roles.get_role_has_permissions(pk)
        return render_data(status_code.OK,roles_per_list,'获取成功')


    def post(self,request,pk):
        per_list = request.data.get('per_list',[])
        result = RolePermissionRelation.add_permission_by(pk,per_list)
        if not result:
            return render_data(status_code.FAILED_2_ADD,'','权限配置失败')
        else:
            return  render_data(status_code.OK,'','权限配置成功')

    def delete(self,request,role_id,permission_id):
        result = RolePermissionRelation.delete_role_permission(role_id,permission_id)
        if result:
            return render_data(status_code.OK,'','删除成功')
        else:
            return  render_data(status_code.PARAMETER_ERROR,'','参数错误')
class MenuListView(APIView):
    def get(self,request):
        per_exist_list = []
        user = request.user
        user_roles_obj = user.roles
        per_dict={}
        per_2_list = []
        for role_obj in user_roles_obj:
            for per in role_obj.permissions:
                if per.permission_level==1:
                    if per.id not in per_exist_list:
                        per_dict[per.id]=per.to_dict()
                        per_dict[per.id]['children']=[]
                        per_exist_list.append(per.id)
                if per.permission_level==2:
                    if per.id not in per_exist_list:
                        per_2_list.append(per)
        for per_2 in per_2_list:
            if per_2.permission_parent_id in per_dict:
                if per_2.id not in per_exist_list:
                    per_exist_list.append(per_2.id)
                    per_dict[per_2.permission_parent_id]['children'].append(per_2.to_dict())

        return render_data(status_code.OK,per_dict.values(),'获取菜单列表')



class RolesHasPermissionListView(APIView):
    def get(self,request,pk):
        per_list = RolePermissionRelation.get_level_3_permission_list_by(pk)
        return render_data(status_code.OK,per_list,'获取权限列表成功')

