<template>
  <div class="intro-container">
    <el-card>这里做一些简介</el-card>
    <el-card>
      这里做一些卡片展示、当前时间、系统展示的数据时间段
    </el-card>
  </div>

  <div class="card-container" v-if="homeStatistics!==null">

    <el-card body-style="padding: 0;">
      <template #header>
        <div class="card-header">
          <h3>各个国家的新闻统计 <el-tag>TOP16</el-tag></h3>
          <el-tag type="info" size="large" effect="dark">
            <h2>ActorCountryCode</h2>
          </el-tag>
        </div>
      </template>
      <div class="chart">
        <VPieCharts :vdata="homeStatistics['ActorCountryCode']"/>
      </div>
    </el-card>

    <el-card body-style="padding: 0;">
      <template #header>
        <div class="card-header">
          <h3>各个媒体的新闻统计 <el-tag>TOP8</el-tag></h3>
          <el-tag type="info" size="large" effect="dark">
            <h2>MentionSourceName</h2>
          </el-tag>
        </div>
      </template>
      <div class="chart">
        <VPieCharts :vdata="homeStatistics['MentionSourceName']"/>
      </div>
    </el-card>

    <el-card body-style="padding: 0;">
      <template #header>
        <div class="card-header">
          <h3>各个类型的新闻统计 <el-tag>TOP8</el-tag></h3>
          <el-tag type="info" size="large" effect="dark">
            <h2>EventRootCode</h2>
          </el-tag>
        </div>
      </template>
      <div class="chart">
        <VPieCharts :vdata="homeStatistics['EventRootCode']"/>
      </div>
    </el-card>

    <el-card body-style="padding: 0;">
      <template #header>
        <div class="card-header">
          <h3>积极/消极的新闻统计</h3>
          <el-tag type="info" size="large" effect="dark">
            <h2>MentionDocTone</h2>
          </el-tag>
        </div>
      </template>
      <div class="chart">
        <VPieCharts :vdata="homeStatistics['MentionDocTone']"/>
      </div>
    </el-card>

    <el-card body-style="padding: 0;">
      <template #header>
        <div class="card-header">
          <h3>已有新闻文章占比</h3>
          <el-tag type="info" size="large" effect="dark">
            <h2>NewsProportion</h2>
          </el-tag>
        </div>
      </template>
      <div class="chart">
        <VPieCharts :vdata="homeStatistics['NewsProportion']"/>
      </div>
    </el-card>

    <el-card body-style="padding: 0;">
      <template #header>
        <div class="card-header">
          <h3>关键词词云</h3>
          <el-tag type="info" size="large" effect="dark">
            <h2>KeywordCloud</h2>
          </el-tag>
        </div>
      </template>
      <div class="chart">
        <VWordCloud />
      </div>
    </el-card>

  </div>
</template>

<script setup lang="ts">
import VPieCharts from '../components/VPieCharts.vue'
// import VBarCharts from '@/components/VBarCharts.vue'
import VWordCloud from '@/components/VWordCloud.vue'
import { queryHomeStatistics } from '@/api/requestAPI'
import { deepCopy } from '@/utils/funcsUtil'
import { reactive, ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
const store = useStore()

const homeStatistics = computed({
  get: () => store.state.homeStatistics,
  set: (value) => {
    throw new Error("homeStatistics is a read-only computed property.");
  },
});

onMounted( async () => {
  await getHomeStatistics()
})

// 请求后端首页统计信息
const getHomeStatistics = async () => {
  await gainHomeStatistics()
}

async function gainHomeStatistics() {
  await queryHomeStatistics().then(res => {
    if (res.code === 0) {
      console.log(res.data) // MentionSourceName
      store.commit("updateHomeStatistics", deepCopy(res.data))
    }
  })
}

</script>
<style lang="scss" scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
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
  height: 230px;
}
</style>