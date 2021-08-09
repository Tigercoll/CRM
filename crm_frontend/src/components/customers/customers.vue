<template>
  <div>
    <crumb></crumb>

    <div class="list">
      <el-card class="box-card">
        <!-- 查询开始 -->
        <div class="search">
          <el-input placeholder="关键词查询" v-model="q" class="query">
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="search"
            ></el-button>
          </el-input>
          <!-- 查询结束 -->

          <!-- 添加客户开始 -->
          <el-button type="primary" @click="openAddCustomereForm = true"
            >添加客户</el-button
          >
          <!-- 添加客户结束 -->
          <!-- 添加对话框 -->

          <el-dialog
            title="添加客户"
            :visible.sync="openAddCustomereForm"
            width="30%"
          >
            <el-form
              :model="customerForm"
              :rules="customerFormRules"
              ref="ruleForm"
              label-width="100px"
              
              
            >
              <el-form-item label="医院代码" prop="hospital_code">
                <el-input v-model="customerForm.hospital_code"></el-input>
              </el-form-item>
              <el-form-item label="医院名称" prop="hospital_name">
                <el-input v-model="customerForm.hospital_name"></el-input>
              </el-form-item>
              <el-form-item label="医院联系人" prop="hospital_contacts">
                <el-input v-model="customerForm.hospital_contacts"></el-input>
              </el-form-item>
              <el-form-item label="医院lis" prop="hospital_lis">
                <el-input v-model="customerForm.hospital_lis"></el-input>
              </el-form-item>
              <el-form-item label="业务员" prop="salesman">
                <el-input v-model="customerForm.salesman"></el-input>
              </el-form-item>
              <el-form-item label="状态" prop="use_type">
                <el-input v-model="customerForm.use_type"></el-input>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="openAddCustomereForm = false">取 消</el-button>
              <el-button type="primary" @click="openAddCustomereForm = false"
                >添 加</el-button
              >
            </span>
          </el-dialog>
        </div>

        <div class="customers-table">
          <el-table :data="customer_list" style="width: 100%" border>
            <el-table-column prop="id" label="id" width="60px">
            </el-table-column>
            <el-table-column prop="hospital_code" label="医院代码">
            </el-table-column>
            <el-table-column prop="hospital_name" label="医院名称">
            </el-table-column>
            <el-table-column prop="hospital_contacts" label="医院联系人">
            </el-table-column>
            <el-table-column prop="hospital_lis" label="第三方lis">
            </el-table-column>
            <el-table-column prop="salesman" label="业务员"> </el-table-column>
            <el-table-column prop="create_time" label="创建时间">
            </el-table-column>
            <el-table-column prop="update_time" label="更新时间">
            </el-table-column>
            <el-table-column prop="use_type" label="状态"> </el-table-column>
            <el-table-column label="操作">
              <template>
                <el-button type="warning" size="mini">修改</el-button>
                <el-button type="danger" size="mini">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
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
import { get } from "../../assets/js/utils";
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
      openAddCustomereForm: false,
      // 客户表单
      customerForm: {
        hospital_code: "",
        hospital_name:'',
        hospital_contacts:'',
        hospital_lis:'',
        salesman:'',
        use_type:''
      },
    // 规则
    customerFormRules:{
        hospital_code:[
            { required: true, message: '请输入医院代码', trigger: 'blur' },
        ],
        hospital_name:[
            { required: true, message: '请输入医院名称', trigger: 'blur' },
        ]
    }
    };
  },

  mounted() {
    this.get_customer_list();
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
      console.log(result);
      this.customer_list = result.data.customer_list;
      this.page = result.data.page;
      this.total = result.data.total;
      console.log(this.customer_list);
    },
    // 改变分页长度触发
    handleSizeChange(val) {
      console.log(val);
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