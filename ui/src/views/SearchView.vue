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

    <div v-if="cardList.length < 1">
      <el-empty description="暂无数据" :image-size="200" />
    </div>

    <div class="news-cards-container">
      <!-- 加上div 每个card 大小自适应 -->
      <div v-for="(item, index) in cardList" :key="index">
        <VNewCard :data="item" />
      </div>
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

    <!-- 回到顶部 -->
    <el-backtop :right="50" :bottom="50" :visibility-height="10">UP</el-backtop>

  </div>
</template>

<script lang="ts" setup>
import VNewCard from '../components/VNewCard.vue'
import { queryNews } from '@/api/requestAPI'
import { deepCopy } from '@/utils/funcsUtil'
import { reactive, ref, onMounted, watch } from 'vue'

const cardList = ref([])

const formInline = reactive({
  keyword: '',
  date: '',
})

const pageModel = reactive({
  page: 1, //默认当前页码
  limit: 20, //默认每页的数量
  total: 0 //返回的总记录数（未分页）
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
      // 更新数组元素
      cardList.value = res.data["newsList"]
      console.log(cardList.value)
      pageModel.total = res.data["totalRecords"]
    }
  })
}


const onSubmit = async () => {
  console.log('submit!')
  pageModel.page = 1 // 注意：在查询时，要将页码显示到第一页
  await getNewsList()
}


const handleSizeChange = async (val: number) => {  
  pageModel.limit = val // 改变每页显示的条数
  pageModel.page = 1 // 注意：在改变每页显示的条数时，要将页码显示到第一页
  console.log(`${val} items per page`)
  await getNewsList()
}

const handleCurrentChange = async (val: number) => {
  pageModel.page = val // 改变页数
  console.log(`current page: ${val}`)
  await getNewsList()
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
