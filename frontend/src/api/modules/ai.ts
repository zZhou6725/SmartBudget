import { get, post } from '@/api/index'
import type { ApiResponse } from '@/types/global'
import type { QuickPrompt, ReceiptValidateRequest, ReceiptValidateResult } from '@/types/ai'

export async function getQuickPrompts() {
  return get<QuickPrompt[]>('/ai/prompts')
}

export async function receiptValidate(data: ReceiptValidateRequest) {
  return post<ReceiptValidateResult>('/ai/receipt-validate', data as Record<string, unknown>)
}

export async function receiptUpload(file: File) {
  const form = new FormData()
  form.append('file', file)
  return post<ReceiptValidateResult>('/ai/receipt-upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

/**
 * 流式 AI 对话 — 返回 async generator，支持 AbortController 取消
 * 用法: const ctrl = new AbortController()
 *       for await (const chunk of streamChat(message, ctrl.signal)) { ... }
 */
export async function* streamChat(
  message: string,
  signal?: AbortSignal,
): AsyncGenerator<{ content: string; thinking: string; done: boolean }> {
  const token = localStorage.getItem('finbalance-token')
  const resp = await fetch('/api/v1/ai/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify({ message }),
    signal,
  })

  if (!resp.ok || !resp.body) {
    yield { content: `请求失败（${resp.status}）`, thinking: '', done: true }
    return
  }

  const reader = resp.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() || ''
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        try {
          const data = JSON.parse(line.slice(6))
          yield { content: data.content || '', thinking: data.thinking || '', done: !!data.done }
        } catch { /* skip parse errors */ }
      }
    }
  }
}