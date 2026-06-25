/** 聊天消息角色 */
export type ChatRole = 'user' | 'ai'

/** 单条聊天消息 */
export interface ChatItem {
  id: string
  role: ChatRole
  content: string
  /** 预渲染的 HTML 内容（缓存，避免每次重渲染都跑正则） */
  renderedContent?: string
  /** 思考过程 */
  thinking?: string
  time: string
}