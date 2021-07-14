<template>
  <div>
    <crumb></crumb>
    <div class="list">
      <el-card>
          <el-button type="primary" @click="openAddPermission">添加权限</el-button>
           <div class="table-box">
        <el-table :data="permission_list" style="width: 100%" border>
          <el-table-column type="index" label="编号" width="80px"> </el-table-column>
          <el-table-column prop="permission_name" label="权限名称"></el-table-column>
          <el-table-column prop="permission_url" label="权限url"></el-table-column>
          <el-table-column  label="权限等级">
            <template slot-scope="scope">
              <el-tag v-if="scope.row.permission_level==1">一级权限</el-tag>
              <el-tag type="success" v-else-if="scope.row.permission_level==2">二级权限</el-tag>
              <el-tag type="info" v-else>三级权限</el-tag>
            </template>
          </el-table-column>
           <el-table-column prop="permission_icon" label="权限图标"></el-table-column>
            <el-table-column  label="操作">
              <template slot-scope="scope">
              <el-button size="mini" @click="openEditPermission(scope.row)">编辑</el-button>
              <el-button size="mini"  type="danger" @click="delete_permission(scope.row)">删除</el-button>
              </template>
            </el-table-column>
        </el-table>
           </div>
      </el-card>
      <!-- 添加权限 -->
      <el-dialog
  title="添加权限"
  :visible.sync="dialogAddVisible"
  width="30%"
  >
 <el-form  label-width="80px">
  <el-form-item label="权限名称">
    <el-input v-model="permission_form.permission_name"></el-input>
  </el-form-item>
   <el-form-item label="权限url">
    <el-input v-model="permission_form.permission_url"></el-input>
  </el-form-item>
    <el-form-item label="权限等级">
       <el-select v-model="permission_form.permission_level" placeholder="请选择权限等级" @change='search_permission'>
      <el-option label="一级权限" value="1"></el-option>
      <el-option label="二级权限" value="2"></el-option>
      <el-option label="三级权限" value="3"></el-option>
    </el-select>
    
  </el-form-item>
   <el-form-item label="父级权限">
     <el-select v-model="permission_form.permission_parent_id" placeholder="请选择父级权限">
      <el-option :label="per.permission_name" :value="per.id" :key="per.id" v-for="per in permission_parent_id_list"></el-option>
      
    </el-select>
  </el-form-item>
   <el-form-item label="权限图标" >
    <el-input v-model="permission_form.permission_icon" :disabled="isShowIcon"></el-input>
  </el-form-item>
 </el-form>

  <span slot="footer" class="dialog-footer">
    <el-button @click="cancelAddForm">取 消</el-button>
    <el-button type="primary" @click="addPermission">确 定</el-button>
  </span>
</el-dialog>
<!-- 编辑权限 -->
      <el-dialog
  title="编辑权限"
  :visible.sync="dialogeditVisible"
  width="30%"
  >
 <el-form  label-width="80px">
  <el-form-item label="权限名称">
    <el-input v-model="permission_form.permission_name"></el-input>
  </el-form-item>
   <el-form-item label="权限url">
    <el-input v-model="permission_form.permission_url"></el-input>
  </el-form-item>
    <el-form-item label="权限等级">
       <el-select v-model="permission_form.permission_level"  placeholder="请选择权限等级" @change='search_permission'>
      <el-option label="一级权限" :value="1" ></el-option>
      <el-option label="二级权限" :value="2"></el-option>
      <el-option label="三级权限" :value="3"></el-option>
    </el-select>
    
  </el-form-item>
   <el-form-item label="父级权限">
     <el-select v-model="permission_form.permission_parent_id" placeholder="请选择父级权限">
      <el-option :label="per.permission_name" :value="per.id" :key="per.id" v-for="per in permission_parent_id_list"></el-option>
      
    </el-select>
  </el-form-item>
   <el-form-item label="权限图标" >
    <el-input v-model="permission_form.permission_icon"></el-input>
  </el-form-item>
 </el-form>

  <span slot="footer" class="dialog-footer">
    <el-button @click="cancelEditForm">取 消</el-button>
    <el-button type="primary" @click="editPermission">确 定</el-button>
  </span>
</el-dialog>
    </div>
  </div>
</template>
<script>
import crumb from "../crumb.vue";
import { get ,post,_delete,put} from "../../assets/js/utils";

export default {
  name: "WorkspaceJsonPermission",
  components: { crumb },
  data() {
    return {
      permission_list: [],
      // 添加权限对话框
      dialogAddVisible:false,
      // 权限表单
      permission_form:{
        permission_name:'',
        permission_url:'',
        permission_level:'',
        permission_parent_id:'',
        permission_icon:''
        
      },
      isShowIcon:true,
      permission_parent_id_list:[],
      dialogeditVisible:false

    };
  },

  mounted() {
    this.get_permission_list();
  },

  methods: {
    async get_permission_list() {
      const result = await get("permission/list/list/");
      if (result.code != 1000) return this.$message.error(result.msg);
      this.permission_list = result.data;
    },
    openAddPermission(){
      this.dialogAddVisible=true
    },
    async search_permission(val){
      if (val==1) {
        this.permission_parent_id_list= []
        this.isShowIcon=false
      }
      else{
        // console.log(val-1);
        const result = await get(`permission/level/${val-1}/`)
        if (result.code!=1000) {return this.$message.error(result.msg) }
        this.permission_parent_id_list = result.data
        this.isShowIcon=true
      }
      this.permission_form.permission_parent_id=''
      
    },
    // 添加权限
    async addPermission(){
      if (!this.permission_form.permission_parent_id) {
        delete this.permission_form["permission_parent_id"]
      }
      const result  =await post('permission/',this.permission_form)
      if (result.code!=1000) { return this.$message.error(result.msg)
        
      }
      this.$message.success(result.msg)
      this.get_permission_list()
      this.permission_form={
        permission_name:'',
        permission_url:'',
        permission_level:'',
        permission_parent_id:'',
        permission_icon:''
        
      }
      this.dialogAddVisible=false
      
    },
    // 清空权限表单
    cancelAddForm(){
      this.permission_form={
        permission_name:'',
        permission_url:'',
        permission_level:'',
        permission_parent_id:'',
        permission_icon:''
        
      }
      this.dialogAddVisible=false
    },
    // 删除权限
    delete_permission(row){
      console.log(row)
       this.$confirm('此操作将永久删除该权限, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then( async () => {
          const result = await _delete(`permission/${row.id}/`)
          console.log(result)
          if (result.code!==1000) { return this.message.error(result.msg)
            
          }
          this.get_permission_list()
          this.$message({
            type: 'success',
            message: result.msg
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });
    },
    // 获取单挑权限
    async openEditPermission(row){
      const result = await get(`permission/${row.id}`)
      if(result.code!==1000)return this.message.error(result.msg)
      this.permission_form = result.data
      this.dialogeditVisible=true
    },
    cancelEditForm(){
      this.permission_form={
        permission_name:'',
        permission_url:'',
        permission_level:'',
        permission_parent_id:'',
        permission_icon:''
        
      }
      this.dialogeditVisible=false
    },
    async editPermission(){
      if (!this.permission_form.permission_parent_id) {
        delete this.permission_form["permission_parent_id"]
      }
      const result  =await put(`permission/${this.permission_form.id}/`,this.permission_form)
      if (result.code!=1000) { return this.$message.error(result.msg)
        
      }
      this.$message.success(result.msg)
      this.get_permission_list()
      this.permission_form={
        permission_name:'',
        permission_url:'',
        permission_level:'',
        permission_parent_id:'',
        permission_icon:''
        
      }
      this.dialogeditVisible=false
      
    }
  },
};
</script>
<style scoped>
.list {
  height: 100%;
  margin-top: 20px;
}
.table-box{
  margin-top: 10px;
}

</style>