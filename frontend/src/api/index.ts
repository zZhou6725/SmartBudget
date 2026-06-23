import type { ApiResponse } from '@/types/global'

// import axios, { type AxiosInstance } from 'axios'

// const http: AxiosInstance = axios.create({
//   baseURL: '/api/v1',
//   timeout: 10000,
//   headers: { 'Content-Type': 'application/json' },
// })

// http.interceptors.request.use((config) => {
//   // TODO: 注入 JWT token
//   return config
// })

// http.interceptors.response.use(
//   (response) => {
//     const res = response.data as ApiResponse
//     return res
//   },
//   (error) => {
//     return Promise.reject(error)
//   },
// )

// export default http

/** 暂不发起真实请求，API 函数仅保留注释外壳 */
export {}

/**
 * 通用 GET 请求外壳
 * @param url 接口路径
 * @param params 查询参数
 * @returns ApiResponse<T>
 */
// export function get<T>(url: string, params?: Record<string, unknown>): Promise<ApiResponse<T>> {
//   return http.get(url, { params })
// }

/**
 * 通用 POST 请求外壳
 * @param url 接口路径
 * @param data 请求体
 * @returns ApiResponse<T>
 */
// export function post<T>(url: string, data?: Record<string, unknown>): Promise<ApiResponse<T>> {
//   return http.post(url, data)
// }