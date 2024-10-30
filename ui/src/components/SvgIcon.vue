<template>
  <svg aria-hidden="true" :style="{width: width, height: height, fill: 'currentColor'}">
    <use :href="`#icon-${icon}`"></use>
  </svg>
</template>

<script setup>

const props = defineProps({
  icon: {
    type: String,
    required: true
  },
  width: {
    type: String,
    default: '1em'
  },
  height: {
    type: String,
    default: '1em'
  }
})

</script>

<style lang="scss" scoped>

</style>
