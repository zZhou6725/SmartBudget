<template>
  <div class="expense">
    <PageCard>
      <template #title>费用报销管理</template>
      <template #extra>
        <el-button type="primary" @click="openCreateDialog">+ 新增报销申请</el-button>
      </template>

      <!-- 筛选栏 -->
      <el-form :model="query" inline class="expense__filter">
        <el-form-item label="关键字">
          <el-input v-model="query.keyword" placeholder="报销单号/标题" clearable />
        </el-form-item>
        <el-form-item label="报销类型">
          <el-select v-model="query.category" placeholder="全部" clearable>
            <el-option
              v-for="(label, value) in ExpenseCategoryMap"
              :key="value"
              :label="label"
              :value="value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="部门">
          <el-select v-model="query.deptName" placeholder="全部" clearable>
            <el-option
              v-for="dept in deptOptions"
              :key="dept"
              :label="dept"
              :value="dept"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="query.status" placeholder="全部" clearable>
            <el-option
              v-for="(label, value) in ExpenseStatusMap"
              :key="value"
              :label="label"
              :value="value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始"
            end-placeholder="结束"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 统计摘要 -->
      <el-row :gutter="16" class="expense__summary">
        <el-col :span="6">
          <div class="expense__summary-item">
            <span class="expense__summary-label">报销总额</span>
            <span class="expense__summary-value">
              {{ summary.totalAmount ? '¥' + summary.totalAmount.toLocaleString() : '--' }}
            </span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="expense__summary-item expense__summary-item--warning">
            <span class="expense__summary-label">待审批</span>
            <span class="expense__summary-value">{{ summary.pendingCount }} 笔</span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="expense__summary-item expense__summary-item--success">
            <span class="expense__summary-label">已通过</span>
            <span class="expense__summary-value">{{ summary.approvedCount }} 笔</span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="expense__summary-item expense__summary-item--danger">
            <span class="expense__summary-label">已驳回</span>
            <span class="expense__summary-value">{{ summary.rejectedCount }} 笔</span>
          </div>
        </el-col>
      </el-row>

      <!-- 数据表格 -->
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
        <el-table-column label="报销单号" prop="expenseNo" width="140" />
        <el-table-column label="标题" prop="title" min-width="160" />
        <el-table-column label="报销类型" width="100">
          <template #default="{ row }">
            {{ ExpenseCategoryMap[row.category] || row.category }}
          </template>
        </el-table-column>
        <el-table-column label="部门" prop="deptName" width="100" />
        <el-table-column label="金额" width="120">
          <template #default="{ row }">
            ¥{{ row.amount.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small">
              {{ ExpenseStatusMap[row.status] || row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="申请人" prop="applicant" width="90" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <div class="expense__actions">
              <el-button size="small" text type="primary" @click="openDetailDrawer(row)">
                详情
              </el-button>
              <el-button
                v-if="row.status === 'draft' || row.status === 'pending'"
                size="small"
                text
                type="primary"
                @click="openEditDialog(row)"
              >
                编辑
              </el-button>
              <el-popconfirm
                title="确认删除该报销记录？"
                @confirm="handleDelete(row.id)"
              >
                <template #reference>
                  <el-button size="small" text type="danger">删除</el-button>
                </template>
              </el-popconfirm>
            </div>
          </template>
        </el-table-column>
      </TableWrapper>
    </PageCard>

    <!-- 新增/编辑 Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑报销' : '新增报销申请'"
      width="620px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" label-width="90px">
        <el-form-item label="报销类型" required>
          <el-select v-model="form.category" placeholder="请选择">
            <el-option
              v-for="(label, value) in ExpenseCategoryMap"
              :key="value"
              :label="label"
              :value="value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="报销标题" required>
          <el-input v-model="form.title" placeholder="请输入报销标题" />
        </el-form-item>
        <el-form-item label="所属部门" required>
          <el-select v-model="form.deptName" placeholder="请选择">
            <el-option
              v-for="dept in deptOptions"
              :key="dept"
              :label="dept"
              :value="dept"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="关联预算">
          <el-select v-model="form.budgetId" placeholder="请选择关联预算（可选）" clearable>
            <el-option
              v-for="budget in budgetOptions"
              :key="budget.id"
              :label="`${budget.name}（余额 ¥${budget.remaining.toLocaleString()}）`"
              :value="budget.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="报销金额" required>
          <el-input-number
            v-model="form.amount"
            :min="0"
            :precision="2"
            placeholder="请输入金额"
          />
          <span class="expense__unit">元</span>
        </el-form-item>
        <el-form-item label="申请日期" required>
          <el-date-picker
            v-model="form.applyDate"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="附件上传">
          <el-button text type="primary">
            <el-icon><Paperclip /></el-icon> 选择文件
          </el-button>
          <span class="expense__attach-hint">（提交后可补充，非必填）</span>
        </el-form-item>
        <el-form-item label="备注说明">
          <el-input
            v-model="form.remark"
            type="textarea"
            :rows="3"
            placeholder="选填"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button @click="handleSave('draft')">保存草稿</el-button>
        <el-button type="primary" @click="handleSave('pending')">提交</el-button>
      </template>
    </el-dialog>

    <!-- 详情 Drawer -->
    <el-drawer
      v-model="drawerVisible"
      title="报销详情"
      size="480px"
    >
      <template v-if="detailItem">
        <div class="expense__detail-section">
          <span class="expense__detail-section-title">基本信息</span>
          <el-descriptions :column="2" border size="small">
            <el-descriptions-item label="报销单号">{{ detailItem.expenseNo }}</el-descriptions-item>
            <el-descriptions-item label="报销类型">
              {{ ExpenseCategoryMap[detailItem.category] }}
            </el-descriptions-item>
            <el-descriptions-item label="标题" :span="2">{{ detailItem.title }}</el-descriptions-item>
            <el-descriptions-item label="部门">{{ detailItem.deptName }}</el-descriptions-item>
            <el-descriptions-item label="金额">¥{{ detailItem.amount.toLocaleString() }}</el-descriptions-item>
            <el-descriptions-item label="申请人">{{ detailItem.applicant }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="statusTagType(detailItem.status)" size="small">
                {{ ExpenseStatusMap[detailItem.status] }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="关联预算">{{ detailItem.budgetName || '--' }}</el-descriptions-item>
            <el-descriptions-item label="申请日期">{{ detailItem.applyDate }}</el-descriptions-item>
            <el-descriptions-item label="备注" :span="2">{{ detailItem.remark || '--' }}</el-descriptions-item>
          </el-descriptions>
        </div>
        <div class="expense__detail-section">
          <span class="expense__detail-section-title">审批记录</span>
          <el-timeline>
            <el-timeline-item timestamp="提交时间" placement="top" type="primary">
              {{ detailItem.applicant }} 提交报销申请
            </el-timeline-item>
            <el-timeline-item timestamp="待处理" placement="top" color="#bbb">
              部门经理审批（待实现）
            </el-timeline-item>
            <el-timeline-item timestamp="待处理" placement="top" color="#bbb">
              财务审核（待实现）
            </el-timeline-item>
          </el-timeline>
        </div>
      </template>
      <EmptyHolder v-else text="暂无详情数据" />
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Paperclip } from '@element-plus/icons-vue'
import PageCard from '@/components/PageCard.vue'
import TableWrapper from '@/components/TableWrapper.vue'
import EmptyHolder from '@/components/EmptyHolder.vue'
import {
  ExpenseCategoryMap,
  ExpenseStatusMap,
  type ExpenseItem,
  type ExpenseForm,
  type ExpenseQuery,
  type ExpenseSummary,
} from '@/types/expense'
import {
  getExpenseList, getExpenseSummary, getExpenseDetail,
  createExpense, updateExpense, deleteExpense,
} from '@/api/modules/expense'

const query = ref<ExpenseQuery>({ keyword: '', page: 1, pageSize: 10 })
const dateRange = ref<string[]>([])

const summary = ref<ExpenseSummary>({ totalAmount: 0, pendingCount: 0, approvedCount: 0, rejectedCount: 0 })
const tableData = ref<ExpenseItem[]>([])
const pagination = reactive({ page: 1, pageSize: 10, total: 0 })

const deptOptions = ref<string[]>([])
const budgetOptions = ref<{ id: number; name: string; remaining: number }[]>([])

const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref<number | null>(null)
const formRef = ref()
const form = ref<ExpenseForm>({
  title: '', category: 'travel', deptName: '', budgetId: null,
  amount: null, applyDate: '', remark: '',
})

const drawerVisible = ref(false)
const detailItem = ref<ExpenseItem | null>(null)

async function fetchList() {
  try {
    const [startDate, endDate] = dateRange.value
    const q: Record<string, unknown> = {
      keyword: query.value.keyword || undefined,
      category: query.value.category || undefined,
      dept_name: query.value.deptName || undefined,
      status: query.value.status || undefined,
      page: query.value.page,
      page_size: query.value.pageSize,
    }
    if (startDate) q.start_date = startDate
    if (endDate) q.end_date = endDate
    const res = await getExpenseList(q as ExpenseQuery)
    if (res.code === 0) {
      tableData.value = res.data.items
      pagination.total = res.data.total
    }
  } catch { /* ignore */ }
}

async function fetchSummary() {
  try {
    const res = await getExpenseSummary()
    if (res.code === 0) summary.value = res.data
  } catch { /* ignore */ }
}

function handleQuery() {
  query.value.page = 1
  pagination.page = 1
  fetchList()
}

function handleReset() {
  query.value = { keyword: '', page: 1, pageSize: 10 }
  dateRange.value = []
  pagination.page = 1
  pagination.pageSize = 10
  fetchList()
}

function handlePageChange(page: number) {
  query.value.page = page
  pagination.page = page
  fetchList()
}

function handleSizeChange(size: number) {
  query.value.pageSize = size
  pagination.pageSize = size
  query.value.page = 1
  pagination.page = 1
  fetchList()
}

function openCreateDialog() {
  isEdit.value = false; editId.value = null
  form.value = { title: '', category: 'travel', deptName: '', budgetId: null, amount: null, applyDate: '', remark: '' }
  dialogVisible.value = true
}

function openEditDialog(row: ExpenseItem) {
  isEdit.value = true; editId.value = row.id
  form.value = { title: row.title, category: row.category, deptName: row.deptName, budgetId: row.budgetId, amount: row.amount, applyDate: row.applyDate, remark: row.remark }
  dialogVisible.value = true
}

async function handleSave(status: string) {
  try {
    const data = { ...form.value, status }
    let res
    if (isEdit.value && editId.value) {
      res = await updateExpense(editId.value, data as Record<string, unknown>)
    } else {
      res = await createExpense(data as Record<string, unknown>)
    }
    if (res.code === 0) {
      ElMessage.success(isEdit.value ? '编辑成功' : '新增成功')
      dialogVisible.value = false
      fetchList(); fetchSummary()
    } else {
      ElMessage.error(res.msg || '操作失败')
    }
  } catch { ElMessage.error('网络错误') }
}

async function openDetailDrawer(row: ExpenseItem) {
  try {
    const res = await getExpenseDetail(row.id)
    if (res.code === 0) detailItem.value = res.data
  } catch { detailItem.value = row }
  drawerVisible.value = true
}

async function handleDelete(id: number) {
  try {
    const res = await deleteExpense(id)
    if (res.code === 0) { ElMessage.success('删除成功'); fetchList(); fetchSummary() }
  } catch { ElMessage.error('网络错误') }
}

function statusTagType(status: string): string {
  const map: Record<string, string> = { draft: 'info', pending: 'warning', approved: 'success', rejected: 'danger' }
  return map[status] || 'info'
}

onMounted(() => { fetchList(); fetchSummary() })
</script>

<style scoped>
.expense__filter {
  margin-bottom: 16px;
}

.expense__summary {
  margin-bottom: 16px;
}

.expense__summary-item {
  background: var(--bg-page);
  border-radius: var(--border-radius-base);
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.expense__summary-label {
  font-size: 12px;
  color: var(--text-placeholder);
}

.expense__summary-value {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-title);
}

.expense__summary-item--warning .expense__summary-value { color: var(--color-warning); }
.expense__summary-item--success .expense__summary-value { color: var(--color-success); }
.expense__summary-item--danger .expense__summary-value { color: var(--color-danger); }

.expense__unit {
  margin-left: 8px;
  font-size: 13px;
  color: var(--text-placeholder);
}

.expense__attach-hint {
  margin-left: 8px;
  font-size: 12px;
  color: var(--text-placeholder);
}

.expense__detail-section {
  margin-bottom: 24px;
}

.expense__detail-section-title {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-title);
  margin-bottom: 12px;
  padding-left: 8px;
  border-left: 3px solid var(--color-primary);
}
.expense__actions {
  display: flex;
  align-items: center;
  white-space: nowrap;
}
</style>