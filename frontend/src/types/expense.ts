/** 报销类型 */
export const ExpenseCategoryMap: Record<string, string> = {
  travel: '差旅费',
  office: '办公费',
  entertainment: '招待费',
  transport: '交通费',
  other: '其他',
}
export type ExpenseCategory = 'travel' | 'office' | 'entertainment' | 'transport' | 'other'

/** 报销状态（前后端共用） */
export const ExpenseStatusMap: Record<string, string> = {
  draft: '草稿',
  pending: '待审批',
  approved: '已通过',
  rejected: '已驳回',
}
export type ExpenseStatus = 'draft' | 'pending' | 'approved' | 'rejected'

/** 报销记录（对齐后端 ExpenseResponse） */
export interface ExpenseItem {
  id: number
  expenseNo: string
  title: string
  category: ExpenseCategory
  deptName: string
  budgetId: number | null
  budgetName: string
  amount: number
  status: ExpenseStatus
  applicant: string
  applyDate: string
  remark: string
  attachmentUrl: string
  createdAt: string
}

/** 新增/编辑表单（对齐后端 ExpenseCreate / ExpenseUpdate） */
export interface ExpenseForm {
  title: string
  category: ExpenseCategory
  deptName: string
  budgetId: number | null
  amount: number | null
  applyDate: string
  remark: string
}

/** 筛选查询参数 */
export interface ExpenseQuery {
  keyword?: string
  category?: ExpenseCategory
  deptName?: string
  status?: ExpenseStatus
  startDate?: string
  endDate?: string
  page: number
  pageSize: number
}

/** 统计摘要（对齐后端 ExpenseSummary） */
export interface ExpenseSummary {
  totalAmount: number
  pendingCount: number
  approvedCount: number
  rejectedCount: number
}