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
          <div class="budget__summary-item">
            <span class="budget__summary-label">总预算</span>
            <span class="budget__summary-value">{{ fmt(summary.totalBudget) }}</span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="budget__summary-item budget__summary-item--warning">
            <span class="budget__summary-label">已使用</span>
            <span class="budget__summary-value">{{ fmt(summary.totalUsed) }}</span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="budget__summary-item budget__summary-item--success">
            <span class="budget__summary-label">剩余</span>
            <span class="budget__summary-value">{{ fmt(summary.totalRemaining) }}</span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="budget__summary-item">
            <span class="budget__summary-label">平均使用率</span>
            <span class="budget__summary-value">{{ summary.avgUsageRate }}%</span>
          </div>
        </el-col>
      </el-row>

      <!-- 筛选 -->
      <el-form :model="query" inline class="budget__filter">
        <el-form-item label="关键字">
          <el-input v-model="query.keyword" placeholder="部门名称" clearable />
        </el-form-item>
        <el-form-item label="部门">
          <el-select v-model="query.deptName" placeholder="全部" clearable>
            <el-option v-for="d in deptOptions" :key="d" :label="d" :value="d" />
          </el-select>
        </el-form-item>
        <el-form-item label="年份">
          <el-select v-model="query.year" placeholder="全部" clearable>
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
        :total="pagination.total"
        :current-page="pagination.page"
        :page-size="pagination.pageSize"
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
import { ref, reactive } from 'vue'
import PageCard from '@/components/PageCard.vue'
import TableWrapper from '@/components/TableWrapper.vue'
import type { BudgetItem, BudgetForm, BudgetAdjustForm, BudgetQuery, BudgetSummary } from '@/types/budget'

/** 统计摘要 */
const summary = ref<BudgetSummary>({
  totalBudget: 0,
  totalUsed: 0,
  totalRemaining: 0,
  avgUsageRate: 0,
})

/** 筛选 */
const query = ref<BudgetQuery>({ keyword: '', page: 1, pageSize: 10 })
const deptOptions = ref<string[]>([])
const yearOptions = ref<number[]>([2024, 2025, 2026, 2027])

/** 表格 */
const tableData = ref<BudgetItem[]>([])
const pagination = reactive({ page: 1, pageSize: 10, total: 0 })

/** 新增/编辑 */
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref<number | null>(null)
const form = ref<BudgetForm>({ deptName: '', year: 2026, totalAmount: null })

/** 调整 */
const adjustVisible = ref(false)
const adjustTarget = ref<BudgetItem | null>(null)
const adjustForm = ref<BudgetAdjustForm>({ direction: 'add', amount: null, reason: '' })

function fmt(v: number) { return v ? `¥${v.toLocaleString()}` : '--' }
function usageColor(rate: number) { return rate > 80 ? 'var(--color-danger)' : rate > 60 ? 'var(--color-warning)' : 'var(--color-primary)' }

function handleQuery() { query.value.page = 1 }
function handleReset() { query.value = { page: 1, pageSize: 10 } }
function handlePageChange(p: number) { pagination.page = p }
function handleSizeChange(s: number) { pagination.pageSize = s }

function openCreateDialog() {
  isEdit.value = false; editId.value = null
  form.value = { deptName: '', year: 2026, totalAmount: null }
  dialogVisible.value = true
}
function openEditDialog(row: BudgetItem) {
  isEdit.value = true; editId.value = row.id
  form.value = { deptName: row.deptName, year: row.year, totalAmount: row.totalAmount }
  dialogVisible.value = true
}
function handleSave() { dialogVisible.value = false }

function openAdjustDialog(row: BudgetItem) {
  adjustTarget.value = row
  adjustForm.value = { direction: 'add', amount: null, reason: '' }
  adjustVisible.value = true
}
function handleAdjust() { adjustVisible.value = false }

function handleDelete(id: number) { /* TODO */ }
</script>

<style scoped>
.budget__summary { margin-bottom: 16px; }
.budget__summary-item {
  background: var(--bg-page);
  border-radius: var(--border-radius-base);
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.budget__summary-label { font-size: 12px; color: var(--text-placeholder); }
.budget__summary-value { font-size: 20px; font-weight: 600; color: var(--text-title); }
.budget__summary-item--warning .budget__summary-value { color: var(--color-warning); }
.budget__summary-item--success .budget__summary-value { color: var(--color-success); }
.budget__filter { margin-bottom: 16px; }
.budget__usage { min-width: 120px; }
.budget__unit { margin-left: 8px; font-size: 13px; color: var(--text-placeholder); }
.budget__adjust-info { margin-bottom: 16px; }
.budget__adjust-form { margin-top: 16px; }
</style>