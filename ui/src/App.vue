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
        <h2>NewsInsightX: The Latest Global News Portal System Featuring Hot News</h2>
        <!-- <h2>NewsInsightX: 以热点新闻为特色的最新全球新闻门户系统</h2> -->
      </el-menu-item>
      <div class="flex-grow"></div>
      <el-menu-item index="/about">
        <h2>Search</h2>
      </el-menu-item>
      <el-menu-item index="/test">
        <h2>Analysis</h2>
      </el-menu-item>
    </el-menu>
  </header>

  <div id="home-container">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'

const handleSelect = (key, keyPath) => {
  console.log(key, keyPath)
}

</script>

<style scoped>

.home-header{
  top: 1rem;
  position: sticky;
  .flex-grow {
    flex-grow: 1;
  }
}

</style>
