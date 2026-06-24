<template>
  <div class="dashboard">
    <PageCard>
      <template #title>数据看板</template>
      <template #extra>
        <el-select v-model="selectedMonth" placeholder="月份" size="small">
          <el-option v-for="m in monthOptions" :key="m" :label="m" :value="m" />
        </el-select>
        <el-select v-model="selectedDept" placeholder="部门" size="small" clearable>
          <el-option v-for="d in deptOptions" :key="d" :label="d" :value="d" />
        </el-select>
      </template>

      <el-row :gutter="16">
        <!-- 支出趋势折线图 -->
        <el-col :xs="24" :lg="12">
          <ChartContainer title="支出趋势" :empty="trendData.length === 0">
            <div class="dashboard__chart-placeholder">折线图 — 12个月趋势</div>
          </ChartContainer>
        </el-col>

        <!-- 部门支出排名柱状图 -->
        <el-col :xs="24" :lg="12">
          <ChartContainer title="部门支出排名" :empty="deptRankData.length === 0">
            <div class="dashboard__chart-placeholder">柱状图 — Top5部门</div>
          </ChartContainer>
        </el-col>

        <!-- 费用类型饼图 -->
        <el-col :xs="24" :lg="12">
          <ChartContainer title="费用类型占比" :empty="categoryPieData.length === 0">
            <div class="dashboard__chart-placeholder">饼图 — 分类占比</div>
          </ChartContainer>
        </el-col>

        <!-- 预算执行对比 -->
        <el-col :xs="24" :lg="12">
          <ChartContainer title="预算执行对比" :empty="budgetExecData.length === 0">
            <div class="dashboard__chart-placeholder">条形图 — 预算 vs 实际</div>
          </ChartContainer>
        </el-col>
      </el-row>
    </PageCard>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PageCard from '@/components/PageCard.vue'
import ChartContainer from '@/components/ChartContainer.vue'
import type { TrendItem, DeptRankItem, CategoryPieItem, BudgetExecItem } from '@/types/dashboard'
import { getTrend, getDeptRank, getCategoryPie, getBudgetExec } from '@/api/modules/dashboard'

const selectedMonth = ref('')
const selectedDept = ref('')
const monthOptions = ref<string[]>([])
const deptOptions = ref<string[]>([])

const trendData = ref<TrendItem[]>([])
const deptRankData = ref<DeptRankItem[]>([])
const categoryPieData = ref<CategoryPieItem[]>([])
const budgetExecData = ref<BudgetExecItem[]>([])

onMounted(async () => {
  try {
    const [trend, rank, pie, exec] = await Promise.all([
      getTrend(), getDeptRank(), getCategoryPie(), getBudgetExec(),
    ])
    if (trend.code === 0) trendData.value = trend.data as TrendItem[]
    if (rank.code === 0) deptRankData.value = rank.data as DeptRankItem[]
    if (pie.code === 0) categoryPieData.value = pie.data as CategoryPieItem[]
    if (exec.code === 0) budgetExecData.value = exec.data as BudgetExecItem[]
  } catch { /* keep empty state */ }
})
</script>

<style scoped>
.dashboard__chart-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 280px;
  color: var(--text-placeholder);
  font-size: 14px;
}
</style>