import http from '@/api/index'
import type { PageResult } from '@/types/global'
import type { BudgetItem, BudgetForm, BudgetAdjustForm, BudgetQuery, BudgetSummary } from '@/types/budget'

export async function getBudgetList(query: BudgetQuery) {
  return http.get<PageResult<BudgetItem>>('/budgets', query as Record<string, unknown>)
}

export async function getBudgetSummary() {
  return http.get<BudgetSummary>('/budgets/summary')
}

export async function getBudgetDetail(id: number) {
  return http.get<BudgetItem>(`/budgets/${id}`)
}

export async function createBudget(data: BudgetForm) {
  return http.post<BudgetItem>('/budgets', data as Record<string, unknown>)
}

export async function updateBudget(id: number, data: Partial<BudgetForm>) {
  return http.put<BudgetItem>(`/budgets/${id}`, data as Record<string, unknown>)
}

export async function adjustBudget(id: number, data: BudgetAdjustForm) {
  return http.post<BudgetItem>(`/budgets/${id}/adjust`, data as Record<string, unknown>)
}

export async function deleteBudget(id: number) {
  return http.del<null>(`/budgets/${id}`)
}