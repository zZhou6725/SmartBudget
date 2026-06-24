<template>
  <div class="login-page">
    <!-- 左侧品牌区 -->
    <div class="login__brand">
      <div class="login__brand-bg">
        <div v-for="i in 6" :key="i" class="login__shape" :style="shapeStyle(i)" />
      </div>
      <div class="login__brand-content">
        <div class="login__logo">
          <el-icon :size="48"><Setting /></el-icon>
        </div>
        <h1 class="login__app-name">FinBalance</h1>
        <p class="login__app-desc">财衡中台 · 企业预算管理平台</p>
      </div>
    </div>

    <!-- 右侧表单区 -->
    <div class="login__form-area">
      <div class="login__card">
        <h2 class="login__title" v-motion>欢迎登录</h2>
        <p class="login__subtitle">请输入您的账号信息</p>

        <el-form
          ref="formRef"
          :model="form"
          class="login__form"
          @keyup.enter="handleLogin"
        >
          <!-- 用户名 -->
          <div class="login__input-wrap" :class="{ 'login__input-wrap--error': shakeUser }">
            <el-input
              v-model="form.username"
              placeholder="用户名"
              size="large"
              :prefix-icon="User"
              class="login__input"
              @focus="shakeUser = false"
            />
          </div>

          <!-- 密码 -->
          <div class="login__input-wrap" :class="{ 'login__input-wrap--error': shakePwd }">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="密码"
              size="large"
              :prefix-icon="Lock"
              show-password
              class="login__input"
              @focus="shakePwd = false"
            />
          </div>

          <!-- 记住我 -->
          <div class="login__options">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          </div>

          <!-- 错误提示 -->
          <transition name="fade">
            <p v-if="errorMsg" class="login__error">{{ errorMsg }}</p>
          </transition>

          <!-- 登录按钮 -->
          <el-button
            type="primary"
            size="large"
            class="login__btn"
            :loading="loading"
            :disabled="!form.username || !form.password"
            @click="handleLogin"
          >
            <span v-if="!loading">登 录</span>
            <span v-else>验证中...</span>
          </el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock, Setting } from '@element-plus/icons-vue'
import { login } from '@/api/modules/auth'

const router = useRouter()

const form = reactive({ username: '', password: '' })
const rememberMe = ref(false)
const loading = ref(false)
const errorMsg = ref('')
const shakeUser = ref(false)
const shakePwd = ref(false)

function shapeStyle(i: number) {
  const sizes = [120, 80, 60, 90, 50, 70]
  const tops = ['5%', '25%', '55%', '70%', '15%', '85%']
  const lefts = ['10%', '60%', '30%', '75%', '50%', '20%']
  const delays = ['0s', '1s', '2s', '0.5s', '1.5s', '2.5s']
  const s = sizes[i - 1]
  return {
    width: `${s}px`,
    height: `${s}px`,
    top: tops[i - 1],
    left: lefts[i - 1],
    animationDelay: delays[i - 1],
  }
}

async function handleLogin() {
  errorMsg.value = ''
  if (!form.username) { shakeUser.value = true; return }
  if (!form.password) { shakePwd.value = true; return }

  loading.value = true
  try {
    const res = await login({ username: form.username, password: form.password })
    if (res.code !== 0) {
      errorMsg.value = res.msg || '登录失败'
      return
    }
    localStorage.setItem('finbalance-token', res.data.token)
    router.push('/workbench')
  } catch {
    errorMsg.value = '网络错误，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* ===== 左侧品牌区 ===== */
.login__brand {
  flex: 1;
  background: linear-gradient(135deg, #165DFF 0%, #3D7FFF 50%, #6499FF 100%);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.login__brand-bg {
  position: absolute;
  inset: 0;
}

.login__shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  animation: floatShape 6s ease-in-out infinite;
}

@keyframes floatShape {
  0%, 100% { transform: translateY(0) scale(1); opacity: 0.6; }
  50% { transform: translateY(-30px) scale(1.1); opacity: 1; }
}

.login__brand-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: #fff;
}

.login__logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 96px;
  height: 96px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  margin-bottom: 24px;
  animation: logoPulse 3s ease-in-out infinite;
}

@keyframes logoPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(255,255,255,0.3); }
  50% { box-shadow: 0 0 0 20px rgba(255,255,255,0); }
}

.login__app-name {
  font-size: 36px;
  font-weight: 700;
  letter-spacing: 2px;
  margin-bottom: 8px;
}

.login__app-desc {
  font-size: 15px;
  opacity: 0.85;
  letter-spacing: 1px;
}

/* ===== 右侧表单区 ===== */
.login__form-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-page);
}

.login__card {
  width: 400px;
  padding: 48px 40px;
  background: var(--bg-card);
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
  animation: cardEnter 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes cardEnter {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.login__title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-title);
  margin-bottom: 4px;
}

.login__subtitle {
  font-size: 14px;
  color: var(--text-placeholder);
  margin-bottom: 32px;
}

.login__form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.login__input-wrap {
  transition: transform 0.15s ease;
}

.login__input-wrap--error {
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  15% { transform: translateX(-8px); }
  30% { transform: translateX(8px); }
  45% { transform: translateX(-6px); }
  60% { transform: translateX(6px); }
  75% { transform: translateX(-3px); }
  90% { transform: translateX(3px); }
}

.login__input :deep(.el-input__wrapper) {
  border-radius: 10px;
  transition: all 0.3s ease;
}

.login__input :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--color-primary-light) inset;
}

.login__options {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.login__btn {
  width: 100%;
  height: 46px;
  font-size: 16px;
  border-radius: 10px;
  letter-spacing: 2px;
  transition: all 0.3s ease;
  margin-top: 4px;
}

.login__btn:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(22, 93, 255, 0.3);
}

.login__error {
  color: var(--color-danger);
  font-size: 13px;
  text-align: center;
}

/* ===== 过渡 ===== */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .login__brand { display: none; }
  .login__card { width: 90%; padding: 32px 24px; }
}
</style>