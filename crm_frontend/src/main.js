import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins/element.js'
// 导入全局样式表
import './assets/css/global.css'

// 导入axios包
import axios from 'axios'

axios.defaults.baseURL='http://127.0.0.1:8888/api/'

// 请求拦截器
axios.interceptors.request.use(config => {
  // console.log(config)
  config.headers.Authorization = window.sessionStorage.getItem('token')
  // 在最后必须 return config
  return config
})

// 响应拦截器
axios.interceptors.response.use(config => {
  return config
},error=>{
  
  const result = error.response.data
  console.log(result);
  if(result.code==1002){
    router.push('login')
  }
})




Vue.prototype.$axios = axios

Vue.config.productionTip = false






new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
