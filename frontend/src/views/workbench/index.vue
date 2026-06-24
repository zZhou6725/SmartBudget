<template>
  <div class="workbench">
    <!-- 概览统计卡片 -->
    <PageCard class="workbench__section">
      <template #title>概览统计</template>
      <el-row :gutter="16">
        <el-col v-for="stat in statCards" :key="stat.title" :xs="24" :sm="12" :md="8" :lg="4" :xl="4">
          <StatCard
            :title="stat.title"
            :value="stat.value"
            :subtitle="stat.subtitle"
          />
        </el-col>
      </el-row>
    </PageCard>

    <!-- 下半区双栏 -->
    <el-row :gutter="16" class="workbench__row">
      <!-- 左侧：待办审批列表 -->
      <el-col :xs="24" :lg="14">
        <PageCard>
          <template #title>待办审批</template>
          <TableWrapper
            :data="pendingList"
            :empty="pendingList.length === 0"
            :show-pagination="false"
          >
            <el-table-column label="审批标题" prop="title" min-width="160" />
            <el-table-column label="申请人" prop="applicant" width="100" />
            <el-table-column label="金额" prop="amount" width="120">
              <template #default="{ row }">
                ¥{{ row.amount.toLocaleString() }}
              </template>
            </el-table-column>
            <el-table-column label="提交时间" prop="time" width="160" />
            <el-table-column label="状态" prop="status" width="100">
              <template #default="{ row }">
                <el-tag :type="statusTagType(row.status)" size="small">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </TableWrapper>
        </PageCard>
      </el-col>

      <!-- 右侧：支出趋势图 -->
      <el-col :xs="24" :lg="10">
        <ChartContainer
          title="支出趋势"
          :empty="trendData.length === 0"
        >
          <div class="workbench__chart-placeholder">
            图表组件将在数据看板模块集成
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
  { title: '总预算', value: overview.value.totalBudget, subtitle: '本年度总预算' },
  { title: '总支出', value: overview.value.totalExpense, subtitle: '本年度累计支出' },
  { title: '剩余余额', value: overview.value.remainingBalance, subtitle: '预算剩余可用' },
  { title: '待审批数', value: overview.value.pendingApprovals, subtitle: '待处理审批单' },
  { title: '超预算部门', value: overview.value.overBudgetDepts, subtitle: '已超出预算' },
])

const pendingList = ref<PendingApprovalItem[]>([])
const trendData = ref<TrendPoint[]>([])

function statusTagType(status: string): string {
  const map: Record<string, string> = {
    draft: 'info',
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
  }
  return map[status] || 'info'
}

onMounted(async () => {
  try {
    const [ov, list, trend] = await Promise.all([
      getWorkbenchOverview(),
      getPendingApprovals({ page: 1, pageSize: 10 }),
      getExpenseTrend(),
    ])
    if (ov.code === 0) overview.value = ov.data
    if (list.code === 0) pendingList.value = list.data.items
    if (trend.code === 0) trendData.value = trend.data
  } catch { /* 网络错误时保持空状态 */ }
})
</script>

<style scoped>
.workbench__section {
  margin-bottom: 16px;
}

.workbench__row {
  margin-bottom: 16px;
}

.workbench__chart-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 280px;
  color: var(--text-placeholder);
  font-size: 14px;
}
</style>