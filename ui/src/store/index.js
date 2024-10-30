import { createStore } from 'vuex'

// 从本地读取新闻清单
const analysisNewsIds = localStorage.getItem('analysisNewsIds') ?
  JSON.parse(localStorage.getItem('analysisNewsIds')) : []

const store = createStore({
  state() {
    return {
      analysisNewsIds: new Set(analysisNewsIds),
      homeStatistics: null,
      userinfo: null
    }
  },
  mutations: {
    // 添加新闻到清单
    appendAnalysisNewsIds: (state, ids) => {
      ids.forEach(newsId => state.analysisNewsIds.add(newsId))
      // 将清单添加到本地存储
      localStorage.setItem('analysisNewsIds', JSON.stringify([...state.analysisNewsIds]))
    },
    // 删除清单中的某个元素
    deleteAnalysisNews: (state, id) => {
      state.analysisNewsIds.delete(id)
      localStorage.setItem('analysisNewsIds', JSON.stringify([...state.analysisNewsIds]))
    },
    // 清空清单
    removeAnalysisNewsIds: (state) => {
      state.analysisNewsIds = new Set()
      localStorage.removeItem('analysisNewsIds')
    },

    updateHomeStatistics: (state, message) => state.homeStatistics = message,
    updateUserInfo: (state, message) => state.userinfo = message,
    clearUserInfo: (state) => state.userinfo = null
  }
})

export default store