/** 通知类型 */
export const NotifyTypeMap: Record<string, string> = {
  alert: '预算预警',
  notice: '系统通知',
  approval: '审批消息',
}
export type NotifyType = 'alert' | 'notice' | 'approval'

/** 消息状态 */
export const NotifyStatusMap: Record<string, string> = {
  unread: '未读',
  read: '已读',
}
export type NotifyStatus = 'unread' | 'read'

/** 消息记录（对齐后端 NotificationResponse） */
export interface NotificationItem {
  id: number
  type: NotifyType
  title: string
  summary: string
  content: string
  status: NotifyStatus
  createdAt: string
}