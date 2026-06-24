import http from '@/api/index'
import type { TrendItem, DeptRankItem, CategoryPieItem, BudgetExecItem } from '@/types/dashboard'

export async function getTrend() {
  return http.get<TrendItem[]>('/dashboard/trend')
}

export async function getDeptRank() {
  return http.get<DeptRankItem[]>('/dashboard/dept-rank')
}

export async function getCategoryPie() {
  return http.get<CategoryPieItem[]>('/dashboard/category-pie')
}

export async function getBudgetExec() {
  return http.get<BudgetExecItem[]>('/dashboard/budget-exec')
}