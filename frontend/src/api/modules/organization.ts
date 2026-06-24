import http from '@/api/index'
import type { PageResult } from '@/types/global'
import type { DeptItem, DeptForm, UserItem, UserForm } from '@/types/organization'

export async function getDeptList() {
  return http.get<DeptItem[]>('/departments')
}

export async function createDept(data: DeptForm) {
  return http.post<DeptItem>('/departments', data as Record<string, unknown>)
}

export async function updateDept(id: number, data: DeptForm) {
  return http.put<DeptItem>(`/departments/${id}`, data as Record<string, unknown>)
}

export async function deleteDept(id: number) {
  return http.del<null>(`/departments/${id}`)
}

export async function getUserList(params: Record<string, unknown>) {
  return http.get<PageResult<UserItem>>('/users', params)
}

export async function createUser(data: UserForm) {
  return http.post<UserItem>('/users', data as Record<string, unknown>)
}

export async function updateUser(id: number, data: Partial<UserForm>) {
  return http.put<UserItem>(`/users/${id}`, data as Record<string, unknown>)
}

export async function deleteUser(id: number) {
  return http.del<null>(`/users/${id}`)
}