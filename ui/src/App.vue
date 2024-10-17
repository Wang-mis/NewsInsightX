<template>
  <div class="nav-bar">
    <NavBar />
  </div>
  <div id="page-container">
    <RouterView />
  </div>
</template>

<script setup lang="ts">

import { RouterView, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { computed } from 'vue'
import NavBar from '@/components/NavBar.vue'

const store = useStore()

const getUsername = computed(() => {
  if (store.state.userinfo === null ||
    store.state.userinfo === undefined ||
    !('username' in store.state.userinfo))
    return 'Not Login'
  return store.state.userinfo.username
})

</script>

<style>
html body {
  margin: 0;
  padding: 0;
}

#app {
  margin: 0;
  padding: 0;
}

.a-none-style {
  text-decoration: none;
  border: none;
  color: inherit;
}

.ul-none-style {
  list-style: none;
}

#page-container {
  padding: 40px 20px 0 20px;
  width: 100%;
}
</style>
