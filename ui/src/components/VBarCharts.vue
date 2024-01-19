<template>
    <div class="echarts" id="charts" ref="chart">
    </div>
</template>

<script setup lang="ts">
import * as echarts from "echarts"
import { ref, reactive, onMounted, watch } from "vue"
const chart = ref()
const options = ref({
  tooltip: {
    trigger: 'item'
  },
  legend: {
    top: '5%',
    left: 'center'
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 40,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: 1048, name: 'Search Engine' },
        { value: 735, name: 'Direct' },
        { value: 580, name: 'Email' },
        { value: 484, name: 'Union Ads' },
        { value: 300, name: 'Video Ads' }
      ]
    }
  ]
})
onMounted(()=>{
    const myChart = echarts.init(chart.value)
    console.log(myChart)
    // 图标自适应
    window.addEventListener(
        "resize",
        () => {
            myChart.resize()
        },
        false
    )
    myChart.setOption(options.value)
})


</script>

<style lang="scss" scoped>
.echarts {
    width: 100%;
    height: 100%;
}
</style>