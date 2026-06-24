/** 登录请求（对齐后端 LoginRequest） */
export interface LoginRequest {
  username: string
  password: string
}

/** 登录响应（对齐后端 LoginResponse） */
export interface LoginResponse {
  token: string
  userInfo: {
    id: number
    username: string
    realName: string
    avatar: string
    role: string
  }
}