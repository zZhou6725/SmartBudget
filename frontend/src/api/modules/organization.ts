import { get, post, put, del } from '@/api/index'
import type { PageResult } from '@/types/global'
import type { DeptItem, DeptForm, UserItem, UserForm } from '@/types/organization'

export async function getDeptList() {
  return get<DeptItem[]>('/departments')
}

export async function createDept(data: DeptForm) {
  return post<DeptItem>('/departments', data as Record<string, unknown>)
}

export async function updateDept(id: number, data: DeptForm) {
  return put<DeptItem>(`/departments/${id}`, data as Record<string, unknown>)
}

export async function deleteDept(id: number) {
  return del<null>(`/departments/${id}`)
}

export async function getUserList(params: Record<string, unknown>) {
  return get<PageResult<UserItem>>('/users', params)
}

export async function createUser(data: UserForm) {
  return post<UserItem>('/users', data as Record<string, unknown>)
}

export async function updateUser(id: number, data: Partial<UserForm>) {
  return put<UserItem>(`/users/${id}`, data as Record<string, unknown>)
}

export async function deleteUser(id: number) {
  return del<null>(`/users/${id}`)
}