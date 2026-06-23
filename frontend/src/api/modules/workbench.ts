import type { ApiResponse, PageResult, PageParams } from '@/types/global'
import type { WorkbenchOverview, PendingApprovalItem, TrendPoint } from '@/types/workbench'

// import http from '@/api/index'

/**
 * 获取工作台概览统计数据
 * GET /api/v1/workbench/overview
 */
// export async function getWorkbenchOverview(): Promise<ApiResponse<WorkbenchOverview>> {
//   return http.get('/workbench/overview')
// }

/**
 * 获取待审批分页列表
 * GET /api/v1/workbench/pending-approvals
 */
// export async function getPendingApprovals(
//   params: PageParams
// ): Promise<ApiResponse<PageResult<PendingApprovalItem>>> {
//   return http.get('/workbench/pending-approvals', params)
// }

/**
 * 获取支出趋势数据
 * GET /api/v1/workbench/expense-trend
 */
// export async function getExpenseTrend(): Promise<ApiResponse<TrendPoint[]>> {
//   return http.get('/workbench/expense-trend')
// }

export {}