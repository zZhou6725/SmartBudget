import http from '@/api/index'
import type { PageResult } from '@/types/global'
import type { NotificationItem } from '@/types/notification'

export async function getNotificationList(params: Record<string, unknown>) {
  return http.get<PageResult<NotificationItem>>('/notifications', params)
}

export async function getUnreadCount() {
  return http.get<number>('/notifications/unread-count')
}

export async function markAsRead(id: number) {
  return http.put<null>(`/notifications/${id}/read`)
}

export async function markAllAsRead() {
  return http.put<null>('/notifications/read-all')
}

export async function deleteNotification(id: number) {
  return http.del<null>(`/notifications/${id}`)
}