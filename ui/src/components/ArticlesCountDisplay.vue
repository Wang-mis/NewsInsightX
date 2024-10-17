<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { queryArticlesCountsDay } from '@/utils/axiosUtil'
import { dateEquals } from 'element-plus'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  startDate: {
    type: Number,
    required: true
  },
  endDate: {
    type: Number,
    required: true
  }
})
const chartRef = ref()
let myChart = null
let counts = [] // 存储从后端请求来的文章数量列表
const { t, locale } = useI18n()

const queryCounts = async () => {
  console.log('开始请求从 ' + props.startDate + ' 到 ' + props.endDate + ' 每天的新闻数量。')
  const configData = { 'timeRange': [props.startDate, props.endDate], 'forceUpdate': false }
  await queryArticlesCountsDay(configData).then(res => {
    if (res.code === 0) {
      console.log('请求从 ' + props.startDate + ' 到 ' + props.endDate + ' 每天的新闻数量成功。')
      counts = res.data['counts']
    }
  })
}

onMounted(async () => {
  myChart = echarts.init(chartRef.value)
  await queryCounts()
  drawChart()
  // 改变窗口大小时重绘图表
  window.addEventListener('resize', () => {
    console.log('检测到窗口大小改变，重新绘制图表。')
    myChart.resize()
  })
})

// 更换语言时修改标题
watch(locale, () => {
  if (myChart === null) return
  console.log('检测到切换语言，修改标题。')
  myChart.setOption({ title: { text: t('chartsName.dailyArticlesCount') } })
})

// 修改时间段时，重新请求数据，并重绘图表
watch([() => props.startDate, () => props.endDate], async () => {
  await queryCounts()
  drawChart()
})

const drawChart = () => {
  if (counts.length === 0) {
    console.log('文章数量数组Counts长度为0，不绘制折线图。')
    return
  }

  console.log('开始绘制文章数量折线图。')

  // 生成日期
  const formatDate = (d) => {
    d = String(d)
    const year = d.slice(0, 4)
    const month = d.slice(4, 6)
    const day = d.slice(6, 8)
    return `${year}-${month}-${day}`
  }
  const start = new Date(formatDate(props.startDate))
  const end = new Date(formatDate(props.endDate))
  const dates = []
  while (start <= end) {
    dates.push(start.toISOString().split('T')[0])
    start.setDate(start.getDate() + 1)
  }

  const gradient = new echarts.graphic.LinearGradient(0, 0, 0, 1, [
    { offset: 0, color: 'rgb(0, 221, 255)' },
    { offset: 1, color: 'rgb(77, 119, 255)' }
  ])
  const options = {
    grid: {
      left: '5%',
      right: '5%',
      top: '17%',
      bottom: '25%'
    },
    title: {
      text: t('chartsName.dailyArticlesCount'),
      left: '0%',
      top: '0%'
    },
    tooltip: {
      trigger: 'axis',
      position: function(pt) {
        return [pt[0], '10%']
      }
    },
    dataZoom: [
      { type: 'inside', start: 0, end: 100 },
      { start: 0, end: 100, height: 15, bottom: '5%' }
    ],
    xAxis: {
      type: 'category',
      data: dates,
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      boundaryGap: false,
      splitNumber: 3,
      axisLine: { show: true },
      axisLabel: {
        margin: 13,
        formatter: (value) => (value / 1000) + 'k'
      }
    },
    series: [
      {
        name: 'Count',
        data: counts,
        type: 'line',
        smooth: true,
        symbol: 'none',
        itemStyle: { color: 'rgb(0, 221, 255)' },
        lineStyle: { color: gradient },
        areaStyle: { color: gradient }
      }
    ]
  }

  myChart.setOption(options)
}


</script>

<template>
  <div class="container">
    <div class="chart" ref="chartRef">
    </div>
  </div>
</template>

<style scoped lang="scss">
.container {
  width: 100%;
  height: 100%;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>