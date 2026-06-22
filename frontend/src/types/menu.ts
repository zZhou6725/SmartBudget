/** 侧边栏菜单项 */
export interface MenuItem {
  /** 唯一标识，对应路由 name */
  id: string
  /** 菜单中文标题 */
  title: string
  /** Element Plus 图标名称 */
  icon: string
  /** 前端路由路径 */
  path: string
  /** 子菜单（可选，暂未使用） */
  children?: MenuItem[]
}