<template>
  <div class="page-card">
    <div v-if="$slots.title || $slots.extra" class="page-card__header">
      <div class="page-card__header-left">
        <span class="page-card__accent-bar" />
        <span class="page-card__title">
          <slot name="title" />
        </span>
      </div>
      <div class="page-card__extra">
        <slot name="extra" />
      </div>
    </div>
    <div class="page-card__body">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.page-card {
  background: var(--bg-card);
  border-radius: var(--border-radius-base);
  border: 1px solid var(--border-normal);
  box-shadow: var(--box-shadow-base);
  overflow: hidden;
}

.page-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px var(--page-padding);
  border-bottom: 1px solid var(--border-normal);
  background: linear-gradient(180deg, var(--color-primary-bg) 0%, var(--bg-card) 100%);
}

.page-card__header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-card__accent-bar {
  width: 3px;
  height: 18px;
  border-radius: 2px;
  background: var(--color-primary);
}

.page-card__title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-title);
}

.page-card__extra {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-card__body {
  padding: var(--page-padding);
}
</style>