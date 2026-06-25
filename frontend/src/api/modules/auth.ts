import { get, post } from '@/api/index'
import type { LoginRequest, LoginResponse } from '@/types/auth'

export async function login(data: LoginRequest) {
  return post<LoginResponse>('/auth/login', data as Record<string, unknown>)
}

export async function getCurrentUser() {
  return get<LoginResponse['userInfo']>('/auth/me')
}