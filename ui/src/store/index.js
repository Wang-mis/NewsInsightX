import { createStore } from 'vuex'

const store = createStore({
  state() {
    return {
      newsList: [],
      homeStatistics: null,
      userinfo: null,
      login: false
    }
  },
  mutations: {
    updateNewsList: (state, message) => state.newsList = message,
    updateHomeStatistics: (state, message) => state.homeStatistics = message,
    updateUserInfo: (state, message) => state.userinfo = message,
    updateLogin: (state, message) => state.login = message
  }
})

export default store