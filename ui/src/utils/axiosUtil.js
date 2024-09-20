import Axios from "axios";
import {ElNotification} from 'element-plus';

function axiosUtil(config) {
    const instance = Axios.create({
        baseURL: "/",
        headers: {'token': "hdjhs__token"}
    })

    //响应拦截器
    instance.interceptors.response.use(res => {
        if (res.data.code === 20010 && res.data.type === 'warning') {
            ElNotification({
                title: 'Error',
                message: res.data.msg,
                type: res.data.type,
                duration: 1500
            })
        }
        return res.data
    }, _ => {
        ElNotification({
            title: 'Error',
            message: '向后端服务器请求数据失败！',
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
        params: (config.data == null || config.data === '') ? '' : config.data
    })
}

function request_post(config) {
    return axiosUtil({
        url: config.url,
        method: 'POST',
        data: config.data
    })
}

export function request(config) {
    if (config.method === "POST") {
        return request_post(config)
    } else if (config.method === "GET") {
        return request_get(config)
    }
}

export function getUserInfo() {
    return request({url: "/api/user/info", method: "GET"})
}

export function getUserTest(config_data) {
    return request({url: "/api/user/test", method: "POST", data: config_data})
}

export function queryLogin(config_data) {
    return request({url: "/api/user/login", method: "POST", data: config_data})
}

export function querySignup(config_data) {
    return request({url: "/api/user/signup", method: "POST", data: config_data})
}

// 查询新闻 分页查询 + 关键字查询
export function queryNews(config_data) {
    return request({url: "/api/querynews", method: "POST", data: config_data})
}

// 首页统计信息
export function queryHomeStatistics() {
    return request({url: "/api/homepage", method: "GET"})
}
