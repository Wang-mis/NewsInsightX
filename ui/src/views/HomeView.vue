<script setup>
import VBarCharts from '../components/VBarCharts.vue'
</script>

<template>
  <div class="intro-container">
    <el-card>这里做一些简介</el-card>
    <el-card>
      这里做一些卡片展示、当前时间、系统展示的数据时间段
    </el-card>
  </div>
  <div class="card-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>各个国家的新闻统计</h3>
        </div>
      </template>
      <div class="chart">
        <VBarCharts />
      </div>
    </el-card>

    <el-card>
      <template #header>
        <div class="card-header">
          <h3>各个媒体的新闻统计</h3>
        </div>
      </template>
      <div class="chart">
        <VBarCharts />
      </div>
    </el-card>

    <el-card>
      <template #header>
        <div class="card-header">
          <h3>各个类型的新闻统计</h3>
        </div>
      </template>
      <div class="chart">
        <VBarCharts />
      </div>
    </el-card>

    <el-card>
      <template #header>
        <div class="card-header">
          <h3>积极/消极的新闻统计</h3>
        </div>
      </template>
      <div class="chart">
        <VBarCharts />
      </div>
    </el-card>

  </div>
</template>

<style lang="scss" scoped>
// .card-header {
//   color: steelblue;
// }
.intro-container {
  margin-top: 1rem;
  display: grid;
  grid-template-columns: 4fr 1fr;
  grid-gap: 1rem;
}
.card-container {
  margin-top: 1rem;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-gap: 1rem;
}
.chart {
  width: 100%;
  height: 300px;
}
</style>