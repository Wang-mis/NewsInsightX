<script setup lang="ts">
import { DataAnalysis, Search, User, House, ChatLineSquare } from '@element-plus/icons-vue'
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'

const i18n = useI18n()
const changeLang = (lang) => {
  console.log(lang)
  i18n.locale.value = lang
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

      <el-menu-item index="/analysis">
        <el-icon style="margin-right: 0;">
          <DataAnalysis />
        </el-icon>
      </el-menu-item>

      <!-- TODO 个人主页 -->
      <el-menu-item index="#">
        <el-icon style="margin-right: 0;">
          <User />
        </el-icon>
      </el-menu-item>

      <!-- todo 语言选择框 -->
      <el-sub-menu>
        <template #title>
          <el-icon>
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