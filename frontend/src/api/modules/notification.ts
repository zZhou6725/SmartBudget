import type { ApiResponse, PageResult } from '@/types/global'
import type { NotificationItem } from '@/types/notification'

// import http from '@/api/index'

/**
 * 获取消息分页列表
 * GET /api/v1/notifications
 */
// export async function getNotificationList(params: Record<string, unknown>): Promise<ApiResponse<PageResult<NotificationItem>>> {
//   return http.get('/notifications', params)
// }

/**
 * 未读消息数量
 * GET /api/v1/notifications/unread-count
 */
// export async function getUnreadCount(): Promise<ApiResponse<number>> {
//   return http.get('/notifications/unread-count')
// }

/**
 * 标记已读
 * PUT /api/v1/notifications/{id}/read
 */
// export async function markAsRead(id: number): Promise<ApiResponse<null>> {
//   return http.put(`/notifications/${id}/read`)
// }

/**
 * 全部已读
 * PUT /api/v1/notifications/read-all
 */
// export async function markAllAsRead(): Promise<ApiResponse<null>> {
//   return http.put('/notifications/read-all')
// }

/**
 * 删除消息
 * DELETE /api/v1/notifications/{id}
 */
// export async function deleteNotification(id: number): Promise<ApiResponse<null>> {
//   return http.delete(`/notifications/${id}`)
// }

export {}