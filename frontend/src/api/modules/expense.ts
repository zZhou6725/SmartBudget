import { get, post, put, del } from '@/api/index'
import type { PageResult } from '@/types/global'
import type { ExpenseItem, ExpenseForm, ExpenseQuery, ExpenseSummary } from '@/types/expense'

export async function getExpenseList(query: ExpenseQuery) {
  return get<PageResult<ExpenseItem>>('/expenses', query as Record<string, unknown>)
}

export async function getExpenseSummary() {
  return get<ExpenseSummary>('/expenses/summary')
}

export async function getExpenseDetail(id: number) {
  return get<ExpenseItem>(`/expenses/${id}`)
}

export async function createExpense(data: ExpenseForm) {
  return post<ExpenseItem>('/expenses', data as Record<string, unknown>)
}

export async function updateExpense(id: number, data: Partial<ExpenseForm>) {
  return put<ExpenseItem>(`/expenses/${id}`, data as Record<string, unknown>)
}

export async function deleteExpense(id: number) {
  return del<null>(`/expenses/${id}`)
}