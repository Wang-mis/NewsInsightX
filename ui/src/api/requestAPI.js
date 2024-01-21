
import { request } from '../utils/axiosUtil'

export function getUserInfo() { return request({ url: "/api/user/info", method: "GET" }) }

export function getUserTest(config_data) { return request({ url: "/api/user/test", method: "POST", data: config_data }) }

// 查询新闻 分页查询 + 关键字查询
export function queryNews(config_data) { return request({ url: "/api/querynews", method: "POST", data: config_data }) }

// 首页统计信息
export function queryHomeStatistics() { return request({ url: "/api/homepage", method: "GET" }) }
