import http from '@/api/index'
import type { UserProfile, ProfileForm, PasswordForm } from '@/types/profile'

export async function getProfile() {
  return http.get<UserProfile>('/profile')
}

export async function updateProfile(data: ProfileForm) {
  return http.put<UserProfile>('/profile', data as Record<string, unknown>)
}

export async function changePassword(data: PasswordForm) {
  return http.put<null>('/profile/password', data as Record<string, unknown>)
}