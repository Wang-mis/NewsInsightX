<template>
  <div class="search-container">
    <div class="search-form-comtainer">
      <el-form :inline="true" :model="formInline" class="demo-form-inline">
        <el-form-item label="关键词：">
          <el-input v-model="formInline.user" placeholder="人物名称、热点词、热点事件" clearable />
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
      <div class="new-card" v-for="(item, index) in cardList">
        <VNewCard />
      </div>
    </div>

    <div class="demo-pagination-block">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[20, 40, 80, 100]"
        background="true"
        layout="total, sizes, prev, pager, next, jumper"
        :total="100"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

  </div>
</template>

<script lang="ts" setup>
import VNewCard from '../components/VNewCard.vue'
import { reactive, ref, onMounted } from 'vue'

const cardList = ref([1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10])

const formInline = reactive({
  user: '',
  date: '',
})

const onSubmit = () => {
  console.log('submit!')
}

const currentPage = ref(1)
const pageSize = ref(20)

const handleSizeChange = (val: number) => {
  console.log(`${val} items per page`)
}
const handleCurrentChange = (val: number) => {
  console.log(`current page: ${val}`)
}
</script>

<style scoped>
.new-card {
  width: 100%;
  height: 120px;
  border-radius: 10px;
  background: rgb(191, 191, 191);
}
.news-cards-container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
  grid-gap: 2.5rem;
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
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
