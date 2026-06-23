import type { ApiResponse, PageResult } from '@/types/global'
import type { BudgetItem, BudgetForm, BudgetAdjustForm, BudgetQuery, BudgetSummary } from '@/types/budget'

// import http from '@/api/index'

/**
 * 获取预算分页列表
 * GET /api/v1/budgets
 */
// export async function getBudgetList(query: BudgetQuery): Promise<ApiResponse<PageResult<BudgetItem>>> {
//   return http.get('/budgets', query)
// }

/**
 * 获取预算统计摘要
 * GET /api/v1/budgets/summary
 */
// export async function getBudgetSummary(): Promise<ApiResponse<BudgetSummary>> {
//   return http.get('/budgets/summary')
// }

/**
 * 获取预算详情
 * GET /api/v1/budgets/{id}
 */
// export async function getBudgetDetail(id: number): Promise<ApiResponse<BudgetItem>> {
//   return http.get(`/budgets/${id}`)
// }

/**
 * 新增预算
 * POST /api/v1/budgets
 */
// export async function createBudget(data: BudgetForm): Promise<ApiResponse<BudgetItem>> {
//   return http.post('/budgets', data)
// }

/**
 * 编辑预算
 * PUT /api/v1/budgets/{id}
 */
// export async function updateBudget(id: number, data: Partial<BudgetForm>): Promise<ApiResponse<BudgetItem>> {
//   return http.put(`/budgets/${id}`, data)
// }

/**
 * 预算调整（追加/削减）
 * POST /api/v1/budgets/{id}/adjust
 */
// export async function adjustBudget(id: number, data: BudgetAdjustForm): Promise<ApiResponse<BudgetItem>> {
//   return http.post(`/budgets/${id}/adjust`, data)
// }

/**
 * 删除预算
 * DELETE /api/v1/budgets/{id}
 */
// export async function deleteBudget(id: number): Promise<ApiResponse<null>> {
//   return http.delete(`/budgets/${id}`)
// }

export {}