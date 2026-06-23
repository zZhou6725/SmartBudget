<template>
  <div class="table-wrapper">
    <div v-if="empty" class="table-wrapper__empty">
      <EmptyHolder text="暂无数据" />
    </div>
    <template v-else>
      <el-table
        :data="data"
        :stripe="stripe"
        class="table-wrapper__table"
        v-bind="$attrs"
      >
        <slot />
      </el-table>
      <div v-if="showPagination" class="table-wrapper__pagination">
        <el-pagination
          :current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          background
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import EmptyHolder from './EmptyHolder.vue'

interface Props {
  data: Record<string, unknown>[]
  empty?: boolean
  showPagination?: boolean
  currentPage?: number
  pageSize?: number
  total?: number
}

withDefaults(defineProps<Props>(), {
  data: () => [],
  empty: false,
  showPagination: false,
  currentPage: 1,
  pageSize: 10,
  total: 0,
  stripe: true,
})

const emit = defineEmits<{
  (e: 'page-change', page: number): void
  (e: 'size-change', size: number): void
}>()

function handlePageChange(page: number) {
  emit('page-change', page)
}

function handleSizeChange(size: number) {
  emit('size-change', size)
}
</script>

<style scoped>
.table-wrapper {
  background: var(--bg-card);
  border-radius: var(--border-radius-base);
}

.table-wrapper__table {
  width: 100%;
}

.table-wrapper__table :deep(.el-table__header th) {
  background: var(--bg-page);
  color: var(--text-title);
  font-weight: 600;
}

.table-wrapper__empty {
  padding: 48px 0;
}

.table-wrapper__pagination {
  display: flex;
  justify-content: flex-end;
  padding: 16px 0;
}
</style>
