<template>
  <div>
    <crumb></crumb>
    <div class="list">
      <el-card class="box-card">
        <div class="search">
          <el-input
            placeholder="用户名或邮箱查找"
            v-model="user_query"
            class="query"
          >
            <el-button slot="append" icon="el-icon-search" @click="search"></el-button>
          </el-input>
          <el-button type="primary" @click="openAddUserForm"
            >添加用户</el-button
          >
          <!-- 添加用户 -->
          <el-dialog
            title="添加用户"
            :visible.sync="addUserFromVisible"
            width="25%"
          >
            <el-form
              ref="add_user_ref"
              :model="addUserForm"
              label-position="left"
              class="add-user"
              :rules="addUserRules"
            >
 
              
              <el-form-item
                label="用户名:"
                label-width="100px"
                prop="user_name"
              >
                <el-input
                  v-model="addUserForm.user_name"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="密码:" label-width="100px" prop="user_pwd">
                <el-input
                  v-model="addUserForm.user_pwd"
                  type="password"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item
                label="确认密码:"
                label-width="100px"
                prop="user_pwd_r"
              >
                <el-input
                  v-model="addUserForm.user_pwd_r"
                  type="password"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="邮箱:" label-width="100px" prop="user_email">
                <el-input
                  v-model="addUserForm.user_email"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="cancelAdd">取 消</el-button>
              <el-button type="primary" @click="postUser">添 加</el-button>
            </div>
          </el-dialog>
        </div>
        <!-- 显示用户列表 -->
        <div class="user-table">
          <el-table :data="user_list" style="width: 100%" border>
            <el-table-column type="index" label="编号" :index="indexMethod" width="60px"> </el-table-column>
            <el-table-column prop="user_name" label="用户名"> </el-table-column>
            <el-table-column prop="user_email" label="邮箱"> </el-table-column>
            <el-table-column label="状态">
              <template slot-scope="scope">
                <span>{{ scope.row.user_status.status }}</span>
              </template>
            </el-table-column>
              <el-table-column label="角色">
              <template slot-scope="scope">
                <el-tag :key="role.id"
            v-for="(role,index) in scope.row.roles"
            :type="types[index% 5]"
          effect="dark"
          disable-transitions>{{role.name}}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button size="mini" @click="editUser(scope.row)"
                  >编辑</el-button
                >
                <el-button size="mini" type="danger" @click="delete_user(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :page-size="page_size"
            :current-page="current_page"
            background
            layout="prev, pager, next, jumper,sizes, ->, total"
            :total="total"
          >
          </el-pagination>
        </div>
      </el-card>
      <!-- 编辑用户 -->
      <el-dialog
        title="编辑用户"
        :visible.sync="editUserFormVisible"
        width="25%"
        :model="editForm"
      >
        <el-form class="edit-user">
          <el-form-item label="用户名:" label-width="80px">
            <el-input
              autocomplete="off"
              v-model="editForm.user_name"
            ></el-input>
          </el-form-item>
          <el-form-item label="密码:" label-width="80px">
            <el-input autocomplete="off" v-model="editForm.user_pwd"></el-input>
          </el-form-item>
          <el-form-item label="邮箱:" label-width="80px">
            <el-input
              autocomplete="off"
              v-model="editForm.user_email"
            ></el-input>
          </el-form-item>
          <el-form-item label="状态:" label-width="80px">
            <el-select v-model="editForm.user_status" placeholder="请选择状态">
              <el-option
                :label="item[1]"
                :value="item[0]"
                :key="item[0]"
                v-for="item in editForm.status_list"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="角色:" label-width="80px">
            <el-select
              v-model="editForm.roles_id"
              multiple
              placeholder="请选择"
            >
              <el-option
                v-for="role in editForm.roles_list"
                :key="role.id"
                :label="role.role_name"
                :value="role.id"
              >
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="editUserFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="updateEditForm">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>
<script>
import Crumb from "../crumb.vue";
import { get, post, put, _delete } from "../../assets/js/utils";
export default {
  name: "users",
  data() {
    // 自定义校验密码
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.addUserForm.user_pwd_r !== "") {
          this.$refs.add_user_ref.validateField("checkPass");
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.addUserForm.user_pwd) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      // 用户列表
      user_list: [],
      types: ["success", "info", "danger", "warning", ""],
      user_query: "",
      // 每页显示条码个数
      page_size: 10,
      // 全部条数
      total: 10,
      // 当前页数
      current_page: 1,
      // 打开添加用户对话框
      addUserFromVisible: false,
      // 添加用户表单
      addUserForm: {
        user_name: "",
        user_pwd: "",
        user_email: "",
        user_pwd_r: "",
      },
      // 添加用户规则
      addUserRules: {
        user_name: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        user_pwd: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { validator: validatePass, trigger: "blur" },
        ],

        user_pwd_r: [
          { required: true, message: "请再次输入密码", trigger: "blur" },
          { validator: validatePass2, trigger: "blur" },
        ],
        user_email: [
          { required: true, message: "请输入邮箱", trigger: "blur" },
        ],
      },
      // 编辑用户对话框
      editUserFormVisible: false,
      // 编辑用户表单
      editForm: {
        id: "",
        user_name: "",
        user_pwd: "",
        user_email: "",
        user_status: "",
        roles_id: [],
        roles_list: [],
        status_list: [],
      },
    };
  },

  mounted() {
    // 获取用户列表
    this.get_user_list();
  },
  components: {
    crumb: Crumb, //注册组件
  },

  methods: {
    indexMethod(index) {
      
        return index +1;
      },
    //查询
    search() {
      this.get_user_list();
    },
    async get_user_list() {
      const result = await get(
        `users/?page=${this.current_page}&&size=${this.page_size}&&q=${this.user_query}`
      );
      if (result.code != 1000) {
        this.$message.error(result.msg);
      }
      this.total = result.data.total;
      this.user_list = result.data.user_list;
      this.current_page = result.data.current_page;
    },
    // 更改size触发
    handleSizeChange(val) {
      this.page_size = val;
      this.get_user_list();
    },
    // 更改页数
    handleCurrentChange(val) {
      this.current_page = val;
      this.get_user_list();
    },
    // 打开添加用户对话框
    openAddUserForm() {
      this.addUserFromVisible = true;
    },
    //添加用户
    postUser() {
      this.$refs.add_user_ref.validate(async (vaild) => {
        if (!vaild) return;
        else {
          const result = await post("users/", this.addUserForm);
          if (result.code != 1000) {
            this.$message.error(result.msg);
          } else {
            // 添加成功提示
            this.$message.success(result.msg);
            // 重新获取列表
            this.get_user_list();
            // 关闭对话框
            this.addUserFromVisible = false;
            // 重置formdata
            this.$refs.add_user_ref.resetFields();
          }
        }
      });
    },
    // 取消添加
    cancelAdd() {
      // 重置表单
      this.$refs.add_user_ref.resetFields();
      // 关闭对话框
      this.addUserFromVisible = false;
    },
    // 编辑用户
    editUser(row) {
      console.log(row);
      this.get_user_single(row.id);
      this.editUserFormVisible = true;
    },
    // 获取单条user
    async get_user_single(id) {
      const result = await get(`/users/${id}`);
      if (result.code != 1000) return this.$message.error(result.msg);
      this.editForm = result.data;
    },
    // 提交更新
    async updateEditForm() {
      // console.log(this.editForm);
      const result = await put(`/users/${this.editForm.id}`, this.editForm);
      if (result.code != 1000) return this.$message.error(result.msg);
      this.$message.success(result.msg);
      this.get_user_list();
      this.editUserFormVisible = false;
    },
    delete_user(row) {
      this.$confirm("此操作将永久删除该记录, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(async () => {
          const result = await _delete(`/users/${row.id}`);
          if (result.code != 1000) return this.$message.error(result.msg);
          this.get_user_list();
          this.$message({
            type: "success",
            message: result.msg,
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
  },
};
</script>

<style>
.list {
  height: 100%;
  margin-top: 20px;
}
.search {
  display: flex;
  justify-content: flex-start;
  width: 400px;
}
.query {
  padding-right: 20px;
}
.add-user .el-input__inner {
  width: 90%;
}
.el-tag {
  margin: 0 10px;
}
/* .edit-user .el-input__inner {
  width: 90%;
} */
</style>