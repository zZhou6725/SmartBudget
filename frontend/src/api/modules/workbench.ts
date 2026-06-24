import http from '@/api/index'
import type { WorkbenchOverview, PendingApprovalItem, TrendPoint } from '@/types/workbench'
import type { PageResult } from '@/types/global'

export async function getWorkbenchOverview() {
  return http.get<WorkbenchOverview>('/workbench/overview')
}

export async function getPendingApprovals(params: Record<string, unknown>) {
  return http.get<PageResult<PendingApprovalItem>>('/workbench/pending-approvals', params)
}

export async function getExpenseTrend() {
  return http.get<TrendPoint[]>('/workbench/expense-trend')
}