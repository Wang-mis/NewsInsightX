<script setup lang="ts">
import { DataAnalysis, Search, User, House, ChatLineSquare } from '@element-plus/icons-vue'
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useStore } from 'vuex'
import { ElNotification } from 'element-plus'
import axios from 'axios'
import { request, updateBiaseerData } from '@/utils/axiosUtil'
import SvgIcon from '@/components/SvgIcon.vue'
import { useRoute, useRouter } from 'vue-router'

const i18n = useI18n()
const store = useStore()
const router = useRouter()
const changeLang = (lang) => i18n.locale.value = lang
const newsCount: Number = computed(() => store.state.analysisNewsIds.size)
const removeList = () => {
  store.commit('removeAnalysisNewsIds')
  ElNotification({
    title: i18n.t('navbar.analysis.notifications.clear.title'),
    message: i18n.t('navbar.analysis.notifications.clear.message'),
    type: 'warning',
    duration: 1500
  })
}

const sendList = async () => {
  const newsIds = []
  // 将数据传输给Biaseer的后端服务器
  const data = { 'ids': [...store.state.analysisNewsIds] }
  // Biaseer部署在本地，需要Chrome浏览器开启跨域--disable-web-security
  const uri = 'http://10.108.17.47:14449/update_data'
  axios.post(uri, data).then(response => console.log(response)).catch(error => console.log(error))
  // Biaseer部署在云服务器上
  // await updateBiaseerData(data).then(res => {
  //   console.log(res)
  // })
}

const toShowList = () => {
  const currentPath = window.location.pathname
  const targetPath = '/search/true'
  if (currentPath === targetPath) window.location.reload()
  else router.push({ name: 'search', params: { queryInList: true } })
}
</script>

<template>
  <header class="nav-bar">
    <el-menu
      class="nav-bar-menu"
      mode="horizontal"
      :ellipsis="false"
      :router="true"
      default-active="/"
    >
      <el-menu-item index="/">
        <el-icon style="margin-right: 0;">
          <House />
        </el-icon>
      </el-menu-item>

      <div style="flex-grow: 1"></div>

      <el-menu-item index="/search/false">
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

      <!-- 清单信息 -->
      <el-dropdown style="padding: 0 8px;">
            <span class="el-dropdown-link" style="color: black">
              <el-icon style="margin: 0; padding: 0;" :size="18"><DataAnalysis /></el-icon>
            </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item
              style="display: flex; justify-content: space-between"
              @click="toShowList">
              <span style="margin-right: 15px;">{{ $t('navbar.analysis.showList') }}</span>
              <span
                style="font-size: 12px; color: #909399">{{ $t('navbar.analysis.listCountPrefix') + String(newsCount) + $t('navbar.analysis.listCountSuffix')
                }}</span>
            </el-dropdown-item>
            <el-dropdown-item style="display: flex; justify-content: start" @click="removeList">
              {{ $t('navbar.analysis.clearList') }}
            </el-dropdown-item>
            <el-dropdown-item style="display: flex; justify-content: start" @click="sendList">
              {{ $t('navbar.analysis.sendList') }}
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>

      <!-- 语言选择框 -->
      <el-dropdown style="padding: 0 8px;">
            <span class="el-dropdown-link">
              <svg-icon icon="translate" width="20px" height="20px" />
            </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item style="display: flex; justify-content: center" @click="changeLang('zh')">
              中文
            </el-dropdown-item>
            <el-dropdown-item style="display: flex; justify-content: center" @click="changeLang('en')">
              English
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
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

  .el-dropdown-link {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;

    cursor: pointer;
    display: flex;
    align-items: center;
  }

  .el-dropdown-link:hover {
    border: none;
    background-color: transparent;
  }
}
</style>