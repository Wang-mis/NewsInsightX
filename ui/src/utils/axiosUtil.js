import Axios from "axios";
// import { ElMessage } from "element-plus";
import { ElNotification } from 'element-plus';

function axiosUtil(config) {
  const instance = Axios.create({
    baseURL: 'http://localhost:5173',
    headers: {'token': "hdjhs__token"}
    // timeout: 5000,
  })
  
  //响应拦截器
  instance.interceptors.response.use(res => {
    if(res.data.code === 20010 && res.data.type == 'warning') {
      ElNotification({
        title: 'Error',
        message: res.data.msg,
        type: res.data.type,
        duration: 1500
      })
    }
    return res.data
  }, error => {
    console.log(error)
    ElNotification({
      title: 'Error',
      message: 'error',
      type: 'error',
      duration: 1500
    })
  })
  return instance(config);
}

function request_get(config) {
  return axiosUtil({
    url: config.url,
    method: 'GET',
    params: (config.data == null || config.data == '')? '': config.data
  })
}

function request_post(config) {
  return axiosUtil({
    url: config.url,
    method: 'POST',
    data: config.data
  })
}

function request(config) {
  if(config.method === "POST"){
    return request_post(config)
  }
  else if(config.method === "GET"){
    return request_get(config)
  }
}

export { request }