<template>
  <div class="search-container">
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
</template>

<script lang="ts" setup>
import { reactive } from 'vue'

const formInline = reactive({
  user: '',
  date: '',
})

const onSubmit = () => {
  console.log('submit!')
  alert('submit!')
}
</script>

<style scoped>
.search-container {
  margin-top: 1rem;
}
.demo-form-inline {
  margin: 0 1rem 0 1rem;
}
.demo-form-inline .el-input {
  --el-input-width: 220px;
}

.demo-form-inline .el-select {
  --el-select-width: 220px;
}
</style>
