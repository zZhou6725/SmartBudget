/** 用户个人信息（对齐后端 UserProfileResponse） */
export interface UserProfile {
  id: number
  username: string
  realName: string
  email: string
  phone: string
  deptName: string
  role: string
  avatar: string
}

/** 更新个人信息表单（对齐后端 ProfileUpdate） */
export interface ProfileForm {
  realName: string
  email: string
  phone: string
}

/** 修改密码表单（对齐后端 PasswordChange） */
export interface PasswordForm {
  oldPassword: string
  newPassword: string
}