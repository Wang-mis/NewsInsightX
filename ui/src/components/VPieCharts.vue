
<!-- 这是前端页面展示的统计数据面板模版 -->
<template>
    <div class="echarts" id="charts" ref="chart">
    </div>
</template>

<script setup lang="ts">
import * as echarts from "echarts"
import { ref, onMounted } from "vue"

const props = defineProps({
  vdata: {
    type: Object,
    required: true
  }
})

const chart = ref()

onMounted(()=>{
  drawChart(props.vdata)
})

const drawChart = (data) => {
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
      tooltip: {
        trigger: 'item',
        // formatter: function(params) {
        //   return (
        //     'X: ' +
        //     params.value +
        //     '<br>Y: ' +
        //     params.name
        //   );
        // }
      },
      legend: {
        top: '5%',
        left: 'left',
        orient: 'vertical',
      },
      series: [
        {
          // name: 'Access From',
          type: 'pie',
          radius: ['30%', '95%'],
          // radius: '50%',
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
          data: data
        }
      ]
    }

    myChart.setOption(options)
}


</script>

<style lang="scss" scoped>
.echarts {
    width: 100%;
    height: 100%;
}
</style>