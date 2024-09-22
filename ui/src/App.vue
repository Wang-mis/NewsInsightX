<template>

  <header class="home-header" style="top: 1rem;">
    <el-menu
      class="el-menu-demo"
      background-color="#545c64"
      text-color="#fff"
      mode="horizontal"
      :ellipsis="false"
      :router="true"
    >
      <el-menu-item index="/">
        <h2 class>NewsInsightX: The Latest Global News Portal System Featuring Hot News</h2>
      </el-menu-item>

      <div style="flex-grow: 1"></div>


      <el-menu-item index="/search">
        <el-icon style="font-size: 2em;">
          <Search />
        </el-icon>
        <h2>Search</h2>
      </el-menu-item>

      <el-menu-item index="/analysis">
        <el-icon style="font-size: 2em;">
          <DataAnalysis />
        </el-icon>
        <h2>Analysis</h2>
      </el-menu-item>


      <el-menu-item @click="handelSync">
        <el-icon style="font-size: 2em;">
          <Refresh />
        </el-icon>
        <h2>Synchronize</h2>
      </el-menu-item>

      <!-- TODO 个人主页 -->
      <el-menu-item index="/">
        <el-icon style="font-size: 2em;">
          <User />
        </el-icon>
        <h2>{{ 'User : ' + getUsername }}</h2>
      </el-menu-item>
    </el-menu>

  </header>

  <div id="home-container">
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { Refresh, Search, DataAnalysis, User } from '@element-plus/icons-vue'
import { RouterView, useRouter } from 'vue-router'
import { ElNotification } from 'element-plus'
import { useStore } from 'vuex'
import { computed } from 'vue'

const store = useStore()

const getUsername = computed(() => {
  if (store.state.userinfo === null ||
    store.state.userinfo === undefined ||
    !('username' in store.state.userinfo))
    return 'Not Login'
  return store.state.userinfo.username
})


const handelSync = () => {
  // TODO: 更新数据

  ElNotification({
    title: '更新数据',
    type: 'success',
    duration: 1000
  })
}
</script>

<style scoped>

</style>
