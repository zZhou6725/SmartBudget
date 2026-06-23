import { defineStore } from 'pinia'
import { ref } from 'vue'

/** 用户简要信息（字段后续与后端 Pydantic 对齐） */
export interface UserInfo {
  id: number | null
  username: string
  avatar: string
  email: string
}

export const useUserStore = defineStore('user', () => {
  const userInfo = ref<UserInfo>({
    id: null,
    username: '',
    avatar: '',
    email: '',
  })

  /** 预留：登录后设置用户信息 */
  function setUserInfo(info: UserInfo) {
    userInfo.value = info
  }

  /** 预留：退出登录清空 */
  function clearUserInfo() {
    userInfo.value = { id: null, username: '', avatar: '', email: '' }
  }

  return {
    userInfo,
    setUserInfo,
    clearUserInfo,
  }
})