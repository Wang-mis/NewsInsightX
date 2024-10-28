<script setup lang="ts">
import { onBeforeMount, reactive, ref } from 'vue'
import { queryLogin } from '@/utils/axiosUtil.js'
import { useRouter } from 'vue-router'
import { ElNotification } from 'element-plus'
import Cookies from 'js-cookie'
import { useStore } from 'vuex'
import { deepCopy } from '@/utils/funcsUtil'

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

const validatePassword = (rule, value, callback) => {
  const regex = /^[a-zA-Z0-9_!@#$%^&*()-=+[\]{};':"\\|,.<>?]+$/
  if (!regex.test(value)) callback(new Error('密码只能由字母、数字、常用字符组成'))
  else callback()
}

const loginRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' }
  ]
})

onBeforeMount(() => {
  store.commit('clearUserInfo')
  document.title = "Login"
})

</script>

<template>
  <div class="login-page-container">
    <div class="top-content-container">
      <div class="login-container">
        <div class="login">
          <div class="title">
            <div class="logo"></div>
            <div class="welcome">Welcome</div>
            <div class="greet">It's great to see you.</div>
          </div>
          <div class="form-container">
            <el-form
              label-position="top"
              :model="userData"
              :rules="loginRules"
              hide-required-asterisk
              :show-message="false"
              ref="formRef"
              label-width="auto"
              style="max-width: 600px;">
              <el-form-item style="margin-bottom: 10px;" prop="username">
                <template #label>
                  Username
                </template>
                <el-input v-model="userData.username" placeholder="Username" size="large" />
              </el-form-item>
              <el-form-item style="margin-bottom: 10px;" prop="password">
                <template #label>
                  <div class="password-label-container"
                       style="display: flex; flex-direction: row; justify-content: space-between;">
                    <span>Password</span>
                    <a>Forgot password?</a>
                  </div>
                </template>
                <el-input type="password" v-model="userData.password" placeholder="Password" autocomplete="off"
                          size="large" />
              </el-form-item>

              <el-form-item style="margin-top: 25px;">
                <el-button type="primary" style="width: 100%; background-color: #5954f5;" size="large"
                           @click="onClickLogin">
                  Let's go
                </el-button>
              </el-form-item>
            </el-form>
            <div class="to-sign" style="width: 100%; display: flex; justify-content: center; color: #2c3e50">
              <span>Don't have an account? <a href="#">Get started.</a></span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="bottom-bar-container">
      <div class="create-by" v-show="false">
        <span>Created by</span>
        <img src="https://upload.wikimedia.org/wikipedia/commons/9/95/Vue.js_Logo_2.svg" alt="Vue Logo" width="55"
             height="55" style="padding: 0 10px;">
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import "public/styles/variables.scss";


.login-page-container {
  font-family: "Inter", sans-serif;

  width: 100%;
  height: 100vh;
  position: absolute;
  left: 0;
  top: 0;
  background-image: url("public/bg_login.webp");

  .top-content-container {
    width: 100%;
    height: calc(100% - $bottom-bar-height);
    position: relative;
  }

  .bottom-bar-container {
    width: 100%;
    height: $bottom-bar-height;
    background-color: #2f2f2f;
    padding: 0 40px;

    display: flex;
    flex-direction: row-reverse;
    align-items: center;

    .create-by {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;
      color: white;

      font-family: "Inter", sans-serif;
      font-size: 22px;
    }
  }

  .login-container {
    height: 100%;
    width: calc(100% - $left-bar-width);
    float: right;
    background-color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    .login {
      width: 320px;

      .title {
        width: 100%;

        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding-bottom: 30px;

        .welcome {
          color: #2c3e50;
          font-size: 25px;
          font-weight: bold;
        }

        .greet {
          color: #2c3e50;
          font-size: 15px;
          font-weight: normal;
        }
      }
    }
  }


}
</style>