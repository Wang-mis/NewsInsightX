
import { request } from '../utils/axiosUtil'

export function getUserInfo() { return request({ url: "/api/user/info", method: "GET" }) }

export function getUserTest(data) { return request({ url: "/api/user/test", method: "POST", data: data }) }
