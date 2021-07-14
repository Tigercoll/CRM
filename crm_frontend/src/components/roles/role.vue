<template>
  <div>
    <Crumb></Crumb>
    <div class="list">
      <el-card class="box-card">
        <el-button type="primary" @click="openAddRole">添加角色</el-button>
        <div class="table-box">
          <el-table
            :data="role_list"
            style="width: 100%"
            border
            @expand-change="expandHandle"
          >
            <el-table-column type="expand">
              <template slot-scope="scope">
                <el-row
                  :key="permission.id"
                  v-for="permission in role_permission[scope.row.id]"
                  class="v-center"
                >
                  <!-- 一级权限 -->
                  <el-col :span="5">
                    <el-tag
                      @close="delete_per(scope.row, permission.id)"
                      closable
                      >{{ permission.permission_name }}</el-tag
                    >
                    <el-icon class="el-icon-caret-right"></el-icon>
                  </el-col>
                  <!-- 二级三级权限 -->
                  <el-col :span="19">
                    <!-- 二级权限 -->
                    <el-row
                      class="v-center"
                      :key="permission_child.id"
                      v-for="permission_child in permission.children"
                    >
                      <el-col :span="6">
                        <el-tag
                          @close="delete_per(scope.row, permission_child.id)"
                          closable
                          type="success"
                          >{{ permission_child.permission_name }}</el-tag
                        >
                        <el-icon class="el-icon-caret-right"></el-icon>
                      </el-col>
                      <!-- 三级权限 -->
                      <el-col :span="18">
                        <el-tag
                          @close="delete_per(scope.row, child.id)"
                          closable
                          type="warning"
                          :key="child.id"
                          v-for="child in permission_child.children"
                          >{{ child.permission_name }}</el-tag
                        >
                      </el-col>
                    </el-row>
                  </el-col>
                </el-row>
              </template>
            </el-table-column>
            <el-table-column
              type="index"
              label="编号"
              width="60px"
              align="center"
            >
            </el-table-column>
            <el-table-column prop="role_name" align="center" label="角色名称">
            </el-table-column>
            <el-table-column prop="role_desc" align="center" label="角色描述">
            </el-table-column>
            <el-table-column align="center" label="操作">
              <template slot-scope="scope">
                <el-button size="mini" @click="openEditRole(scope.row)"
                  >编辑</el-button
                >
                <el-button
                  size="mini"
                  type="warning"
                  @click="openSetPermission(scope.row)"
                  >分配权限</el-button
                >
                <el-button
                  size="mini"
                  type="danger"
                  @click="delete_role(scope.row)"
                  >删除</el-button
                >
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
      <!-- 添加角色对话框 -->
      <el-dialog
        title="添加角色"
        width="30%"
        :visible.sync="dialogRoleFormVisible"
      >
        <el-form :model="role_form" ref="roleRef" :rules="rulesRole">
          <el-form-item label="角色名称:" label-width="100px" prop="role_name">
            <el-input
              v-model="role_form.role_name"
              autocomplete="off"
            ></el-input>
          </el-form-item>
          <el-form-item label="角色描述:" label-width="100px">
            <el-input
              v-model="role_form.role_desc"
              autocomplete="off"
            ></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="cancelAdd">取 消</el-button>
          <el-button type="primary" @click="addRole">确 定</el-button>
        </div>
      </el-dialog>
      <!-- 编辑角色对话框 -->
      <el-dialog
        title="编辑角色"
        width="30%"
        :visible.sync="dialogEditRoleFormVisible"
      >
        <el-form :model="role_form" ref="roleRef" :rules="rulesRole">
          <el-form-item label="角色名称:" label-width="100px" prop="role_name">
            <el-input
              v-model="role_form.role_name"
              autocomplete="off"
            ></el-input>
          </el-form-item>
          <el-form-item label="角色描述:" label-width="100px">
            <el-input
              v-model="role_form.role_desc"
              autocomplete="off"
            ></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="cancelEdit">取 消</el-button>
          <el-button type="primary" @click="editRole">确 定</el-button>
        </div>
      </el-dialog>
      <!-- 分配权限对话框 -->
      <el-dialog title="分配权限" :visible.sync="dialogSetPermissionVisible" width="50%">
        <el-tree ref="per_tree"  show-checkbox node-key='id' :default-checked-keys='checked_per_list' :highlight-current="true" :default-expand-all="true" :data="permission_list_tree" :props="permissionProps" ></el-tree>
        <div slot="footer" class="dialog-footer">
          <el-button @click="cancelSet">取 消</el-button>
          <el-button type="primary" @click="setPermission"
            >确 定</el-button
          >
        </div>
      </el-dialog>
    </div>
  </div>
</template>
<script>
import Crumb from "../crumb.vue";
import { get, post, put, _delete } from "../../assets/js/utils";
export default {
  components: { Crumb },

  data() {
    return {
      // 角色权限字典
      role_permission: {},
      // 角色列表
      role_list: [],
      // 角色表单
      role_form: {
        id: "",
        role_name: "",
        role_desc: "",
      },
      // 角色添加对话框
      dialogRoleFormVisible: false,
      // 添加角色规则
      rulesRole: {
        role_name: [
          { required: true, message: "请输入角色名", trigger: "blur" },
        ],
      },
      dialogEditRoleFormVisible: false,
      dialogSetPermissionVisible:false,
      permission_list_tree:[],
      permissionProps:{
        children:'children',
        label:'permission_name'
      },
      checked_per_list:[],
      role_id:''
    };
  },

  mounted() {
    this.get_role_list();
  },
  methods: {
    // 获取角色列表
    async get_role_list() {
      const result = await get("roles/list/");
      if (result.code != 1000) return this.$message.error(result.msg);
      this.role_list = result.data;
    },
    // 打开添加角色对话框
    openAddRole() {
      this.clean_from();
      this.dialogRoleFormVisible = true;
    },
    // 添加角色
    addRole() {
      this.$refs.roleRef.validate(async (vaild) => {
        if (!vaild) {
          return;
        }
        const result = await post("roles/", this.role_form);
        if (result.code != 1000) {
          return this.$message.error(result.msg);
        }
        this.$message.success(result.msg);
        this.get_role_list();
        // 清空添加form

        this.dialogRoleFormVisible = false;
      });
    },
    // 关闭添加
    cancelAdd() {
      this.dialogRoleFormVisible = false;
    },
    //清除表单
    clean_from() {
      this.role_form = {
        role_name: "",
        role_desc: "",
      };
    },
    // 打开编辑并获取单条数据
    async openEditRole(row) {
      const result = await get(`roles/${row.id}`);
      if (result.code != 1000) return this.$message.error(result.msg);
      this.role_form = result.data;
      this.dialogEditRoleFormVisible = true;
    },
    // 取消编辑
    cancelEdit() {
      this.dialogEditRoleFormVisible = false;
    },
    // 提交编辑
    editRole() {
      this.$refs.roleRef.validate(async (vaild) => {
        if (!vaild) {
          return;
        }
        const result = await put(`roles/${this.role_form.id}`, this.role_form);
        if (result.code != 1000) return this.$message.error(result.msg);
        this.$message.success(result.msg);
        this.get_role_list();
        this.dialogEditRoleFormVisible = false;
      });
    },
    delete_role(row) {
      this.$confirm("此操作将永久删除该角色, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(async () => {
          const resutl = await _delete(`roles/${row.id}`);
          if (resutl.code != 1000) return this.$message(resutl.msg);
          this.get_role_list();
          this.$message({
            type: "success",
            message: resutl.msg,
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    // 展开获取权限
    async expandHandle(row) {
      const id = row.id;
      // 如果存在则跳过
      if (this.role_permission[id]) {
        return;
      } else {
        const result = await get(`roles/permissions/${id}`);
        this.$set(this.role_permission, id, result.data);
        // this.role_permission[id] = result.data
      }
    },
    // 点击tag标签删除权限
    async delete_per(row, permission_id) {
      const role_id = row.id;
      const result = await _delete(
        `roles/${role_id}/permissions/${permission_id}`
      );
      if (result.code != 1000) return this.$message.error(result.msg);
      this.$message.success(result.msg);
      const per_result = await get(`roles/permissions/${role_id}`);
      this.$set(this.role_permission, role_id, per_result.data);
    },
    async openSetPermission(row) {
     
      this.role_id = row.id
      const result = await get('permission/list/tree/')
      if(result.code!=1000)return this.$message.error(result.msg)
      this.permission_list_tree = result.data
      const checked_per = await get(`roles/${row.id}/permissions/list`)
      if (checked_per.code!==1000) {return this.$message.error(checked_per.msg)
        
      }
      this.checked_per_list = checked_per.data
      this.dialogSetPermissionVisible =true
    },
    async setPermission(){
      const checked_keys = this.$refs.per_tree.getCheckedKeys()
      const checked_half_keys = this.$refs.per_tree.getHalfCheckedKeys()
      checked_half_keys.push.apply(checked_half_keys,checked_keys);
      console.log(checked_half_keys);
      const result =await post(`roles/permissions/${this.role_id}`,{per_list:checked_half_keys})
      if (result.code!==1000) {
        return this.$message.error(result.msg)        
      }
      this.$message.success(result.msg)
      this.role_permission={}
      this.checked_per_list=[]
      this.dialogSetPermissionVisible=false
      
    },
    cancelSet(){
       this.role_permission={}
      this.checked_per_list=[]
      this.dialogSetPermissionVisible=false
    }
  },
};
</script>
<style>
.list {
  height: 100%;
  margin-top: 20px;
}
.table-box {
  margin-top: 10px;
}
.el-tag {
  margin: 7px;
}
.v-center {
  display: flex;
  align-items: center;
}
</style>