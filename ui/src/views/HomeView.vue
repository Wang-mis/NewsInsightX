<script setup>
import VBarCharts from '../components/VBarCharts.vue'
</script>

<template>
  <el-card>
    <div class="chart">
      <VBarCharts />
    </div>
  </el-card>
</template>

<style lang="scss" scoped>
.chart {
  width: 100%;
  height: 400px;
}
</style>