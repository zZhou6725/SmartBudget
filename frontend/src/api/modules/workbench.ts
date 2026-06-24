import { get } from '@/api/index'
import type { WorkbenchOverview, PendingApprovalItem, TrendPoint } from '@/types/workbench'
import type { PageResult } from '@/types/global'

export async function getWorkbenchOverview() {
  return get<WorkbenchOverview>('/workbench/overview')
}

export async function getPendingApprovals(params: Record<string, unknown>) {
  return get<PageResult<PendingApprovalItem>>('/workbench/pending-approvals', params)
}

export async function getExpenseTrend() {
  return get<TrendPoint[]>('/workbench/expense-trend')
}