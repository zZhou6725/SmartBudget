import type { ApiResponse } from '@/types/global'
import type { QuickPrompt, AIChatRequest, AIReply, ReceiptValidateRequest, ReceiptValidateResult } from '@/types/ai'

// import http from '@/api/index'

/**
 * AI 对话
 * POST /api/v1/ai/chat
 */
// export async function aiChat(data: AIChatRequest): Promise<ApiResponse<AIReply>> {
//   return http.post('/ai/chat', data)
// }

/**
 * 票据校验（LLM识别）
 * POST /api/v1/ai/receipt-validate
 */
// export async function receiptValidate(data: ReceiptValidateRequest): Promise<ApiResponse<ReceiptValidateResult>> {
//   return http.post('/ai/receipt-validate', data)
// }

/**
 * 获取快捷提问列表
 * GET /api/v1/ai/prompts
 */
// export async function getQuickPrompts(): Promise<ApiResponse<QuickPrompt[]>> {
//   return http.get('/ai/prompts')
// }

export {}