<!-- 这是前端页面展示的新闻文章模版 -->
<template>
  <el-card class="article-card" shadow="hover" @click="dialogVisible = true">
    <div
      ref="titleBox"
      style="border-bottom: 1px dashed #cccccc; line-height: 1.5em; height: calc(1.5em * 2 + 5px); padding-bottom: 10px; overflow: hidden; text-overflow: ellipsis;"
    >
      <span v-html="processTitle(data.Title)"></span>
    </div>

    <div class="new-item"
         style="line-height: 1.5em; height: calc(1.5em * 2 + 10px); padding: 10px 0; align-items: flex-start;overflow: hidden;">
      <el-icon class="new-item-icon" style="padding-top: 7px;">
        <Avatar />
      </el-icon>
      {{ data.Author }}
    </div>

    <div class="new-item" style="color: #aaaaaa">
      <el-icon class="new-item-icon">
        <Clock />
      </el-icon>
      <span class="post-meta">{{ publishTimeFormat(data.DTime) }}</span>
    </div>
    <div class="new-item" style="color: #aaaaaa">
      <el-icon class="new-item-icon">
        <Printer />
      </el-icon>
      <span class="post-meta"> {{ data.MentionSourceName }} </span>
    </div>
  </el-card>


  <el-dialog
    v-model="dialogVisible"
    :title="data.Title"
    width="50%"
    class="custom-dialog"
    :lock-scroll="false"
    append-to-body
    @close="dialogVisible = false"
  >

    <!--<editor-fold desc="标题">-->
    <template #header>
      <div class="new-item" style="font-size: 23px; color: black">
        <el-icon class="new-item-icon">
          <Document />
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
            <Printer />
          </el-icon>
          {{ data.MentionSourceName }}
        </div>
        <!--</editor-fold>-->
        <!--<editor-fold desc="作者">-->
        <div class="new-item">
          <el-icon class="new-item-icon">
            <Avatar />
          </el-icon>
          {{ data.Author }}
        </div>
        <!--</editor-fold>-->
      </div>

      <div style="display: flex; gap: 1rem;">
        <!--<editor-fold desc="时间">-->
        <div class="new-item" style="color: #aaaaaa">
          <el-icon class="new-item-icon">
            <Clock />
          </el-icon>
          <span class="post-meta" style="white-space: nowrap">{{ publishTimeFormat(data.DTime) }}</span>
        </div>
        <!--</editor-fold>-->
        <!--<editor-fold desc="网址">-->
        <div class="new-item" style="color: #67C23A">
          <el-icon class="new-item-icon">
            <Link />
          </el-icon>
          <el-link type="success" :href="data.MentionIdentifier" target="_blank" style="white-space: nowrap">
            {{ formatUrl(data.MentionIdentifier, 60, 30) }}
          </el-link>
        </div>
        <!--</editor-fold>-->
      </div>
    </div>

    <div
      style="
        margin-top: 0.7rem;
        white-space: pre-line;
        font-size: 17px;
        line-height: 1.6;
        text-align: justify;
        text-indent: 2em;
        padding: 0 1em;
        color: #222222;
      "
    >
      <p v-for="line in processArticleContent" style="padding-bottom: 0.5em">
        {{ line }}
      </p>
    </div>

  </el-dialog>

</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { Avatar, Clock, Document, Link, Printer } from '@element-plus/icons-vue'
import { publishTimeFormat } from '@/utils/funcsUtil.js'
import 'tippy.js/dist/tippy.css'
import tippy from 'tippy.js'
import 'tippy.js/themes/light.css'

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  keywords: {
    type: Array,
    default: []
  }
})
const dialogVisible = ref(false)

const processArticleContent = computed(() => {
  let lines = props.data.Content.split('\n')
  lines = lines.map(line => line.trim())
  return lines
})

const processTitle = (title: string) => {
  props.keywords.forEach(keyword => {
    if (keyword !== '') {
      title = title.replace(new RegExp(keyword, 'gi'),
        (match) => '<span style="background-color: yellow;">' + match + '</span>')
    }
  })

  return title
}

const formatUrl = (url, frontLen, rearLen) => {
  if (url.length > frontLen + rearLen)
    return url.slice(0, frontLen) + '......' + (rearLen > 0 ? url.slice(-rearLen) : '')
  return url
}

const titleBox = ref(null)

onMounted(() => {
  tippy(titleBox.value, {
    theme: 'light',
    content: props.data.Title,
    placement: 'right',
    arrow: false,
    delay: [400, 0]
  })
})

</script>

<style lang="scss" scoped>

.article-card {
  cursor: default;
}

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