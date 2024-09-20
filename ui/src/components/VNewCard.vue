<!-- 这是前端页面展示的新闻文章模版 -->
<template>
  <el-card shadow="hover" @click="dialogVisible = true">
    <div style="border-bottom: 1px dashed #cccccc;">
      <el-icon class="new-item-icon">
        <Document/>
      </el-icon>
      {{ data.Title }}
    </div>

    <div class="new-item">
      <el-icon class="new-item-icon">
        <Avatar/>
      </el-icon>
      {{ data.Author }}
    </div>
    <div class="new-item" style="color: #aaaaaa">
      <el-icon class="new-item-icon">
        <Clock/>
      </el-icon>
      <span class="post-meta">{{ publishTimeFormat(data.DTime) }}</span>
    </div>
    <div class="new-item" style="color: #aaaaaa">
      <el-icon class="new-item-icon">
        <Printer/>
      </el-icon>
      <span class="post-meta"> {{ data.MentionSourceName }} </span>
    </div>
  </el-card>


  <el-dialog
      v-model="dialogVisible"
      :title="data.Title"
      width="60%"
      class="custom-dialog"
      :lock-scroll="false"
      append-to-body
      @close="dialogVisible = false">

    <!--<editor-fold desc="标题">-->
    <template #header>
      <div class="new-item" style="font-size: 22px; color: #222222">
        <el-icon class="new-item-icon">
          <Document/>
        </el-icon>
        {{ data.Title }}
      </div>
    </template>
    <!--</editor-fold>-->

    <div style="display: flex; flex-direction: column;">
      <div style="display: flex; gap: 1rem;">
        <!--<editor-fold desc="来源">-->
        <div class="new-item">
          <el-icon class="new-item-icon">
            <Printer/>
          </el-icon>
          {{ data.MentionSourceName }}
        </div>
        <!--</editor-fold>-->
        <!--<editor-fold desc="作者">-->
        <div class="new-item">
          <el-icon class="new-item-icon">
            <Avatar/>
          </el-icon>
          {{ data.Author }}
        </div>
        <!--</editor-fold>-->
      </div>

      <div style="display: flex; gap: 1rem;">
        <!--<editor-fold desc="时间">-->
        <div class="new-item" style="color: #aaaaaa">
          <el-icon class="new-item-icon">
            <Clock/>
          </el-icon>
          <span class="post-meta">{{ publishTimeFormat(data.DTime) }}</span>
        </div>
        <!--</editor-fold>-->
        <!--<editor-fold desc="网址">-->
        <div class="new-item" style="color: #67C23A">
          <el-icon class="new-item-icon">
            <Link/>
          </el-icon>
          <el-link type="success" :href="data.MentionIdentifier" target="_blank">{{ data.MentionIdentifier }}</el-link>
        </div>
        <!--</editor-fold>-->
      </div>
    </div>

    <div style="margin-top: 0.7rem; white-space: pre-line; font-size: 16px"
         v-html="processArticleContent(data.Content)"></div>

  </el-dialog>

</template>

<script setup lang="ts">
import {ref} from 'vue'
import {Avatar, Clock, Document, Link, Printer} from '@element-plus/icons-vue'
import {publishTimeFormat} from '@/utils/funcsUtil.js'

defineProps({
  data: {
    type: Object,
    required: true
  }
})
const dialogVisible = ref(false)

const processArticleContent = (content) => {
  let newContent = ""
  let lines = content.split('\n')
  lines.forEach(line => {
    line.trim()
    if (line === "") return

    line = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + line + '\n'
    newContent += line
  })

  return newContent
}

</script>

<style lang="scss" scoped>

.new-item-icon {
  margin-right: 0.2rem;
}

.new-item {
  display: flex;
  align-items: center;
}

.post-meta {
  font-size: 14px;
  display: inline-block;
  line-height: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>

<style>
/* 注意使用了全局样式 */
.custom-dialog {
  .el-dialog__body {
    padding-top: 0;
  }
}
</style>