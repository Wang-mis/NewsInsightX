<!-- 这是前端页面展示的词云模版 -->
<template>
  <div class="chart" id="charts" ref="chart">
  </div>
</template>

<script setup lang="ts">
import * as echarts from 'echarts'
import { ref, onMounted, watch } from 'vue'
import 'echarts-wordcloud'

let myChart = null
const props = defineProps({
  vdata: {
    type: Object,
    required: true
  }
})

const chart = ref()

onMounted(() => {
  myChart = echarts.init(chart.value)
  drawChart(props.vdata)
})

watch(() => props.vdata, () => drawChart(props.vdata))

const drawChart = (data) => {
  // 图标自适应
  window.addEventListener(
    'resize',
    () => {
      myChart.resize()
    },
    false
  )

  const options = {
    tooltip: { trigger: 'item' },
    series: [
      {
        type: 'wordCloud',
        shape: 'triangle',
        keepAspect: false,
        left: 'center',
        top: 'center',
        width: '95%',
        height: '90%',
        right: null,
        bottom: null,
        sizeRange: [15, 60],
        rotationRange: [-90, 90],
        rotationStep: 90,
        gridSize: 8,
        drawOutOfBound: false,
        shrinkToFit: true,
        layoutAnimation: true,
        textStyle: {
          fontFamily: 'sans-serif',
          fontWeight: 'bold',
          color: function() {
            return (
              'rgb(' +
              [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160)
              ].join(',') +
              ')'
            )
          }
        },
        emphasis: {
          focus: 'self',
          textStyle: {
            textShadowBlur: 10,
            textShadowColor: '#333'
          }
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