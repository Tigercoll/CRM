import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import dash from '../components/dash.vue'
import User from '../components/users/user.vue'
import Role from '../components/roles/role.vue'
import Permission from '../components/permissions/permission.vue'
Vue.use(VueRouter)

const routes = [
  // 重定向到login
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/home', component: Home ,redirect: '/welcome',
  children:[
    { path: '/welcome', component: dash },
    { path: '/users', component: User },
    { path: '/roles', component: Role },
    { path: '/permission', component: Permission }
  ]}
]

const router = new VueRouter({
  mode: 'history',
  routes
})

// GOOD
router.beforeEach((to, from, next) => {
  const token = window.sessionStorage.getItem('token')
  // 获取url 如果不是login 或者没有token 跳转到login
  if (to.path!== '/login' && !token) next('/login')
  else next()
})


export default router
