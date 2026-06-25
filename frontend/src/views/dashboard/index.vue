<template>
  <div class="dashboard">
    <PageCard>
      <template #title>数据看板</template>
      <template #extra>
        <el-select v-model="selectedMonth" placeholder="月份" size="small" @change="fetchAll">
          <el-option v-for="m in monthOptions" :key="m" :label="m" :value="m" />
        </el-select>
        <el-select v-model="selectedDept" placeholder="部门" size="small" clearable @change="fetchAll">
          <el-option v-for="d in deptOptions" :key="d" :label="d" :value="d" />
        </el-select>
      </template>

      <el-row :gutter="16">
        <!-- 支出趋势折线图 -->
        <el-col :xs="24" :lg="12">
          <ChartContainer title="支出趋势" :empty="trendData.length === 0">
            <v-chart class="dashboard__chart" :option="trendOption" autoresize />
          </ChartContainer>
        </el-col>

        <!-- 部门支出排名柱状图 -->
        <el-col :xs="24" :lg="12">
          <ChartContainer title="部门支出排名" :empty="deptRankData.length === 0">
            <v-chart class="dashboard__chart" :option="deptRankOption" autoresize />
          </ChartContainer>
        </el-col>

        <!-- 费用类型饼图 -->
        <el-col :xs="24" :lg="12">
          <ChartContainer title="费用类型占比" :empty="categoryPieData.length === 0">
            <v-chart class="dashboard__chart" :option="categoryPieOption" autoresize />
          </ChartContainer>
        </el-col>

        <!-- 预算执行对比 -->
        <el-col :xs="24" :lg="12">
          <ChartContainer title="预算执行对比" :empty="budgetExecData.length === 0">
            <v-chart class="dashboard__chart" :option="budgetExecOption" autoresize />
          </ChartContainer>
        </el-col>
      </el-row>
    </PageCard>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart, PieChart } from 'echarts/charts'
import {
  TitleComponent, TooltipComponent, LegendComponent, GridComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'
import PageCard from '@/components/PageCard.vue'
import ChartContainer from '@/components/ChartContainer.vue'
import type { TrendItem, DeptRankItem, CategoryPieItem, BudgetExecItem } from '@/types/dashboard'
import { getTrend, getDeptRank, getCategoryPie, getBudgetExec } from '@/api/modules/dashboard'
import { ExpenseCategoryMap } from '@/types/expense'

const CATEGORY_COLORS: Record<string, string> = {
  travel: '#165DFF',
  office: '#00B42A',
  entertainment: '#FF7D00',
  transport: '#722ED1',
  other: '#86909C',
}

function categoryLabel(cat: string) {
  return ExpenseCategoryMap[cat] || cat || '其他'
}

use([CanvasRenderer, LineChart, BarChart, PieChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent])

const selectedMonth = ref('')
const selectedDept = ref('')
const monthOptions = ref<string[]>([])
const deptOptions = ref<string[]>([])

const trendData = ref<TrendItem[]>([])
const deptRankData = ref<DeptRankItem[]>([])
const categoryPieData = ref<CategoryPieItem[]>([])
const budgetExecData = ref<BudgetExecItem[]>([])

const trendOption = computed(() => ({
  tooltip: { trigger: 'axis' as const },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'category' as const, data: trendData.value.map(d => d.month), axisLabel: { rotate: 45 } },
  yAxis: { type: 'value' as const, axisLabel: { formatter: (v: number) => `¥${(v / 10000).toFixed(0)}万` } },
  series: [{
    type: 'line' as const, name: '支出金额',
    data: trendData.value.map(d => d.amount),
    smooth: true, areaStyle: { opacity: 0.1 },
    itemStyle: { color: '#165DFF' },
  }],
}))

const deptRankOption = computed(() => ({
  tooltip: { trigger: 'axis' as const },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'category' as const, data: deptRankData.value.map(d => d.deptName), axisLabel: { rotate: 30 } },
  yAxis: { type: 'value' as const, axisLabel: { formatter: (v: number) => `¥${(v / 10000).toFixed(0)}万` } },
  series: [{
    type: 'bar' as const, name: '支出金额',
    data: deptRankData.value.map(d => d.amount),
    itemStyle: { color: '#165DFF', borderRadius: [4, 4, 0, 0] },
  }],
}))

const categoryPieOption = computed(() => ({
  tooltip: { trigger: 'item' as const, formatter: '{b}: ¥{c} ({d}%)' },
  legend: { bottom: 0 },
  series: [{
    type: 'pie' as const, radius: ['45%', '70%'], center: ['50%', '45%'],
    data: categoryPieData.value.map(d => ({
      name: categoryLabel(d.category),
      value: d.amount,
      itemStyle: { color: CATEGORY_COLORS[d.category] || CATEGORY_COLORS.other },
    })),
    label: { formatter: '{b}\n{d}%' },
    itemStyle: { borderRadius: 4, borderColor: '#fff', borderWidth: 2 },
  }],
}))

const budgetExecOption = computed(() => ({
  tooltip: { trigger: 'axis' as const },
  legend: { data: ['预算金额', '实际支出'], bottom: 0 },
  grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
  xAxis: { type: 'category' as const, data: budgetExecData.value.map(d => d.deptName), axisLabel: { rotate: 30 } },
  yAxis: { type: 'value' as const, axisLabel: { formatter: (v: number) => `¥${(v / 10000).toFixed(0)}万` } },
  series: [
    {
      type: 'bar' as const, name: '预算金额',
      data: budgetExecData.value.map(d => d.budget),
      itemStyle: { color: '#165DFF', borderRadius: [4, 4, 0, 0] },
    },
    {
      type: 'bar' as const, name: '实际支出',
      data: budgetExecData.value.map(d => d.used),
      itemStyle: { color: '#FF7D00', borderRadius: [4, 4, 0, 0] },
    },
  ],
}))

async function fetchAll() {
  try {
    const [trend, rank, pie, exec] = await Promise.all([
      getTrend(selectedMonth.value || undefined, selectedDept.value || undefined),
      getDeptRank(selectedMonth.value || undefined),
      getCategoryPie(selectedMonth.value || undefined, selectedDept.value || undefined),
      getBudgetExec(),
    ])
    if (trend.code === 0) trendData.value = trend.data as TrendItem[]
    if (rank.code === 0) deptRankData.value = rank.data as DeptRankItem[]
    if (pie.code === 0) categoryPieData.value = pie.data as CategoryPieItem[]
    if (exec.code === 0) budgetExecData.value = exec.data as BudgetExecItem[]
  } catch { /* keep empty state */ }
}

onMounted(async () => {
  try {
    const [trend, rank, pie, exec] = await Promise.all([
      getTrend(), getDeptRank(), getCategoryPie(), getBudgetExec(),
    ])
    if (trend.code === 0 && trend.data) {
      trendData.value = trend.data as TrendItem[]
      monthOptions.value = [...new Set(trendData.value.map(d => d.month))].sort()
    }
    if (rank.code === 0 && rank.data) {
      deptRankData.value = rank.data as DeptRankItem[]
      deptOptions.value = deptRankData.value.map(d => d.deptName)
    }
    if (pie.code === 0) categoryPieData.value = pie.data as CategoryPieItem[]
    if (exec.code === 0) budgetExecData.value = exec.data as BudgetExecItem[]
  } catch { /* keep empty state */ }
})
</script>

<style scoped>
.dashboard__chart {
  min-height: 280px;
  width: 100%;
}
</style>