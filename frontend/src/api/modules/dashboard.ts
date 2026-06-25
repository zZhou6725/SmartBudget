import { get } from '@/api/index'
import type { TrendItem, DeptRankItem, CategoryPieItem, BudgetExecItem } from '@/types/dashboard'

export async function getTrend(month?: string, deptName?: string) {
  const params: Record<string, string> = {}
  if (month) params.month = month
  if (deptName) params.dept_name = deptName
  return get<TrendItem[]>('/dashboard/trend', params)
}

export async function getDeptRank(month?: string) {
  const params: Record<string, string> = {}
  if (month) params.month = month
  return get<DeptRankItem[]>('/dashboard/dept-rank', params)
}

export async function getCategoryPie(month?: string, deptName?: string) {
  const params: Record<string, string> = {}
  if (month) params.month = month
  if (deptName) params.dept_name = deptName
  return get<CategoryPieItem[]>('/dashboard/category-pie', params)
}

export async function getBudgetExec(year?: number) {
  const params: Record<string, string> = {}
  if (year) params.year = String(year)
  return get<BudgetExecItem[]>('/dashboard/budget-exec', params)
}