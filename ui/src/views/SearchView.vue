<template>
  <div class="search">
    <h1>This is an search page</h1>
    <br>
    <h2> {{ name }}</h2>
  </div>
</template>
<script>
import { useStore } from "vuex"
export default {
  name: "SearchView",
  setup() {
    let { name } = useStore().state  //2.取值

    return {
      name   //3.return出去
    }
  }
}
</script>
<style scoped>
.search {
  display: flex;
}
</style>
