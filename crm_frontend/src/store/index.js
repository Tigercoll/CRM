import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    breadcrumb_list:[]
  },
  mutations: {
    add_breadcrumb_list(state,params){
      state.breadcrumb_list=params
    }
  },
  actions: {
  },
  modules: {
  }
})
