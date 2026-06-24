<template>
  <div class="personal">
    <PageCard>
      <template #title>个人中心</template>

      <!-- 头像区 -->
      <div class="personal__avatar-area">
        <el-avatar :size="72" :src="profile.avatar || undefined">
          <el-icon :size="36"><UserFilled /></el-icon>
        </el-avatar>
        <div class="personal__avatar-info">
          <span class="personal__name">{{ profile.username || '未设置' }}</span>
          <span class="personal__dept">{{ profile.deptName || '--' }} · {{ RoleMap[profile.role] || profile.role }}</span>
        </div>
      </div>

      <!-- 基本信息表单 -->
      <el-form :model="form" label-width="90px" class="personal__form">
        <el-form-item label="用户名">
          <el-input :model-value="profile.username" disabled />
        </el-form-item>
        <el-form-item label="真实姓名">
          <el-input v-model="form.realName" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item>
          <el-button @click="openPasswordDialog">修改密码</el-button>
          <el-button type="primary" @click="handleSave">保存</el-button>
        </el-form-item>
      </el-form>
    </PageCard>

    <!-- 修改密码 Dialog -->
    <el-dialog v-model="passwordVisible" title="修改密码" width="400px">
      <el-form :model="passwordForm" label-width="90px">
        <el-form-item label="原密码" required>
          <el-input v-model="passwordForm.oldPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码" required>
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="passwordVisible = false">取消</el-button>
        <el-button type="primary" @click="handleChangePassword">确认修改</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UserFilled } from '@element-plus/icons-vue'
import PageCard from '@/components/PageCard.vue'
import { RoleMap } from '@/types/organization'
import type { UserProfile, ProfileForm, PasswordForm } from '@/types/profile'

const profile = ref<UserProfile>({
  id: 0, username: '', realName: '', email: '', phone: '', deptName: '', role: '', avatar: '',
})

const form = ref<ProfileForm>({ realName: '', email: '', phone: '' })
const passwordVisible = ref(false)
const passwordForm = ref<PasswordForm>({ oldPassword: '', newPassword: '' })

function handleSave() { /* TODO */ }
function openPasswordDialog() { passwordVisible.value = true }
function handleChangePassword() { passwordVisible.value = false }
</script>

<style scoped>
.personal__avatar-area {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px 0;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--border-normal);
}
.personal__avatar-info { display: flex; flex-direction: column; gap: 4px; }
.personal__name { font-size: 20px; font-weight: 600; color: var(--text-title); }
.personal__dept { font-size: 13px; color: var(--text-placeholder); }
.personal__form { max-width: 520px; }
</style>