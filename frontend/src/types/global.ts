/** 统一API返回体（与后端 ApiResponse 对齐） */
export interface ApiResponse<T = unknown> {
  code: number
  data: T | null
  msg: string
}

/** 分页查询结果（与后端 PageResult 对齐） */
export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}

/** 分页请求参数 */
export interface PageParams {
  page: number
  pageSize: number
}