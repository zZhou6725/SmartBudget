<template>
  <div class="workbench">
    <PageCard class="workbench__section">
      <template #title>概览统计</template>
      <el-row :gutter="16">
        <el-col v-for="stat in statCards" :key="stat.title" :xs="24" :sm="12" :md="8" :lg="4" :xl="4">
          <StatCard
            :title="stat.title"
            :value="stat.value"
            :prefix="stat.prefix"
            :suffix="stat.suffix"
            :subtitle="stat.subtitle"
            :color="stat.color"
          />
        </el-col>
    </el-row>
  </PageCard>

  <el-row :gutter="16" class="workbench__row">
    <el-col :xs="24" :lg="14">
      <PageCard>
        <template #title>待办审批</template>
        <div v-loading="loadingApprovals" class="workbench__loading-wrap">
          <TableWrapper
            :data="pendingList"
            :empty="pendingList.length === 0"
            :show-pagination="false"
          >
            <el-table-column label="审批标题" prop="title" min-width="160" />
            <el-table-column label="申请人" prop="applicant" width="100" />
            <el-table-column label="金额" width="120">
              <template #default="{ row }">¥{{ row.amount.toLocaleString() }}</template>
            </el-table-column>
            <el-table-column label="提交时间" prop="time" width="120" />
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="statusTagType(row.status)" size="small">
                  {{ statusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
          </TableWrapper>
        </div>
      </PageCard>
    </el-col>

    <el-col :xs="24" :lg="10">
      <ChartContainer title="支出趋势" :empty="trendData.length === 0">
        <div class="workbench__trend-list">
          <div
            v-for="point in trendData"
            :key="point.date"
            class="workbench__trend-item"
          >
            <span class="workbench__trend-date">{{ point.date }}</span>
            <span class="workbench__trend-bar-bg">
              <span
                class="workbench__trend-bar"
                :style="{ width: trendBarWidth(point.amount) }"
              />
            </span>
            <span class="workbench__trend-amount">¥{{ point.amount.toLocaleString() }}</span>
          </div>
        </div>
      </ChartContainer>
    </el-col>
  </el-row>
</div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import PageCard from '@/components/PageCard.vue'
import StatCard from '@/components/StatCard.vue'
import TableWrapper from '@/components/TableWrapper.vue'
import ChartContainer from '@/components/ChartContainer.vue'
import type { WorkbenchOverview, PendingApprovalItem, TrendPoint } from '@/types/workbench'
import { getWorkbenchOverview, getPendingApprovals, getExpenseTrend } from '@/api/modules/workbench'

const overview = ref<WorkbenchOverview>({
  totalBudget: null,
  totalExpense: null,
  remainingBalance: null,
  pendingApprovals: null,
  overBudgetDepts: null,
})

const statCards = computed(() => [
  { title: '总预算', value: overview.value.totalBudget, prefix: '¥', subtitle: '本年度总预算', color: 'var(--color-primary)' },
  { title: '总支出', value: overview.value.totalExpense, prefix: '¥', subtitle: '本年度累计支出', color: 'var(--color-warning)' },
  { title: '剩余余额', value: overview.value.remainingBalance, prefix: '¥', subtitle: '预算剩余可用', color: 'var(--color-success)' },
  { title: '待审批数', value: overview.value.pendingApprovals, suffix: ' 笔', subtitle: '待处理审批单', color: 'var(--color-purple)' },
  { title: '超预算部门', value: overview.value.overBudgetDepts, suffix: ' 个', subtitle: '已超出预算', color: 'var(--color-danger)' },
])

const pendingList = ref<PendingApprovalItem[]>([])
const trendData = ref<TrendPoint[]>([])
const loadingOverview = ref(false)
const loadingApprovals = ref(false)
const loadingTrend = ref(false)

const maxTrendAmount = computed(() => Math.max(...trendData.value.map(t => t.amount), 1))

function trendBarWidth(amount: number): string {
  return `${(amount / maxTrendAmount.value) * 100}%`
}

const statusMap: Record<string, string> = {
  draft: '草稿', pending: '待审批', approved: '已通过', rejected: '已驳回',
}
function statusLabel(status: string): string { return statusMap[status] || status }
function statusTagType(status: string): string {
  if (status === 'pending') return 'warning'
  if (status === 'approved') return 'success'
  if (status === 'rejected') return 'danger'
  return 'info'
}

function fmtCurrency(v: number | null): string {
  if (v === null || v === undefined) return '--'
  return `¥${v.toLocaleString()}`
}

async function fetchOverview() {
  loadingOverview.value = true
  try {
    const res = await getWorkbenchOverview()
    if (res.code === 0) overview.value = res.data as WorkbenchOverview
  } catch { /* ignore */ }
  finally { loadingOverview.value = false }
}

async function fetchPending() {
  loadingApprovals.value = true
  try {
    const res = await getPendingApprovals({ page: 1, page_size: 10 })
    if (res.code === 0) pendingList.value = res.data?.items || []
  } catch { /* ignore */ }
  finally { loadingApprovals.value = false }
}

async function fetchTrend() {
  loadingTrend.value = true
  try {
    const res = await getExpenseTrend()
    if (res.code === 0 && Array.isArray(res.data)) trendData.value = res.data
  } catch { /* ignore */ }
  finally { loadingTrend.value = false }
}

onMounted(async () => {
  await Promise.all([fetchOverview(), fetchPending(), fetchTrend()])
})
</script>

<style scoped>
.workbench__section { margin-bottom: 16px; }
.workbench__row { margin-bottom: 16px; }
.workbench__loading-wrap { min-height: 200px; }

.workbench__trend-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 8px 0;
}
.workbench__trend-item {
  display: flex;
  align-items: center;
  gap: 12px;
}
.workbench__trend-date {
  width: 64px;
  font-size: 12px;
  color: var(--text-placeholder);
  text-align: right;
  flex-shrink: 0;
}
.workbench__trend-bar-bg {
  flex: 1;
  height: 18px;
  background: var(--bg-page);
  border-radius: 4px;
  overflow: hidden;
}
.workbench__trend-bar {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light));
  border-radius: 4px;
  min-width: 4px;
  transition: width 0.6s ease;
}
.workbench__trend-amount {
  width: 100px;
  font-size: 13px;
  color: var(--text-body);
  flex-shrink: 0;
}
</style>