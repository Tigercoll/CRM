<template>
  <div>
    <crumb></crumb>

    <div class="list">
      <el-card class="box-card">
        <!-- 查询开始 -->
        <div class="search">
          <!-- vue中需要加一个native -->
          <el-input
            placeholder="关键词查询"
            v-model="q"
            class="query"
            @keyup.enter.native="search"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="search"
            ></el-button>
          </el-input>
          <!-- 查询结束 -->

          <!-- 添加客户开始 -->
          <el-button type="primary" @click="openAddCustomersForm"
            >添加客户</el-button
          >
          <!-- 添加客户结束 -->
          <!-- 添加对话框 -->

          <el-dialog
            title="添加客户"
            :visible.sync="openAddCustomereVisible"
            width="30%"
            @close="cancelAddCustomerForm"
          >
            <el-form
              :model="customerForm"
              :rules="customerFormRules"
              ref="customerFormRef"
              label-width="100px"
              style="width: 90%"
            >
              <el-form-item label="客户编码" prop="customer_id">
                <el-input v-model="customerForm.customer_id"></el-input>
              </el-form-item>
              <el-form-item label="客户名称" prop="customer_name">
                <el-input v-model="customerForm.customer_name"></el-input>
              </el-form-item>
              <el-form-item label="客户描述" prop="customer_desc">
                <el-input v-model="customerForm.customer_desc"></el-input>
              </el-form-item>
              <el-form-item label="业务员" prop="salesman">
                <el-select
                  v-model="customerForm.salesman"
                  placeholder="请选择业务员"
                  style="width: 100%"
                  clearable
                >
                  <el-option
                    :label="item.user_name"
                    :value="item.id"
                    :key="item.id"
                    v-for="item in salesman_list"
                  ></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="状态" prop="customer_status">
                <el-input v-model="customerForm.customer_status"></el-input>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="cancelAddCustomerForm">取 消</el-button>
              <el-button type="primary" @click="addCustomer">添 加</el-button>
            </span>
          </el-dialog>
        </div>

        <div class="customers-table">
          <el-table :data="customer_list" style="width: 100%" border>
            <el-table-column prop="id" label="id" width="60px" sortable>
            </el-table-column>
            <el-table-column prop="customer_id" label="客户编号">
            </el-table-column>
            <el-table-column prop="customer_name" label="客户名称">
            </el-table-column>
            <el-table-column prop="customer_desc" label="客户描述">
            </el-table-column>
            <el-table-column prop="salesman_name" label="销售人员">
            </el-table-column>
            <el-table-column prop="create_time" label="创建时间">
            </el-table-column>
            <el-table-column prop="update_time" label="更新时间">
            </el-table-column>
            <el-table-column prop="customer_status" label="状态"> </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button
                  type="warning"
                  size="mini"
                  @click="openEditCustomer(scope.row)"
                  >修改</el-button
                >
                <el-button type="danger" size="mini" @click="deleteCustomer(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <!-- 修改客户对话框 -->
          <el-dialog
            title="修改客户"
            :visible.sync="openEditCustomereVisible"
            width="30%"
          >
            <el-form
              :model="customerForm"
              :rules="customerFormRules"
              ref="customerEditFormRef"
              label-width="100px"
              style="width: 90%"
            >
              <el-form-item label="客户编码" prop="customer_id">
                <el-input v-model="customerForm.customer_id"></el-input>
              </el-form-item>
              <el-form-item label="客户名称" prop="customer_name">
                <el-input v-model="customerForm.customer_name"></el-input>
              </el-form-item>
              <el-form-item label="客户描述" prop="customer_desc">
                <el-input v-model="customerForm.customer_desc"></el-input>
              </el-form-item>
              <el-form-item label="业务员" prop="salesman">
                <el-select
                  v-model="customerForm.salesman"
                  placeholder="请选择业务员"
                  style="width: 100%"
                  clearable
                >
                  <el-option
                    :label="item.user_name"
                    :value="item.id"
                    :key="item.id"
                    v-for="item in salesman_list"
                  ></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="状态" prop="customer_status">
                <el-input v-model="customerForm.customer_status"></el-input>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="openEditCustomereVisible = false"
                >取 消</el-button
              >
              <el-button type="primary" @click="editCustomer(customerForm.id)">修 改</el-button>
            </span>
          </el-dialog>

          <div class="pagination">
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="page"
              :page-sizes="[10, 20, 30, 50]"
              :page-size="page_size"
              layout="total, sizes, prev, pager, next, jumper"
              :total="total"
            >
            </el-pagination>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>
<script>
import Crumb from "../crumb.vue";
import { get, post, put,_delete } from "../../assets/js/utils";
export default {
  name: "Customers",
  components: { Crumb },

  data() {
    return {
      // 查询关键词
      q: "",
      // 客户列表
      customer_list: [],
      // 分页长度
      page_size: 10,
      // 总数
      total: 0,
      // 当前页
      page: 1,
      // 打开添加客户按钮
      openAddCustomereVisible: false,
      // 打开修改客户按钮
      openEditCustomereVisible: false,
      // 业务员列表
      salesman_list: [],
      // 客户表单
      customerForm: {
        customer_id: "",
        customer_name: "",
        customer_desc: "",
        salesman: null,
        customer_status: "",
      },
      // 规则
      customerFormRules: {
        hospital_code: [
          { required: true, message: "请输入医院代码", trigger: "blur" },
        ],
        hospital_name: [
          { required: true, message: "请输入医院名称", trigger: "blur" },
        ],
      },
    };
  },

  mounted() {
    this.get_customer_list();
    // 获取业务员信息
    this.get_salesman_list();
  },

  methods: {
    // 获取客户列表
    async get_customer_list() {
      const result = await get(
        `/customers/?page=${this.page}&&size=${this.page_size}&&q=${this.q}`
      );
      if (result.code != 1000) {
        return this.$message.error(result.msg);
      }
      this.customer_list = result.data.customer_list;
      this.page = result.data.page;
      this.total = result.data.total;
    },
    // 改变分页长度触发
    handleSizeChange(val) {
      this.page_size = val;
      this.get_customer_list();
    },
    // 改变当前页触发
    handleCurrentChange(val) {
      this.page = val;
      this.get_customer_list();
    },
    // 查询
    search() {
      this.page = 1;
      this.page_size = 10;
      this.get_customer_list();
    },
    // 获取业务员列表
    async get_salesman_list() {
      const result = await get("users/all/");
      console.log(result);
      if (result.code != 1000) {
        return this.$message.error(result.msg);
      }
      this.salesman_list = result.data;
    },

    // 打开添加客户对话框
    openAddCustomersForm() {
      this.openAddCustomereVisible = true;
    },
    clearCustomerForm() {
      this.customerForm = {
        hospital_code: "",
        hospital_name: "",
        hospital_contacts: "",
        hospital_lis: "",
        salesman: null,
        use_type: "",
      };
    },
    // 取消添加客户
    cancelAddCustomerForm() {
      this.clearCustomerForm();
      this.openAddCustomereVisible = false;
    },
    // 添加客户
    addCustomer() {
      this.$refs.customerFormRef.validate(async (valid) => {
        if (!valid) {
          return;
        }
        const result = await post("customers/", this.customerForm);
        if (result.code != 1000) {
          return this.$message.error(result.msg);
        }

        this.clearCustomerForm();
        this.get_customer_list();
        this.$message.success(result.msg)
        this.openAddCustomereVisible = false;
        
      });
    },
    // 打开修改客户对话框
    async openEditCustomer(row) {
      // 请求单条客户数据
      const result = await get(`customers/${row.id}`);
      if (result.code != 1000) {
        return this.$message.error(result.msg);
      }
      this.customerForm = result.data;
      this.openEditCustomereVisible = true;
    },
    // 编辑客户
    editCustomer(id) {
      this.$refs.customerEditFormRef.validate(async valid =>{
        if (!valid) { return }
        const result =await put(`customers/${id}`,this.customerForm)
        if (result.code!=1000) {return this.$message.error(result.msg)          
        }
        this.$message.success(result.msg)
        this.get_customer_list()
        this.openEditCustomereVisible = false
        
      })
    },
    // 删除客户
    deleteCustomer(row){
      this.$confirm('此操作将永久删除该条记录, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async () => {
          const result =await _delete(`customers/${row.id}`)
          if (result.code!==1000) {
            throw result.msg
          }
          this.get_customer_list()
          this.$message({
            type: 'success',
            message: result.msg
          });
        }).catch((error) => {
          let msg=null
          if(error=='cancel'){
            msg = '取消删除'
          }else{
              msg =error
          }
          
          this.$message({
            type: 'info',
            message: msg
          });          
        });
    }
  },
};
</script>

<style>
.list {
  height: 100%;
  margin-top: 20px;
}
.customers-table {
  margin-top: 20px;
}
.pagination {
  margin-top: 10px;
}
</style>