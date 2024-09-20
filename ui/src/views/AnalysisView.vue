<!-- <script setup>
import { ref, onMounted } from 'vue'

// 响应式状态
const count = ref(0)

// 用来修改状态、触发更新的函数
function increment() {
  count.value++
}

// 生命周期钩子
onMounted(() => {
  console.log(`The initial count is ${count.value}.`)
})
</script>

<template>
  <el-button type="primary" @click="increment">Count is: {{ count }}</el-button>
</template> -->


<template>
  <div class="home">
    <el-button type="primary">我是按钮</el-button>
    <div>用户名：{{ user.userName }}</div>
    <div>姓名：{{ user.realName }}</div>

    <div>test: {{ test.arr }}</div>
  </div>
</template>

<script>
import {getUserInfo, getUserTest} from '@/utils/axiosUtil'

export default {
  name: "TestView",
  data() {
    return {
      user: {},
      test: {},
    };
  },
  created() {
    getUserInfo().then(res => {
      if (res.code === 0) {
        this.user = res.data;
      }
    })

    getUserTest({test_arg: "test_arg"}).then(res => {
      if (res.code === 0) {
        this.test = res.data;
      }
    })
  },
};
</script>