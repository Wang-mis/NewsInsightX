<script setup lang="ts">
import { useRoute } from 'vue-router'
import { queryHomeStatistics, queryNewsById } from '@/utils/axiosUtil'
import { deepCopy } from '@/utils/funcsUtil'
import { ref } from 'vue'

const route = useRoute()
const data = ref(null)


// 请求文章数据
async function getArticleData() {
  const id = route.params.id
  const configData = { id }
  await queryNewsById(configData).then(res => {
    if (res.code === 0) return  // todo
  })
}

</script>

<template>

  <h2>AAA{{ id }}</h2>
</template>

<style scoped lang="scss">

</style>