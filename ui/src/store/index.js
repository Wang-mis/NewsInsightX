import { createStore } from 'vuex'

// 从本地读取新闻清单
const analysisNewsIds = localStorage.getItem('analysisNewsIds') ?
  JSON.parse(localStorage.getItem('analysisNewsIds')) : []

const store = createStore({
  state() {
    return {
      analysisNewsIds,
      homeStatistics: null,
      userinfo: null
    }
  },
  mutations: {
    // 添加新闻到清单
    appendAnalysisNewsIds: (state, ids) => {
      // 去除重复元素
      ids.forEach(newsId => {
        if (state.analysisNewsIds.some(id => id === newsId)) return
        state.analysisNewsIds.push(newsId)
      })
      // 将清单添加到本地存储
      localStorage.setItem('analysisNewsIds', JSON.stringify(state.analysisNewsIds))
    },
    // 清空清单
    removeAnalysisNewsIds: (state) => {
      state.analysisNewsIds = []
      localStorage.removeItem('analysisNewsIds')
    },

    updateHomeStatistics: (state, message) => state.homeStatistics = message,
    updateUserInfo: (state, message) => state.userinfo = message,
    clearUserInfo: (state) => state.userinfo = null
  }
})

export default store