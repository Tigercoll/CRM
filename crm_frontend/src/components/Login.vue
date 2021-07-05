<template>
  <div class="login-container">
    <div class="login-box">
      <el-form class="login-form" ref="login_ref" :rules="login_rules" :model="login_form">
        <el-form-item prop="user_name">
          <el-input v-model="login_form.user_name" prefix-icon="el-icon-user">
          </el-input>
        </el-form-item>
        <el-form-item prop="user_pwd">
          <el-input
            type="password"
            v-model="login_form.user_pwd"
            prefix-icon="el-icon-lock"
          >
          </el-input>
        </el-form-item>
        <el-form-item class="btns">
          <el-button type="primary" @click="login"> 登录 </el-button>
          <el-button type="info" @click="resetLoginForm"> 重置 </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import post from "../assets/js/utils.js"

export default {
  name: "Login",

  data() {
    return {
      login_form: {
        user_name: "",
        user_pwd: "",
      },
      // 表单验证对象
      login_rules: {
        // 验证用户名不能为空
        user_name: [
          { required: true, message: "用户名不能为空", trigger: "blur" },
        ],
        // 验证密码不能为空
        user_pwd: [
          { required: true, message: "密码不能为空", trigger: "blur" },
        ],
      },
    };
  },

  mounted() {},

  methods: {
    //   点击重置按钮重置表单
      resetLoginForm(){
          this.$refs.login_ref.resetFields()
      },
    //   登录
    login(){
        // 通过validate校验
         this.$refs.login_ref.validate(async valid=>{
            if(!valid){
                return
            }
           
                const result =await post('login/',this.login_form)
            console.log(result)
            
})
    }
  },
};
</script>

<style>
.login-container {
  background-color: #2b4b6b;
  height: 100%;
}
.login-box {
  height: 300px;
  width: 450px;
  background-color: #fff;
  border: 3px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.login-form {
  position: absolute;
  bottom: 25px;
  width: 100%;
  padding: 0 20px;
  box-sizing: border-box;
}
.btns {
  display: flex;
  justify-content: flex-end;
}
</style>