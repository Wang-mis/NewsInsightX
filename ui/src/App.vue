<template>
  <div class="nav-bar" v-if="store.state.userinfo !== null && store.state.userinfo !== undefined">
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

<style lang="scss">
@font-face {
  font-family: 'Inter';
  src: url('/public/fonts/Inter-4.0/InterVariable.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Inter';
  src: url('/public/fonts/Inter-4.0/extras/ttf/Inter-Bold.ttf') format('truetype');
  font-weight: bold;
  font-style: normal;
}

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
  padding: 40px 0 0 0;
  width: 100%;
}
</style>
