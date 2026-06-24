import type { ApiResponse } from '@/types/global'
import axios, { type AxiosInstance } from 'axios'

const http: AxiosInstance = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('finbalance-token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

http.interceptors.response.use(
  (response) => response.data,
  (error) => Promise.reject(error),
)

export default http

export function get<T>(url: string, params?: Record<string, unknown>): Promise<ApiResponse<T>> {
  return http.get(url, { params }) as unknown as Promise<ApiResponse<T>>
}

export function post<T>(url: string, data?: Record<string, unknown>): Promise<ApiResponse<T>> {
  return http.post(url, data) as unknown as Promise<ApiResponse<T>>
}

export function put<T>(url: string, data?: Record<string, unknown>): Promise<ApiResponse<T>> {
  return http.put(url, data) as unknown as Promise<ApiResponse<T>>
}

export function del<T>(url: string): Promise<ApiResponse<T>> {
  return http.delete(url) as unknown as Promise<ApiResponse<T>>
}