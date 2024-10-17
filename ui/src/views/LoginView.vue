<script setup lang="ts">
import { reactive, ref } from 'vue'
import { queryLogin, querySignup } from '@/utils/axiosUtil.js'
import { useRouter } from 'vue-router'
import { ElNotification } from 'element-plus'
import Cookies from 'js-cookie'
import { useStore } from 'vuex'
import { deepCopy } from '@/utils/funcsUtil'

let isSignup = ref(false)

const userData = reactive({
  username: '',
  password: '',
  passwordAgain: ''
})
const router = useRouter()
const store = useStore()
const formRef = ref(null)

const onClickLogin = () => {
  formRef.value.validate(async (valid) => {
    if (!valid) return

    const config_data = {
      username: userData.username,
      password: userData.password
    }

    await queryLogin(config_data).then((res) => {
      if (res.code === 0) {
        // 登录成功，跳转到主页
        Cookies.set('token', res.data.token, { expires: 7 })
        delete res.data.token
        store.commit('updateUserInfo', deepCopy(res.data))
        router.replace('/')
      } else if (res.code === 1) {
        // 密码错误
        ElNotification({
          title: '登录失败',
          message: '密码错误！',
          type: 'error',
          duration: 1500
        })
      } else if (res.code === 2) {
        // 用户名不存在
        ElNotification({
          title: '登录失败',
          message: '用户名不存在！',
          type: 'error',
          duration: 1500
        })
      } else {
        // 其他错误
        ElNotification({
          title: '登录失败',
          message: '未知错误！',
          type: 'error',
          duration: 1500
        })
      }
    })
  })
}

const onClickSign = () => {
  // 第一次点击注册按钮，切换至注册界面
  if (!isSignup.value) {
    isSignup.value = true
    return
  }

  // 第二次点击注册按钮，提交数据
  formRef.value.validate(async (valid) => {
    if (!valid) return
    const config_data = {
      username: userData.username,
      password: userData.password
    }

    await querySignup(config_data).then((res) => {
      if (res.code === 0) {
        // 注册成功，跳转到homepage
        Cookies.set('token', res.data.token, { expires: 7 })
        delete res.data.token
        store.commit('updateUserInfo', deepCopy(res.data))
        router.replace('/')
      } else if (res.code === 1) {
        // 用户名已存在
        ElNotification({
          title: '注册失败',
          message: '用户名已存在！',
          type: 'error',
          duration: 1500
        })
      } else {
        // 其他错误
        ElNotification({
          title: '注册失败',
          message: '未知错误！',
          type: 'error',
          duration: 1500
        })
      }
    })


  })
}


const validatePassword = (rule, value, callback) => {
  const regex = /^[a-zA-Z0-9_!@#$%^&*()-=+[\]{};':"\\|,.<>?]+$/
  if (!regex.test(value)) callback(new Error('密码只能由字母、数字、常用字符组成'))
  else callback()
}

const validatePasswordAgain = (rule, value, callback) => {
  if (value !== userData.password) callback(new Error('两次输入的密码不一致'))
  else callback()
}

const signupRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' }
  ],
  passwordAgain: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePasswordAgain, trigger: 'blur' }
  ]
})

const loginRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' }
  ]
})


</script>

<template>
  <div class="login-container">
    <div class="login">
      <div class="title" v-if="isSignup">用户注册</div>
      <div class="title" v-else>用户登录</div>

      <el-form
        :model="userData"
        :rules="isSignup ? signupRules : loginRules"
        ref="formRef"
        label-width="auto"
        style="max-width: 600px;">
        <el-form-item label="用户名" style="margin-bottom: 16px;" prop="username">
          <el-input v-model="userData.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" style="margin-bottom: 16px;" prop="password">
          <el-input type="password" v-model="userData.password" placeholder="请输入密码" autocomplete="off" />
        </el-form-item>
        <el-form-item label="确认密码" v-show="isSignup" style="margin-bottom: 16px;" prop="passwordAgain">
          <el-input type="password" v-model="userData.passwordAgain" placeholder="请再次输入密码" autocomplete="off" />
        </el-form-item>

        <el-form-item style="margin-top: 25px;">
          <div style="width: 100%; display: flex; justify-content: center">
            <el-button type="primary" @click="onClickLogin" v-show="!isSignup">登录</el-button>
            <el-button :type="isSignup ? 'primary' : ''" @click="onClickSign">注册</el-button>
            <el-button @click="isSignup = false" v-show="isSignup">返回登录</el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-container {
  width: 100%;
  height: 800px;
  position: relative;

  .login {
    // 调整位置到父元素正中间
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 300px;

    // 设置边框
    border: solid;
    border-radius: 5px;
    padding: 0 20px;

    background-color: whitesmoke;

    // 设置标题
    .title {
      display: flex;
      justify-content: center;
      align-items: center;
      margin: 15px 0;
      font-size: 25px;
      color: #2c3e50;
    }
  }
}
</style>