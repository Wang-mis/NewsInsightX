<!-- 这是前端页面展示的新闻文章模版 -->
<template>
  <el-card class="article-card" shadow="hover" @click="showArticle()">
    <div
      ref="titleBox"
      style="border-bottom: 1px dashed #cccccc; line-height: 1.5em; height: calc(1.5em * 2 + 5px); padding-bottom: 10px; overflow: hidden; text-overflow: ellipsis;"
    >
      <span v-html="processTitleHighlight(data.Title)"></span>
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
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Avatar, Clock, Link, Printer } from '@element-plus/icons-vue'
import { publishTimeFormat } from '@/utils/funcsUtil.js'
import 'tippy.js/dist/tippy.css'
import tippy from 'tippy.js'
import 'tippy.js/themes/light.css'
import { useRouter } from 'vue-router'

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

const router = useRouter()
const showArticle = () => {
  const url = router.resolve({ name: 'article', params: { id: props.data.UniqueID } }).href
  window.open(url, '_blank')
}

const processTitleHighlight = (title: string) => {
  props.keywords.forEach(keyword => {
    if (keyword !== '') {
      title = title.replace(new RegExp(keyword, 'gi'),
        (match) => '<span style="background-color: yellow;">' + match + '</span>')
    }
  })

  return title
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
