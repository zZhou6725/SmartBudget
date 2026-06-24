import { get, put } from '@/api/index'
import type { UserProfile, ProfileForm, PasswordForm } from '@/types/profile'

export async function getProfile() {
  return get<UserProfile>('/profile')
}

export async function updateProfile(data: ProfileForm) {
  return put<UserProfile>('/profile', data as Record<string, unknown>)
}

export async function changePassword(data: PasswordForm) {
  return put<null>('/profile/password', data as Record<string, unknown>)
}