<script setup lang="ts">
import { DataAnalysis, Search, User, House, ChatLineSquare } from '@element-plus/icons-vue'
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useStore } from 'vuex'
import { ElNotification } from 'element-plus'
import axios from 'axios'
import { request, updateBiaseerData } from '@/utils/axiosUtil'

const i18n = useI18n()
const store = useStore()
const changeLang = (lang) => i18n.locale.value = lang
const newsCount: Number = computed(() => store.state.analysisNewsIds.length)
const removeList = () => {
  store.commit('removeAnalysisNewsIds')
  ElNotification({
    title: '新闻清单已清空',
    message: '',
    type: 'warning',
    duration: 1500
  })
}

const sendList = async () => {
  const newsIds = []
  // 将数据传输给Biaseer的后端服务器
  const data = { 'ids': store.state.analysisNewsIds }
  // Biaseer部署在本地，需要Chrome浏览器开启跨域--disable-web-security
  const uri = 'http://10.108.17.47:14449/update_data'
  axios.post(uri, data).then(response => console.log(response)).catch(error => console.log(error))
  // Biaseer部署在云服务器上
  // await updateBiaseerData(data).then(res => {
  //   console.log(res)
  // })
}

</script>

<template>
  <header class="nav-bar">
    <el-menu
      mode="horizontal"
      :ellipsis="false"
      :router="true"
    >
      <el-menu-item index="/">
        <el-icon style="margin-right: 0;">
          <House />
        </el-icon>
      </el-menu-item>

      <div style="flex-grow: 1"></div>

      <el-menu-item index="/search">
        <el-icon style="margin-right: 0;">
          <Search />
        </el-icon>
      </el-menu-item>

      <!-- TODO 个人主页 -->
      <el-menu-item index="#">
        <el-icon style="margin-right: 0;">
          <User />
        </el-icon>
      </el-menu-item>

      <el-sub-menu index="/analysis" style="margin: 0; padding: 0;">
        <template #title>
          <el-icon style="margin: 0; padding: 0;">
            <DataAnalysis />
          </el-icon>
        </template>

        <el-menu-item>清单内共{{ newsCount }}条新闻</el-menu-item>
        <el-menu-item @click="removeList">清空新闻清单</el-menu-item>
        <el-menu-item @click="sendList">发送数据</el-menu-item>
      </el-sub-menu>

      <!-- todo 语言选择框 -->
      <el-sub-menu style="margin: 0; padding: 0;">
        <template #title>
          <el-icon style="margin: 0; padding: 0;">
            <ChatLineSquare />
          </el-icon>
        </template>

        <el-menu-item @click="changeLang('zh')">简体中文</el-menu-item>
        <el-menu-item @click="changeLang('en')">English</el-menu-item>
      </el-sub-menu>
    </el-menu>
  </header>
</template>

<style scoped lang="scss">
.nav-bar {
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .05);

  --el-menu-horizontal-height: 40px;
  --el-menu-bg-color: white;
  --el-menu-text-color: black;

  position: fixed;
  width: 100%;
  height: 40px;
  z-index: 100;
  top: 0;
  left: 0;

  .el-menu {
    padding: 0 20px;
  }

  .el-menu-item {
    padding: 0 5px;
  }

  el-icon {
    font-size: 2em;
  }
}
</style>