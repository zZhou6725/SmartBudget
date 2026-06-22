/** 聊天消息角色 */
export type ChatRole = 'user' | 'ai'

/** 单条聊天消息 */
export interface ChatItem {
  id: string
  /** 消息发送方 */
  role: ChatRole
  /** 消息内容（支持markdown） */
  content: string
  /** 发送时间 ISO 字符串 */
  time: string
}