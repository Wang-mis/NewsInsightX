<template>
  <div class="search-container">
    <div class="search-form-comtainer">
      <el-form :inline="true" :model="formInline" class="demo-form-inline">
        <el-form-item label="关键词：">
          <el-input v-model="formInline.keyword" placeholder="人物名称、热点词、热点事件" clearable />
        </el-form-item>
        <el-form-item label="时间点：">
          <el-date-picker
            v-model="formInline.date"
            type="date"
            placeholder="选择日期"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">查询</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="news-cards-container">

      <VNewCard :data="item" v-for="(item, index) in cardList"/>

    </div>

    <div class="demo-pagination-block">
      <el-pagination
        v-model:current-page="pageModel.page"
        v-model:page-size="pageModel.limit"
        :page-sizes="[20, 40, 80, 100]"
        background
        layout="total, sizes, prev, pager, next, jumper"
        :total="pageModel.total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

  </div>
</template>

<script lang="ts" setup>
import VNewCard from '../components/VNewCard.vue'
import { generateRandomString } from '@/utils/funcsUtil'
import { queryNews } from '@/api/requestAPI'

import { reactive, ref, onMounted } from 'vue'

const cardList = ref<any>([])

const formInline = reactive({
  keyword: '',
  date: '',
})

const pageModel = reactive({
  page: 1,//默认当前页码
  limit: 20,//默认每页的数量
  total: 0//返回的总记录数（未分页）
})

onMounted( async () => {
  await getNewsList()
})

// 请求后端新闻文章
const getNewsList = async () => {
  const config_data = {...formInline, ...pageModel}
  await gainNewsList(config_data)
}

async function gainNewsList(config_data) {
  await queryNews(config_data).then(res => {
    if (res.code === 0) {
      console.log("查询到的新闻文章：", res.data)
      cardList.value = res.data["newsList"]
      pageModel.total = res.data["totalRecords"]
    }
  })
}


const onSubmit = async () => {
  console.log('submit!')
  await getNewsList()
}


const handleSizeChange = (val: number) => {
  pageModel.limit = val
  console.log(`${val} items per page`)
}
const handleCurrentChange = (val: number) => {
  pageModel.page = val
  console.log(`current page: ${val}`)
}
</script>

<style scoped>
.news-cards-container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
  grid-gap: 1rem;
}
.search-container {
  margin: 1rem 1rem 0 1rem;
}
.demo-form-inline .el-input {
  --el-input-width: 220px;
}

.demo-form-inline .el-select {
  --el-select-width: 220px;
}


.demo-pagination-block {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
