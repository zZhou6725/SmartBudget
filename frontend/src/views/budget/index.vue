<template>
  <div class="budget">
    <PageCard>
      <template #title>预算管理</template>
      <template #extra>
        <el-button type="primary" @click="openCreateDialog">+ 新增预算</el-button>
      </template>

      <!-- 统计摘要 -->
      <el-row :gutter="16" class="budget__summary">
        <el-col :span="6">
          <div class="budget__summary-item" style="border-top-color: var(--color-primary)">
            <span class="budget__summary-dot" style="background: var(--color-primary)" />
            <span class="budget__summary-label">总预算</span>
            <span class="budget__summary-value" style="color: var(--color-primary)">{{ fmt(summary.totalBudget) }}</span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="budget__summary-item" style="border-top-color: var(--color-warning)">
            <span class="budget__summary-dot" style="background: var(--color-warning)" />
            <span class="budget__summary-label">已使用</span>
            <span class="budget__summary-value" style="color: var(--color-warning)">{{ fmt(summary.totalUsed) }}</span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="budget__summary-item" style="border-top-color: var(--color-success)">
            <span class="budget__summary-dot" style="background: var(--color-success)" />
            <span class="budget__summary-label">剩余</span>
            <span class="budget__summary-value" style="color: var(--color-success)">{{ fmt(summary.totalRemaining) }}</span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="budget__summary-item" style="border-top-color: var(--color-purple)">
            <span class="budget__summary-dot" style="background: var(--color-purple)" />
            <span class="budget__summary-label">平均使用率</span>
            <span class="budget__summary-value" style="color: var(--color-purple)">{{ summary.avgUsageRate }}%</span>
          </div>
        </el-col>
      </el-row>

      <!-- 筛选 -->
      <el-form inline class="budget__filter">
        <el-form-item label="关键字">
          <el-input v-model="filterKeyword" placeholder="部门名称" clearable />
        </el-form-item>
        <el-form-item label="部门">
          <el-select v-model="filterDeptName" placeholder="全部" clearable>
            <el-option v-for="d in deptOptions" :key="d" :label="d" :value="d" />
          </el-select>
        </el-form-item>
        <el-form-item label="年份">
          <el-select v-model="filterYear" placeholder="全部" clearable>
            <el-option v-for="y in yearOptions" :key="y" :label="String(y)" :value="y" />
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
        :total="total"
        :current-page="page"
        :page-size="pageSize"
        @page-change="handlePageChange"
        @size-change="handleSizeChange"
      >
        <el-table-column label="部门" prop="deptName" width="120" />
        <el-table-column label="年份" prop="year" width="80" />
        <el-table-column label="预算总额" width="130">
          <template #default="{ row }">¥{{ row.totalAmount.toLocaleString() }}</template>
        </el-table-column>
        <el-table-column label="已使用" width="130">
          <template #default="{ row }">¥{{ row.usedAmount.toLocaleString() }}</template>
        </el-table-column>
        <el-table-column label="剩余" width="130">
          <template #default="{ row }">¥{{ row.remaining.toLocaleString() }}</template>
        </el-table-column>
        <el-table-column label="使用率" width="160">
          <template #default="{ row }">
            <div class="budget__usage">
              <el-progress
                :percentage="row.usageRate"
                :color="usageColor(row.usageRate)"
                :stroke-width="8"
              />
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button size="small" text type="primary" @click="openAdjustDialog(row)">
              调整
            </el-button>
            <el-button size="small" text type="primary" @click="openEditDialog(row)">
              编辑
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

    <!-- 新增/编辑 Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑预算' : '新增预算'"
      width="480px"
    >
      <el-form :model="form" label-width="90px">
        <el-form-item label="部门" required>
          <el-select v-model="form.deptName" placeholder="请选择">
            <el-option v-for="d in deptOptions" :key="d" :label="d" :value="d" />
          </el-select>
        </el-form-item>
        <el-form-item label="年份" required>
          <el-input-number v-model="form.year" :min="2020" :max="2030" />
        </el-form-item>
        <el-form-item label="预算总额" required>
          <el-input-number v-model="form.totalAmount" :min="0" :precision="2" placeholder="请输入" />
          <span class="budget__unit">元</span>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>

    <!-- 预算调整 Dialog -->
    <el-dialog
      v-model="adjustVisible"
      title="预算调整"
      width="480px"
    >
      <template v-if="adjustTarget">
        <el-descriptions :column="2" border size="small" class="budget__adjust-info">
          <el-descriptions-item label="部门">{{ adjustTarget.deptName }}</el-descriptions-item>
          <el-descriptions-item label="年份">{{ adjustTarget.year }}</el-descriptions-item>
          <el-descriptions-item label="预算总额">¥{{ adjustTarget.totalAmount.toLocaleString() }}</el-descriptions-item>
          <el-descriptions-item label="已使用">¥{{ adjustTarget.usedAmount.toLocaleString() }}</el-descriptions-item>
          <el-descriptions-item label="当前剩余" :span="2">
            ¥{{ adjustTarget.remaining.toLocaleString() }}
          </el-descriptions-item>
        </el-descriptions>
        <el-form :model="adjustForm" label-width="90px" class="budget__adjust-form">
          <el-form-item label="调整方向" required>
            <el-radio-group v-model="adjustForm.direction">
              <el-radio value="add">追加预算</el-radio>
              <el-radio value="subtract">削减预算</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="调整金额" required>
            <el-input-number v-model="adjustForm.amount" :min="0" :precision="2" />
            <span class="budget__unit">元</span>
          </el-form-item>
          <el-form-item label="调整原因">
            <el-input v-model="adjustForm.reason" type="textarea" :rows="2" placeholder="请输入调整原因（选填）" />
          </el-form-item>
        </el-form>
      </template>
      <template #footer>
        <el-button @click="adjustVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAdjust">确认调整</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import PageCard from '@/components/PageCard.vue'
import TableWrapper from '@/components/TableWrapper.vue'
import type { BudgetItem, BudgetForm, BudgetAdjustForm, BudgetSummary } from '@/types/budget'
import {
  getBudgetList, getBudgetSummary, createBudget, updateBudget,
  adjustBudget, deleteBudget,
} from '@/api/modules/budget'
import { getDeptList } from '@/api/modules/organization'

const summary = ref<BudgetSummary>({ totalBudget: 0, totalUsed: 0, totalRemaining: 0, avgUsageRate: 0 })
const filterKeyword = ref('')
const filterDeptName = ref('')
const filterYear = ref<number | null>(null)
const yearOptions = ref<number[]>([2024, 2025, 2026, 2027])

const deptOptions = ref<string[]>([])
const tableData = ref<BudgetItem[]>([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const dialogVisible = ref(false); const isEdit = ref(false); const editId = ref<number | null>(null)
const form = ref<BudgetForm>({ deptName: '', year: 2026, totalAmount: 0 })
const adjustVisible = ref(false); const adjustTarget = ref<BudgetItem | null>(null)
const adjustForm = ref<BudgetAdjustForm>({ direction: 'add', amount: 0, reason: '' })

function fmt(v: number) { return v ? `¥${v.toLocaleString()}` : '--' }
function usageColor(rate: number) { return rate > 80 ? 'var(--color-danger)' : rate > 60 ? 'var(--color-warning)' : 'var(--color-primary)' }

async function fetchList() {
  try {
    const q: Record<string, unknown> = {
      keyword: filterKeyword.value || undefined,
      dept_name: filterDeptName.value || undefined,
      year: filterYear.value || undefined,
      page: page.value,
      page_size: pageSize.value,
    }
    const res = await getBudgetList(q as Record<string, unknown>)
    if (res.code === 0) { tableData.value = res.data.items; total.value = res.data.total }
  } catch { /* ignore */ }
}

async function fetchSummary() {
  try {
    const res = await getBudgetSummary()
    if (res.code === 0) summary.value = res.data as BudgetSummary
  } catch { /* ignore */ }
}

async function fetchDeptOptions() {
  try {
    const res = await getDeptList()
    if (res.code === 0 && Array.isArray(res.data)) {
      deptOptions.value = res.data.map((d: { name: string }) => d.name)
    }
  } catch { /* ignore */ }
}

function handleQuery() { page.value = 1; fetchList() }
function handleReset() {
  filterKeyword.value = ''
  filterDeptName.value = ''
  filterYear.value = null
  page.value = 1
  pageSize.value = 10
  fetchList()
}
function handlePageChange(p: number) { page.value = p; fetchList() }
function handleSizeChange(s: number) { pageSize.value = s; page.value = 1; fetchList() }

function openCreateDialog() {
  isEdit.value = false; editId.value = null
  form.value = { deptName: '', year: 2026, totalAmount: 0 }
  dialogVisible.value = true
}
function openEditDialog(row: BudgetItem) {
  isEdit.value = true; editId.value = row.id
  form.value = { deptName: row.deptName, year: row.year, totalAmount: row.totalAmount }
  dialogVisible.value = true
}
async function handleSave() {
  if (!form.value.deptName || !form.value.totalAmount) {
    ElMessage.warning('请填写部门和预算总额')
    return
  }
  try {
    let res
    if (isEdit.value && editId.value) {
      res = await updateBudget(editId.value, form.value as Record<string, unknown>)
    } else {
      res = await createBudget(form.value as Record<string, unknown>)
    }
    if (res.code === 0) { ElMessage.success(isEdit.value ? '编辑成功' : '新增成功'); dialogVisible.value = false; fetchList(); fetchSummary() }
    else { ElMessage.error(res.msg || '操作失败') }
  } catch (e: any) {
    const msg = e?.response?.data?.detail?.[0]?.msg || e?.response?.data?.msg || '网络错误'
    ElMessage.error(msg)
  }
}

function openAdjustDialog(row: BudgetItem) {
  adjustTarget.value = row
  adjustForm.value = { direction: 'add', amount: 0, reason: '' }
  adjustVisible.value = true
}
async function handleAdjust() {
  if (!adjustTarget.value) return
  if (!adjustForm.value.amount) { ElMessage.warning('请输入调整金额'); return }
  try {
    const res = await adjustBudget(adjustTarget.value.id, adjustForm.value as Record<string, unknown>)
    if (res.code === 0) { ElMessage.success('调整成功'); adjustVisible.value = false; fetchList(); fetchSummary() }
    else { ElMessage.error(res.msg || '操作失败') }
  } catch (e: any) {
    const msg = e?.response?.data?.detail?.[0]?.msg || e?.response?.data?.msg || '网络错误'
    ElMessage.error(msg)
  }
}

async function handleDelete(id: number) {
  try {
    const res = await deleteBudget(id)
    if (res.code === 0) { ElMessage.success('删除成功'); fetchList(); fetchSummary() }
    else { ElMessage.error(res.msg || '删除失败') }
  } catch (e: any) {
    const msg = e?.response?.data?.detail?.[0]?.msg || e?.response?.data?.msg || '网络错误'
    ElMessage.error(msg)
  }
}

onMounted(() => { fetchList(); fetchSummary(); fetchDeptOptions() })
</script>

<style scoped>
.budget__summary { margin-bottom: 16px; }
.budget__summary-item {
  background: var(--bg-card);
  border: 1px solid var(--border-normal);
  border-top: 3px solid var(--color-primary);
  border-radius: var(--border-radius-base);
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  box-shadow: var(--box-shadow-base);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.budget__summary-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
.budget__summary-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  margin-bottom: 2px;
}
.budget__summary-label { font-size: 12px; color: var(--text-placeholder); }
.budget__summary-value { font-size: 20px; font-weight: 700; }
.budget__summary-item--warning .budget__summary-value { color: var(--color-warning); }
.budget__summary-item--success .budget__summary-value { color: var(--color-success); }
.budget__filter { margin-bottom: 16px; }
.budget__usage { min-width: 120px; }
.budget__unit { margin-left: 8px; font-size: 13px; color: var(--text-placeholder); }
.budget__adjust-info { margin-bottom: 16px; }
.budget__adjust-form { margin-top: 16px; }
</style>