import {createStore} from 'vuex'
 
// a new store instance
const store = createStore({
    state() {
        return {
            name: 'a new store instance.'
        }
    }
})
 
export default store