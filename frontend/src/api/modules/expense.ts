import type { ApiResponse, PageResult } from '@/types/global'
import type { ExpenseItem, ExpenseForm, ExpenseQuery, ExpenseSummary } from '@/types/expense'

// import http from '@/api/index'

/**
 * 获取报销分页列表
 * GET /api/v1/expenses
 */
// export async function getExpenseList(query: ExpenseQuery): Promise<ApiResponse<PageResult<ExpenseItem>>> {
//   return http.get('/expenses', query)
// }

/**
 * 获取报销统计摘要
 * GET /api/v1/expenses/summary
 */
// export async function getExpenseSummary(): Promise<ApiResponse<ExpenseSummary>> {
//   return http.get('/expenses/summary')
// }

/**
 * 获取报销详情
 * GET /api/v1/expenses/{id}
 */
// export async function getExpenseDetail(id: number): Promise<ApiResponse<ExpenseItem>> {
//   return http.get(`/expenses/${id}`)
// }

/**
 * 新增报销
 * POST /api/v1/expenses
 */
// export async function createExpense(data: ExpenseForm): Promise<ApiResponse<ExpenseItem>> {
//   return http.post('/expenses', data)
// }

/**
 * 编辑报销
 * PUT /api/v1/expenses/{id}
 */
// export async function updateExpense(id: number, data: Partial<ExpenseForm>): Promise<ApiResponse<ExpenseItem>> {
//   return http.put(`/expenses/${id}`, data)
// }

/**
 * 删除报销（软删除）
 * DELETE /api/v1/expenses/{id}
 */
// export async function deleteExpense(id: number): Promise<ApiResponse<null>> {
//   return http.delete(`/expenses/${id}`)
// }

export {}