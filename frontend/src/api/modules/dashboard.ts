import { get } from '@/api/index'
import type { TrendItem, DeptRankItem, CategoryPieItem, BudgetExecItem } from '@/types/dashboard'

export async function getTrend() {
  return get<TrendItem[]>('/dashboard/trend')
}

export async function getDeptRank() {
  return get<DeptRankItem[]>('/dashboard/dept-rank')
}

export async function getCategoryPie() {
  return get<CategoryPieItem[]>('/dashboard/category-pie')
}

export async function getBudgetExec() {
  return get<BudgetExecItem[]>('/dashboard/budget-exec')
}