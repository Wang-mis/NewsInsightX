<!-- 这是前端页面展示的新闻文章模版 -->
<template>
  <el-card class="article-card" shadow="hover" @click="showArticle"
           @mouseenter="showAddToList = true"
           @mouseleave="showAddToList = false">
    <!-- 标题 -->
    <div ref="titleBox" class="title-container">
      <span v-html="processTitleHighlight(data.Title)"></span>
    </div>

    <!-- 作者 -->
    <div class="new-item author-container">
      <el-icon class="new-item-icon" style="padding-top: 7px;">
        <Avatar />
      </el-icon>
      {{ data.Author }}
    </div>

    <div class="other-info-container">
      <div class="date-and-source">
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
      </div>
      <div style="flex-grow: 1"></div>
      <div ref="addToListRef" class="add-to-list"
           style="display: flex; justify-content: center; align-items: center"
           v-show="showAddToList">
        <el-button :icon="Plus" circle v-if="!inList"
                   @click.stop="store.commit('appendAnalysisNewsIds', [data.UniqueID])"></el-button>
        <el-button :icon="Minus" circle v-if="inList"
                   @click.stop="store.commit('deleteAnalysisNews', data.UniqueID)"></el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { Avatar, Clock, Printer, Plus, Minus } from '@element-plus/icons-vue'
import { publishTimeFormat } from '@/utils/funcsUtil.js'
import 'tippy.js/dist/tippy.css'
import tippy from 'tippy.js'
import 'tippy.js/themes/light.css'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useI18n } from 'vue-i18n'

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

const store = useStore()
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

// region 鼠标悬停时显示标题
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
// endregion

// region 加入清单按钮相关功能实现
const i18n = useI18n()
const showAddToList = ref(false)
const inList = computed(() => store.state.analysisNewsIds.has(props.data.UniqueID))
const addToListRef = ref(null)
let addToListTippy = null

onMounted(() => {
  addToListTippy = tippy(addToListRef.value, {
    theme: 'light',
    content: i18n.t('card.addToList'),
    placement: 'top'
  })
})

watch([i18n.locale, inList], () => {
  if (addToListTippy === null) return
  addToListTippy.setContent(inList.value ? i18n.t('card.removeFromList') : i18n.t('card.addToList'))
})
// endregion

</script>

<style lang="scss" scoped>

.article-card {
  cursor: default;

  .title-container {
    border-bottom: 1px dashed #cccccc;
    line-height: 1.5em;
    height: calc(1.5em * 2 + 5px);
    padding-bottom: 10px;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .author-container {
    line-height: 1.5em;
    height: calc(1.5em * 2 + 10px);
    padding: 10px 0;
    align-items: flex-start;
    overflow: hidden;
  }

  .other-info-container {
    display: flex;
    flex-direction: row;

    .date-and-source {
      display: flex;
      flex-direction: column;
    }
  }
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

</style>
