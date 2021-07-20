<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item
        :key="index"
        v-for="(item, index) in breadcrumb_list"
        >{{ item }}</el-breadcrumb-item
      >
    </el-breadcrumb>
  </div>
</template>
<script>
export default {
  name: "users",
  data() {
    return {
      breadcrumb_list: [],
    };
  },

  mounted() {
    const crumb_list = window.sessionStorage.getItem("crumb");
    this.breadcrumb_list = JSON.parse(crumb_list);
  },

  methods: {},
  computed: {},
};
</script>