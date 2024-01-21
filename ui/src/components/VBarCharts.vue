
<!-- 这是前端页面展示的统计数据面板模版 -->
<template>
    <div class="echarts" id="charts" ref="chart">
    </div>
</template>

<script setup lang="ts">
import * as echarts from "echarts"
import { ref, onMounted } from "vue"

// const props = defineProps({
//   vdata: {
//     type: Object,
//     required: true
//   }
// })

const chart = ref()

onMounted(()=>{
  drawChart()
  // drawChart(props.vdata)
})

const drawChart = () => {
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
    
    const options = {
      legend: {},
      tooltip: {},
      grid:{
        top: "30px",
        left: "12px",
        right: "12px",
        bottom: "12px",
        containLabel: true
      },
      dataset: {
        dimensions: ['MentionSourceName', 'AllNews', 'CrawlNews', 'WaitNews'],
        source: [
            {'MentionSourceName': 'bbc.co.uk', 'AllNews': 12, 'CrawlNews': 12, 'WaitNews': 0}, 
            {'MentionSourceName': 'bbc.com', 'AllNews': 16, 'CrawlNews': 15, 'WaitNews': 1}, 
            {'MentionSourceName': 'cnn.com', 'AllNews': 21, 'CrawlNews': 19, 'WaitNews': 2}, 
            {'MentionSourceName': 'dailymail.co.uk', 'AllNews': 27, 'CrawlNews': 0, 'WaitNews': 27}, 
            {'MentionSourceName': 'europesun.com', 'AllNews': 1, 'CrawlNews': 0, 'WaitNews': 1}, 
            {'MentionSourceName': 'foxnews.com', 'AllNews': 14, 'CrawlNews': 0, 'WaitNews': 14}, 
            {'MentionSourceName': 'nytimes.com', 'AllNews': 8, 'CrawlNews': 0, 'WaitNews': 8}, 
            {'MentionSourceName': 'washingtonpost.com', 'AllNews': 7, 'CrawlNews': 0, 'WaitNews': 7}, 
            {'MentionSourceName': 'yahoo.com', 'AllNews': 315, 'CrawlNews': 315, 'WaitNews': 0}
          ]
      },
      xAxis: { 
        type: 'category',
        splitLine: {
          show:false
        }
      },
      yAxis: {
        splitLine: {
          show:false
        }
      },
      // Declare several bar series, each will be mapped
      // to a column of dataset.source by default.
      series: [{ type: 'bar' }, { type: 'bar' }, { type: 'bar' }]
    };

    myChart.setOption(options)
}


</script>

<style lang="scss" scoped>
.echarts {
    width: 100%;
    height: 100%;
}
</style>