import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Cookies from 'js-cookie'
import { useStore } from 'vuex'
import { queryCheckToken } from '@/utils/axiosUtil'
import { ElNotification } from 'element-plus'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/SearchView.vue')
    },
    {
      path: '/analysis',
      name: 'analysis',
      component: () => import('../views/AnalysisView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  // 跳转到登录页面，不受影响
  if (to.path === '/login') {
    next()
    return
  }

  const store = useStore()
  if (store.state.login) {
    // 已登录，允许跳转
    next()
    return
  }


  const token = Cookies.get('token')
  // 无token
  if (token === undefined) {
    ElNotification({
      title: '未登录',
      message: '将跳转至登录页面',
      type: 'error',
      duration: 1500
    })
    // 延迟跳转登录页面
    setTimeout(() => {
      next({ path: '/login' })
    }, 1500)
    return
  }

  // 检查token
  queryCheckToken(token).then((res) => {
    if (res.code === 0) {
      next()
      return
    }

    if (res.code === 1) {
      ElNotification({
        title: '未登录',
        message: 'token错误！将跳转至登录页面',
        type: 'error',
        duration: 1500
      })
    } else if (res.code === 2) {
      ElNotification({
        title: '未登录',
        message: 'token过期！将跳转至登录页面',
        type: 'error',
        duration: 1500
      })
    } else {
      ElNotification({
        title: '未登录',
        message: '未知错误！将跳转至登录页面',
        type: 'error',
        duration: 1500
      })
    }

    // 延迟跳转登录页面
    setTimeout(() => {
      console.log('-----------------------------')
      next({ path: '/login' })
    }, 1500)
  })
})

export default router
