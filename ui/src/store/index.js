import { createStore } from 'vuex'

// a new store instance
const store = createStore({
    state() {
        return {
            name: "a new store instance.",
            // 新闻文章的列表
            newsList: [],
        }
    },
    mutations:{
        updateNewsList(state, message) {
            state.newsList = message
            // console.log(state.newsList)
        },
    }
})
 
export default store