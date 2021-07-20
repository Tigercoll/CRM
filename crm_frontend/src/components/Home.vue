<template>
  <el-container class="container">
    <!-- 头部区域 -->
    <el-header>
      <div class="logout">
        <font class="title">CRM</font>
        <el-button @click="logout" type="info" class="logout"
          >退出登录</el-button
        >
      </div>
    </el-header>
    <!-- 左侧菜单栏 -->
    <el-container>
      <el-aside :width="isCollapse ? '64px':'200px' ">
       <!-- 收缩按钮 -->
       <div class="collapse">
          <el-radio-group v-model="isCollapse" style="margin: 20px;">
  <el-radio-button :label="false">展开</el-radio-button>
  <el-radio-button :label="true">收起</el-radio-button>
</el-radio-group>
           </div>
        <el-menu
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#409eff"
          :unique-opened="true"
          :collapse="isCollapse"
          :collapse-transition="false"
          router
        >
          <el-submenu
            :index="'/' + item.permission_url"
            v-for="item in menu_list"
            :key="item.id"
          >
            <template slot="title">
              <i :class="item.permission_icon"></i>
              <span>{{ item.permission_name }}</span>
            </template>
            <el-menu-item-group v-for="child in item.children" :key="child.id" >
              <el-menu-item :index="'/' + child.permission_url" @click="add_crumb(item,child)">
                <template slot="title">
                  <i class="el-icon-menu"></i>
                  <span >{{ child.permission_name }}</span>
                </template>
              </el-menu-item>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
      </el-aside>
      <!-- 右侧主体 -->
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { get } from "../assets/js/utils";
export default {
  name: "Home",
  data() {
    return {
      menu_list: [],
      isCollapse: false,
      
    };
  },

  mounted() {
    this.get_menu();
  },

  methods: {
    // 退出
    logout() {
      window.sessionStorage.clear();
      this.$router.push({ path: "login" });
    },
    // 获取菜单栏
    async get_menu() {
      const result = await get("menu/");
      if (result.code !== 1000) {
        this.$message.error(result.msg);
      }
      this.menu_list = result.data;
    },
    add_crumb(item,child){
      window.sessionStorage.setItem('crumb','')
      const crumb = JSON.stringify([item.permission_name,child.permission_name])
      window.sessionStorage.setItem('crumb',crumb)
    }

  },

};
</script>
<style>
.container {
  height: 100%;
}
.el-header {
  background-color: rgb(33, 57, 126);
}
.logout {
  display: flex;
  justify-content: space-between;
  padding: 6px;
}
.title {
  font-size: 40px;
  color: #fff;
}

.el-aside {
  background-color: #545c64;
}

.collapse{
    display: flex;
    justify-content: center;
}
.el-aside .el-menu{
border-right: none;
}

.el-main {
  background-color: #eaedf1;
}
</style>