/** 支出趋势数据点（对齐后端 TrendItem） */
export interface TrendItem {
  month: string
  amount: number
}

/** 部门支出排名（对齐后端 DeptRankItem） */
export interface DeptRankItem {
  deptName: string
  amount: number
  usageRate: number
}

/** 费用类型占比（对齐后端 CategoryPieItem） */
export interface CategoryPieItem {
  category: string
  amount: number
  percent: number
}

/** 预算执行情况（对齐后端 BudgetExecItem） */
export interface BudgetExecItem {
  deptName: string
  budget: number
  used: number
  rate: number
}