/** 用户角色 */
export const RoleMap: Record<string, string> = {
  admin: '管理员',
  manager: '部门经理',
  finance: '财务',
  viewer: '查看者',
}
export type UserRole = 'admin' | 'manager' | 'finance' | 'viewer'

/** 部门 */
export interface DeptItem {
  id: number
  name: string
  manager: string
  memberCount: number
  totalBudget: number
}

/** 用户 */
export interface UserItem {
  id: number
  username: string
  realName: string
  deptName: string
  role: UserRole
  status: string
}

/** 部门表单 */
export interface DeptForm {
  name: string
  manager: string
}

/** 用户表单 */
export interface UserForm {
  username: string
  realName: string
  deptId: number | null
  role: UserRole
}