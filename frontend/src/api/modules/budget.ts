import { get, post, put, del } from '@/api/index'
import type { PageResult } from '@/types/global'
import type { BudgetItem, BudgetForm, BudgetAdjustForm, BudgetQuery, BudgetSummary } from '@/types/budget'

export async function getBudgetList(query: BudgetQuery) {
  return get<PageResult<BudgetItem>>('/budgets', query as Record<string, unknown>)
}

export async function getBudgetSummary() {
  return get<BudgetSummary>('/budgets/summary')
}

export async function getBudgetDetail(id: number) {
  return get<BudgetItem>(`/budgets/${id}`)
}

export async function createBudget(data: BudgetForm) {
  return post<BudgetItem>('/budgets', data as Record<string, unknown>)
}

export async function updateBudget(id: number, data: Partial<BudgetForm>) {
  return put<BudgetItem>(`/budgets/${id}`, data as Record<string, unknown>)
}

export async function adjustBudget(id: number, data: BudgetAdjustForm) {
  return post<BudgetItem>(`/budgets/${id}/adjust`, data as Record<string, unknown>)
}

export async function deleteBudget(id: number) {
  return del<null>(`/budgets/${id}`)
}