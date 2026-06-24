import http from '@/api/index'
import type { PageResult } from '@/types/global'
import type { ExpenseItem, ExpenseForm, ExpenseQuery, ExpenseSummary } from '@/types/expense'

export async function getExpenseList(query: ExpenseQuery) {
  return http.get<PageResult<ExpenseItem>>('/expenses', query as Record<string, unknown>)
}

export async function getExpenseSummary() {
  return http.get<ExpenseSummary>('/expenses/summary')
}

export async function getExpenseDetail(id: number) {
  return http.get<ExpenseItem>(`/expenses/${id}`)
}

export async function createExpense(data: ExpenseForm) {
  return http.post<ExpenseItem>('/expenses', data as Record<string, unknown>)
}

export async function updateExpense(id: number, data: Partial<ExpenseForm>) {
  return http.put<ExpenseItem>(`/expenses/${id}`, data as Record<string, unknown>)
}

export async function deleteExpense(id: number) {
  return http.del<null>(`/expenses/${id}`)
}