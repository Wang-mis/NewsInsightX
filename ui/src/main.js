import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { createI18n } from 'vue-i18n'
// import VTooltip from 'v-tooltip'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 中文
import locale from 'element-plus/es/locale/lang/zh-cn'
import zh from '@/language/zh'
import en from '@/language/en'


const app = createApp(App)

app.use(router)
app.use(store)
app.use(ElementPlus, { locale })

// 设置语言配置
const messages = { zh, en }
const i18n = createI18n({
  legacy: false,
  messages,
  locale: navigator.language
})

app.use(i18n)
// app.use(VTooltip)

app.mount('#app')
