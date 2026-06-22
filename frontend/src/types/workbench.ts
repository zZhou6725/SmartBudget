/** 工作台概览统计（对齐后端 WorkbenchOverview schema） */
export interface WorkbenchOverview {
  totalBudget: number | null
  totalExpense: number | null
  remainingBalance: number | null
  pendingApprovals: number | null
  overBudgetDepts: number | null
}

/** 待审批事项（对齐后端 PendingApprovalItem schema） */
export interface PendingApprovalItem {
  id: number
  title: string
  applicant: string
  amount: number
  time: string
  status: string
}

/** 支出趋势数据点（对齐后端 TrendPoint schema） */
export interface TrendPoint {
  date: string
  amount: number
}