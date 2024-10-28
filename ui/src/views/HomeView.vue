<template>
  <div class="home-page-container">
    <div class="intro-container">
      <div class="intro">
        <ArticlesCountDisplay :start-date="dataTimeRange[0]" :end-date="dataTimeRange[1]" />
      </div>
      <div class="separator-container">
        <div class="separator"></div>
      </div>
      <div class="info">
        <el-form style="width: 100%;">
          <el-form-item :label="$t('info.dataTimeRange')">
            <el-date-picker
              v-model="dataTimeRange"
              type="daterange"
              :range-separator="$t('search.timeRangeSep')"
              :start-placeholder="$t('search.startTime')"
              :end-placeholder="$t('search.endTime')"
              value-format="YYYYMMDD"
              format="YY/MM/DD"
              :disabled-date="(date) => date.getTime() > Date.now()"
              disabled
            />
          </el-form-item>
          <el-form-item :label="$t('info.displayTimeRange')">
            <el-date-picker
              v-model="displayTimeRange"
              type="daterange"
              :range-separator="$t('search.timeRangeSep')"
              :start-placeholder="$t('search.startTime')"
              :end-placeholder="$t('search.endTime')"
              value-format="YYYYMMDD"
              format="YY/MM/DD"
              :disabled-date="(date) => date.getTime() > Date.now()"
              :clearable="false"
            />
          </el-form-item>
          <div
            v-if="homeStatistics !== null"
            class="number-info-contatiner"
            style="width: 100%; display: flex; justify-content: space-between; align-items: center; padding-top: 10px;">

            <el-statistic :title="$t('info.totalCount')" :value="homeStatistics['totalCount']" />
            <el-statistic :title="$t('info.timeRangeCount')" :value="homeStatistics['timeRangeCount']" />
            <el-statistic :title="$t('info.yesterdayCount')" :value="homeStatistics['yesterdayCount']" />
          </div>
        </el-form>
      </div>
    </div>
    <div class="card-container" v-if="homeStatistics !== null">
      <div class="card">
        <div class="card-header">
          <h3>{{ $t('chartsName.ActorCountryCode') }}
            <el-tag>TOP 8</el-tag>
          </h3>
        </div>
        <div class="card-separator"></div>
        <div class="card-body">
          <VPieCharts :vdata="homeStatistics['ActorCountryCode']" />
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3>{{ $t('chartsName.shortMentionSourceName') }}
            <el-tag>TOP 8</el-tag>
          </h3>
        </div>
        <div class="card-separator"></div>
        <div class="card-body">
          <VPieCharts :vdata="shortMentionSourceName" />
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3>{{ $t('chartsName.EventRootCode') }}
            <el-tag>TOP 8</el-tag>
          </h3>
        </div>
        <div class="card-separator"></div>
        <div class="card-body">
          <VPieCharts :vdata="homeStatistics['EventRootCode']" />
        </div>
      </div>

      <div class="card">
        <div class="card-header"><h3>{{ $t('chartsName.MentionDocTone') }}</h3></div>
        <div class="card-separator"></div>
        <div class="card-body">
          <VPieCharts :vdata="homeStatistics['MentionDocTone']" />
        </div>
      </div>

      <div class="card">
        <div class="card-header"><h3>{{ $t('chartsName.NewsProportion') }}</h3></div>
        <div class="card-separator"></div>
        <div class="card-body">
          <VPieCharts :vdata="homeStatistics['NewsProportion']" />
        </div>
      </div>

      <div class="card">
        <div class="card-header"><h3>{{ $t('chartsName.KeywordCloud') }}</h3></div>
        <div class="card-separator"></div>
        <div class="card-body">
          <VWordCloud :vdata="homeStatistics['KeywordCloud']" />
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import VPieCharts from '@/components/VPieCharts.vue'
import VWordCloud from '@/components/VWordCloud.vue'
import { queryHomeStatistics } from '@/utils/axiosUtil.js'
import { deepCopy } from '@/utils/funcsUtil.js'
import { onMounted, computed, ref, watch, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import ArticlesCountDisplay from '@/components/ArticlesCountDisplay.vue'

const store = useStore()

function formatDate(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0') // 月份从0开始，需加1
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}${month}${day}`
}

const yesterday = new Date()
yesterday.setDate(new Date().getDate() - 2)
const yesterdayStr = formatDate(yesterday)

const sevenDaysAgo = new Date()
sevenDaysAgo.setDate(new Date().getDate() - 8)
const sevenDaysAgoStr = formatDate(sevenDaysAgo)

const dataTimeRange = ref(['20240915', yesterdayStr])
const displayTimeRange = ref([sevenDaysAgoStr, yesterdayStr])

const homeStatistics = computed(() => store.state.homeStatistics)
const shortMentionSourceName = computed(() => {
  const data = store.state.homeStatistics['MentionSourceName']
  return data.map(x => {
    return { name: x['name'].split('.')[0], value: x['value'] }
  })
})

onBeforeMount(() => document.title = "Home")
onMounted(async () => await getHomeStatistics())

// 请求后端首页统计信息
async function getHomeStatistics() {
  const configData = {
    'forceUpdate': false,
    'startDate': displayTimeRange.value[0],
    'endDate': displayTimeRange.value[1]
  }
  await queryHomeStatistics(configData).then(res => {
    if (res.code === 0) store.commit('updateHomeStatistics', deepCopy(res.data))
  })
}

// 修改timeRange后更新数据
watch(displayTimeRange, async () => {
  console.log('检测到用户修改当前显示时间段，更新数据。')
  await getHomeStatistics()
})

</script>

<style lang="scss" scoped>
@import "public/styles/variables.scss";

.home-page-container {
  width: 100%;
  height: 100%;
  padding: 0 20px;
}

.intro-container {
  background-color: white;
  color: #2c3e50;

  margin-top: 15px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.12);

  display: flex;
  width: 100%;
  height: $intro-container-height;

  .intro {
    padding: 20px;

    width: $intro-width-percent;
    height: 100%;
  }

  .separator-container {
    height: 100%;
    padding: 20px 0;

    .separator {
      height: 100%;
      border-left: 1px solid #e4e7ed;
    }

  }

  .info {
    padding: 20px;

    width: $info-width-percent;
    min-width: 300px;
    height: 100%;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
}

.card-container {
  padding: 15px 0;
  width: 100%;
  height: calc(100vh - $intro-container-height - 55px);

  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  grid-gap: 12px;

  .card {
    background-color: white;
    color: #2c3e50;

    min-height: 200px;
    min-width: 200px;

    border: 1px solid #e4e7ed;
    border-radius: 4px;
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.12);

    display: flex;
    flex-direction: column;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      height: 45px;
      padding: 5px 20px;
    }

    .card-separator {
      border-top: 1px solid #e4e7ed;
    }

    .card-body {
      width: 100%;
      flex-grow: 1;
    }
  }
}

@media (max-width: 800px) {
  .card-container {
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr 1fr;
  }
}

</style>