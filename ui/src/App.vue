<template>
  
  <header class="home-header">
    <el-menu
      class="el-menu-demo"
      background-color="#545c64"
      text-color="#fff"
      mode="horizontal"
      :ellipsis="false"
      :router="true"
      @select="handleSelect"
    >
      <el-menu-item index="/">
        <!-- <img
          style="width: 100px; margin-right: 3px;"
          src="@/assets/element-plus-logo.svg"
          alt="Element logo"
        /> -->
        <!-- <el-icon style="font-size: 2em;"><DataLine /></el-icon> -->
        <h2>NewsInsightX: The Latest Global News Portal System Featuring Hot News</h2>
      </el-menu-item>
      <div class="flex-grow"></div>

      <el-menu-item @click="handelSync">
        <el-icon style="font-size: 2em;"><Refresh /></el-icon><h2>Sync</h2>
      </el-menu-item>
      
      <el-menu-item index="/search">
        <el-icon style="font-size: 2em;"><Search /></el-icon><h2>Search</h2>
      </el-menu-item>
      <el-menu-item index="/analysis">
        <el-icon style="font-size: 2em;"><DataAnalysis /></el-icon><h2>Analysis</h2>
      </el-menu-item>
      <!-- 中英文翻译 -->
      <!-- <el-menu-item @click="exportDataSet"><el-icon style="font-size: 2em;"><Download /></el-icon></el-menu-item> -->
    </el-menu>
  </header>

  <div id="home-container">
    <RouterView />
  </div>
</template>

<script setup>
import { Refresh, Search, DataAnalysis, DataLine } from '@element-plus/icons-vue'
import { RouterView } from 'vue-router'
import { ElNotification } from 'element-plus'


const handleSelect = (key, keyPath) => {
  console.log(key, keyPath)
}

const handelSync = () => {
  ElNotification({
    title: "更新数据",
    type: "success",
    duration: 1000
  })
}
</script>

<style scoped>

.home-header{
  top: 1rem;
  /* position: sticky; */
  .flex-grow {
    flex-grow: 1;
  }
}

</style>
