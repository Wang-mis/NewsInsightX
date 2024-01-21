import { createStore } from 'vuex'

// a new store instance
const store = createStore({
    state() {
        return {
            name: "a new store instance.",
            // 新闻文章的列表
            newsList: [],
            // 首页统计信息
            homeStatistics: null,

        }
    },
    mutations:{
        updateNewsList(state, message) {
            state.newsList = message
            // console.log(state.newsList)
        },
        updateHomeStatistics(state, message) {
            state.homeStatistics = message
        },
    }
})
 
export default store