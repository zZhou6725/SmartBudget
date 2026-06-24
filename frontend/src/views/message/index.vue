<template>
  <div class="message">
    <PageCard>
      <template #title>消息预警中心</template>
      <template #extra>
        <el-button @click="handleReadAll">全部已读</el-button>
      </template>

      <!-- 筛选 -->
      <el-form :model="query" inline class="message__filter">
        <el-form-item label="类型">
          <el-select v-model="query.type" placeholder="全部" clearable>
            <el-option v-for="(label, value) in NotifyTypeMap" :key="value" :label="label" :value="value" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="query.status" placeholder="全部" clearable>
            <el-option v-for="(label, value) in NotifyStatusMap" :key="value" :label="label" :value="value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <TableWrapper
        :data="tableData"
        :empty="tableData.length === 0"
        :show-pagination="true"
        :total="pagination.total"
        :current-page="pagination.page"
        :page-size="pagination.pageSize"
        @page-change="handlePageChange"
        @size-change="handleSizeChange"
      >
        <el-table-column label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="typeTagType(row.type)" size="small">
              {{ NotifyTypeMap[row.type] || row.type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="标题" prop="title" min-width="180" />
        <el-table-column label="内容摘要" prop="summary" min-width="200">
          <template #default="{ row }">
            <span class="message__summary">{{ row.summary }}</span>
          </template>
        </el-table-column>
        <el-table-column label="时间" prop="createdAt" width="160" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <span :class="['message__status-dot', row.status === 'unread' ? 'message__status-dot--unread' : '']" />
            {{ NotifyStatusMap[row.status] }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'unread'"
              size="small"
              text
              type="primary"
              @click="handleMarkRead(row.id)"
            >
              标记已读
            </el-button>
            <el-popconfirm title="确认删除？" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button size="small" text type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </TableWrapper>
    </PageCard>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import PageCard from '@/components/PageCard.vue'
import TableWrapper from '@/components/TableWrapper.vue'
import { NotifyTypeMap, NotifyStatusMap, type NotificationItem } from '@/types/notification'

const query = ref({ type: '', status: '', page: 1, pageSize: 10 })
const tableData = ref<NotificationItem[]>([])
const pagination = reactive({ page: 1, pageSize: 10, total: 0 })

function typeTagType(type: string) { return type === 'alert' ? 'danger' : type === 'approval' ? 'warning' : 'info' }

function handleQuery() { query.value.page = 1 }
function handleReset() { query.value = { type: '', status: '', page: 1, pageSize: 10 } }
function handlePageChange(p: number) { pagination.page = p }
function handleSizeChange(s: number) { pagination.pageSize = s }
function handleMarkRead(id: number) { /* TODO */ }
function handleReadAll() { /* TODO */ }
function handleDelete(id: number) { /* TODO */ }
</script>

<style scoped>
.message__filter { margin-bottom: 16px; }
.message__summary { color: var(--text-placeholder); font-size: 13px; }
.message__status-dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: var(--text-placeholder); margin-right: 6px; }
.message__status-dot--unread { background: var(--color-primary); }
</style>