<!-- 这是前端页面展示的统计数据面板模版 -->
<template>
  <div class="chart" ref="chartRef">
  </div>
</template>

<script setup lang="ts">
import * as echarts from 'echarts'
import { ref, onMounted, watch } from 'vue'

let myChart = null
const chartRef = ref()
const props = defineProps({
  vdata: {
    type: Object,
    required: true
  }
})

onMounted(() => {
  myChart = echarts.init(chartRef.value)
  drawChart(props.vdata)
})

watch(() => props.vdata, () => drawChart(props.vdata))

const drawChart = (data) => {
  // 图标自适应
  window.addEventListener(
    'resize',
    () => myChart.resize(),
    false
  )

  const options = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '5%',
      left: 'left',
      orient: 'vertical'
    },
    series: [
      {
        type: 'pie',
        radius: ['30%', '95%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 5,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          formatter: '{b}({d}%)',
          show: false,
          position: 'center'
        },
        labelLine: {
          show: false
        },
        data: data
      }
    ]
  }

  myChart.setOption(options)
}


</script>

<style lang="scss" scoped>
.chart {
  width: 100%;
  height: 100%;
}
</style>