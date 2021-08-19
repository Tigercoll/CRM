<template>
  <div>
    <crumb></crumb>
    <div class="list">
      <el-card class="box-card">
        <div class="search">
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

          <!-- 添加联系人开始 -->
          <el-button type="primary" @click="openAddCustomereVisible=true">添加联系人</el-button>
          <!-- 添加联系人对话框 -->
          <el-dialog
            title="添加联系人"
            :visible.sync="openAddCustomereVisible"
            width="30%"
            @close ="clearLinkmanForm"
          >
            <el-form
              :model="linkmanForm"
              :rules="linkmanFormRules"
              ref="linkmanFormRef"
              label-width="100px"
              style="width: 90%"
            >
              <el-form-item label="姓名" prop="name">
                <el-input v-model="linkmanForm.name"></el-input>
              </el-form-item>
              <el-form-item label="客户" prop="customer_id">
                <el-select
                  v-model="linkmanForm.customer_id"
                  clearable
                  filterable
                  remote
                  reserve-keyword
                  placeholder="请输入关键词"
                  :remote-method="get_customer_list"
                  style="width: 100%"
                >
                  <el-option
                    v-for="item in customer_list"
                    :key="item.customer_id"
                    :label="item.customer_name"
                    :value="item.customer_id"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="手机号" prop="phone">
                <el-input v-model="linkmanForm.phone"></el-input>
              </el-form-item>
              <el-form-item label="性别" prop="gender">
               <el-select v-model="linkmanForm.gender" style="width: 100%">
                  <el-option :key='index' v-for="(item,index) in gender_list"
                  :label="item.name"
                  :value="item.id"
                  >

                  </el-option>
               </el-select>
              </el-form-item>
              <el-form-item label="QQ" prop="QQ">
                <el-input v-model="linkmanForm.QQ"></el-input>
              </el-form-item>
              <el-form-item label="爱好" prop="likes">
                <el-input v-model="linkmanForm.likes"></el-input>
              </el-form-item>
              <el-form-item label="职位" prop="position">
                <el-input v-model="linkmanForm.position"></el-input>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="cancelAdd">取 消</el-button>
              <el-button type="primary" @click="addLinkman">添 加</el-button>
            </span>
          </el-dialog>
        </div>
        <div class="linkman-table">
          <el-table :data="linkman_list" style="width: 100%" border>
            <el-table-column prop="id" label="id" width="60px" sortable>
            </el-table-column>
            <el-table-column prop="name" label="联系人"> </el-table-column>
            <el-table-column prop="customer_name" label="客户名称">
            </el-table-column>
            <el-table-column prop="gender" label="性别"> </el-table-column>
            <el-table-column prop="position" label="职位"> </el-table-column>
            <el-table-column prop="QQ" label="QQ"> </el-table-column>
            <el-table-column prop="phone" label="手机号"> </el-table-column>
            <el-table-column prop="likes" label="爱好"> </el-table-column>
            <el-table-column prop="remark" label="备注"> </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button type="warning" size="mini" @click="openEditLinkmanForm(scope.row)">修改</el-button>
                <el-button type="danger" size="mini">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <!-- 编辑用户对话框 -->
          <el-dialog
            title="修改联系人"
            :visible.sync="openEditCustomereVisible"
            width="30%"
            @close ="clearLinkmanForm"
          >
            <el-form
              :model="linkmanForm"
              :rules="linkmanFormRules"
              ref="editLinkmanFormRef"
              label-width="100px"
              style="width: 90%"
            >
              <el-form-item label="姓名" prop="name">
                <el-input v-model="linkmanForm.name"></el-input>
              </el-form-item>
              <el-form-item label="客户" prop="customer_id">
                <el-select
                  v-model="linkmanForm.customer_id"
                  clearable
                  filterable
                  remote
                  reserve-keyword
                  placeholder="请输入关键词"
                  :remote-method="get_customer_list"
                  style="width: 100%"
                >
                  <el-option
                    v-for="item in customer_list"
                    :key="item.customer_id"
                    :label="item.customer_name"
                    :value="item.customer_id"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="手机号" prop="phone">
                <el-input v-model="linkmanForm.phone"></el-input>
              </el-form-item>
              <el-form-item label="性别" prop="gender">
               <el-select v-model="linkmanForm.gender" style="width: 100%">
                  <el-option :key='index' v-for="(item,index) in gender_list"
                  :label="item.name"
                  :value="item.id"
                  >

                  </el-option>
               </el-select>
              </el-form-item>
              <el-form-item label="QQ" prop="QQ">
                <el-input v-model="linkmanForm.QQ"></el-input>
              </el-form-item>
              <el-form-item label="爱好" prop="likes">
                <el-input v-model="linkmanForm.likes"></el-input>
              </el-form-item>
              <el-form-item label="职位" prop="position">
                <el-input v-model="linkmanForm.position"></el-input>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="openEditCustomereVisible=false">取 消</el-button>
              <el-button type="primary" @click="editLinkman" >修 改</el-button>
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
import { get, post, put } from "../../assets/js/utils";
export default {
  name: "Linkman",
  components: { Crumb },

  data() {
    return {
      linkman_list: [],
      q: "",
      // 分页长度
      page_size: 10,
      // 总数
      total: 0,
      // 当前页
      page: 1,
      // 添加联系人对话框开关
      openAddCustomereVisible: false,
      // 联系人表单
      linkmanForm: {
        name: "",
        phone: "",
        gender: "",
        QQ: "",
        likes: "",
        remark: "",
        customer_id: "",
        position: "",
      },
      customer_list:[],
      linkmanFormRules:{},
      openEditCustomereVisible:false,
      gender_list:[
       {
         'id':1,
         'name':'男'
       },
       {
         'id':2,
         'name':'女'
       },
       {
         'id':3,
         'name':'其他'
       }
      ]
    };
  },

  mounted() {
    this.get_linkman_list();
  },

  methods: {
    async get_linkman_list() {
      const result = await get(
        "linkman/?q=" +
          this.q +
          "&page=" +
          this.page +
          "&size=" +
          this.page_size
      );
      if (result.code != 1000) {
        return this.$message.error(result.msg);
      }
      this.linkman_list = result.data.linkman_list;
      this.page = result.data.page;
      this.total = result.data.total;
    },
    search() {
      this.get_linkman_list();
    },
    handleSizeChange(val) {
      this.page_size = val;
      this.get_linkman_list();
    },
    handleCurrentChange(val) {
      this.page = val;
      this.get_linkman_list();
    },
    // 获取客户列表
    async get_customer_list(query){
      if (!query) {
        return
      }
      
      const result =await get('customers/search/?kw='+query)
      if (result.code!=1000) {
        return
      }
      
      this.customer_list = result.data
      
      
    },
    clearLinkmanForm(){
      this.linkmanForm= {
        name: "",
        phone: "",
        gender: "",
        QQ: "",
        likes: "",
        remark: "",
        customer_id: "",
        position: "",
      }
    },
    // 添加联系人
    addLinkman(){
      this.$refs.linkmanFormRef.validate(async valid=>{
        if (!valid) {return
          
        }
        const  result =await post('linkman/',this.linkmanForm)
        if(result.code!=1000)return this.$message.error(result.msg)
        this.$message.success(result.msg)
        this.clearLinkmanForm()
        this.get_linkman_list()
        this.openAddCustomereVisible = false
      })
    },
    // 取消添加
    cancelAdd(){
      this.clearLinkmanForm()
      this.openAddCustomereVisible = false
    },
    // 获取单条
    async get_one_linkman(id){
      const result  = await get('linkman/'+id)
      if (result.code!=1000) {
        return this.$message.erro(result.msg)
      }
      this.linkmanForm = result.data
      this.get_customer_list(this.linkmanForm.customer_id)
      this.openEditCustomereVisible = true
      
    },
    // 打开修改对话框并回去单条数据
    openEditLinkmanForm(row){
      this.get_one_linkman(row.id)

    },
    editLinkman(){
      this.$refs.editLinkmanFormRef.validate(async valid => {
          if(!valid){return}
          const result  = await put('linkman/'+this.linkmanForm.id,this.linkmanForm)
          if(result.code!=1000){return this.$$message.error(result.msg)}
          this.get_linkman_list()
          this.$message.success(result.msg)
          this.openEditCustomereVisible = false
      })
    }
  },
};
</script>

<style>
.list {
  height: 100%;
  margin-top: 20px;
}
.linkman-table {
  margin-top: 20px;
}
.pagination {
  margin-top: 10px;
}
</style>