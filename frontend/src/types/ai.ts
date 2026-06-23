/** 快捷提问标签 */
export interface QuickPrompt {
  id: string
  text: string
}

/** AI 消息（扩展 ChatItem） */
export interface AIReply {
  content: string
  thinking: string
  sources: string[]
}

/** AI 对话请求（对齐后端 AIChatRequest） */
export interface AIChatRequest {
  message: string
}

/** 票据校验请求（对齐后端 ReceiptValidateRequest） */
export interface ReceiptValidateRequest {
  content: string
}

/** 票据校验结果（对齐后端 ReceiptValidateResponse） */
export interface ReceiptValidateResult {
  amount: number | null
  category: string
  date: string
  vendor: string
  confidence: number
}