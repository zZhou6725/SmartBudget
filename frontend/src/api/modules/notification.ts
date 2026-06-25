import { get, put, del } from '@/api/index'
import type { PageResult } from '@/types/global'
import type { NotificationItem } from '@/types/notification'

export async function getNotificationList(params: Record<string, unknown>) {
  return get<PageResult<NotificationItem>>('/notifications', params)
}

export async function getUnreadCount() {
  return get<number>('/notifications/unread-count')
}

export async function markAsRead(id: number) {
  return put<null>(`/notifications/${id}/read`)
}

export async function markAllAsRead() {
  return put<null>('/notifications/read-all')
}

export async function deleteNotification(id: number) {
  return del<null>(`/notifications/${id}`)
}