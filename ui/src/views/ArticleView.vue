<script setup lang="ts">
import { useRoute } from 'vue-router'
import { queryNewsById } from '@/utils/axiosUtil'
import { onBeforeMount, onMounted, reactive } from 'vue'

const route = useRoute()
const data = reactive({
  uniqueId: '',
  title: '',
  author: '',
  ptime: '',
  dtime: '',
  mentionSourceName: '',
  mentionIdentifier: '',
  paragraphs: []
})

onBeforeMount(async () => getArticleData())

// 请求文章数据
async function getArticleData() {
  const id = route.params.id
  const configData = { id }
  console.log('请求文章数据中。')
  await queryNewsById(configData).then(res => {
    if (res.code !== 0) {
      console.log('请求文章数据失败！')
      return
    }

    data.uniqueId = res.data['UniqueID']
    data.title = res.data['Title']
    document.title = data.title
    data.author = processAuthor(res.data['Author'])
    data.ptime = res.data['PTime']
    data.dtime = processDate(String(res.data['DTime']))
    data.mentionSourceName = res.data['MentionSourceName']
    data.mentionIdentifier = res.data['MentionIdentifier']
    data.paragraphs = processArticleContent(res.data['Content'])
    console.log('请求文章数据成功。')
  })
}

const processArticleContent = (content: string) => {
  let lines = content.split('\n')
  return lines.map(line => line.trim())
}

const formatUrl = (url, frontLen, rearLen) => {
  if (url.length > frontLen + rearLen)
    return url.slice(0, frontLen) + '......' + (rearLen > 0 ? url.slice(-rearLen) : '')
  return url
}

const processDate = (date: string) => date.slice(0, 4) + '-' + date.slice(4, 6) + '-' + date.slice(6, 8)

const processAuthor = (author: string) => {
  author = author.trim().replace(/^by/i, '').trim()
  return author.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ')
}


</script>

<template>
  <div class="article-page-container">
    <div class="left-container"></div>
    <div class="article-container">
      <h1 class="title">{{ data.title }}</h1>
      <div class="info">
        <span class="author" v-if="data.author !== '_'">By {{ data.author }}</span>
        <span style="flex-grow: 1"></span>
        <span class="date">{{ data.dtime }}</span>
        <span class="identifier"><a :href="data.mentionIdentifier" target="_blank">goto original page</a></span>
      </div>
      <div class="content">
        <p class="paragraph" v-for="p in data.paragraphs">
          {{ p }}
        </p>
      </div>
    </div>
    <div class="right-container"></div>
  </div>
</template>

<style scoped lang="scss">
@import "public/styles/variables";

.article-page-container {
  width: 100%;
  height: calc(100vh - $navbar-height);

  display: flex;
  flex-direction: row;
  justify-content: center;

  .article-container {
    width: 50%;
    height: 100%;

    .title {
      padding-top: 20px;
      font-size: 30px;
      font-weight: bold;
      text-align: justify;

    }

    .info {
      font-size: 14px;
      color: #909399;

      display: flex;
      flex-direction: row;

      padding: 15px;

      .date {
        margin-right: 15px;
      }
    }

    .paragraph {
      font-family: "Inter", sans-serif;
      white-space: pre-line;
      font-size: 17px;
      line-height: 1.6;
      text-align: justify;
      text-indent: 2em;
      padding: 0 1em;
      color: #222222;
      margin-bottom: 0.7rem;
    }
  }
}
</style>