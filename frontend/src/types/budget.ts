/** 预算记录（对齐后端 BudgetResponse） */
export interface BudgetItem {
  id: number
  deptName: string
  year: number
  totalAmount: number
  usedAmount: number
  remaining: number
  usageRate: number
  createdAt: string
}

/** 新增/编辑预算表单（对齐后端 BudgetCreate / BudgetUpdate） */
export interface BudgetForm {
  deptName: string
  year: number
  totalAmount: number | null
}

/** 预算调整表单（对齐后端 BudgetAdjust） */
export interface BudgetAdjustForm {
  direction: 'add' | 'subtract'
  amount: number | null
  reason: string
}

/** 筛选查询参数 */
export interface BudgetQuery {
  keyword?: string
  deptName?: string
  year?: number
  page: number
  pageSize: number
}

/** 统计摘要（对齐后端 BudgetSummary） */
export interface BudgetSummary {
  totalBudget: number
  totalUsed: number
  totalRemaining: number
  avgUsageRate: number
}