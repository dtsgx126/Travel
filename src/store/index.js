import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    city: '杭州'
  },
  actions: {
    changeCity: function (ctx, city) {
      ctx.commit('changeCity', city)
    }
  },
  mutations: {
    changeCity: function (state, city) {
      state.city = city
    }
  }
})
