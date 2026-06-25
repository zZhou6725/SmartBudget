<template>
  <div class="org">
    <PageCard>
      <template #title>组织权限管理</template>
      <template #extra>
        <el-button v-if="activeTab === 'dept'" type="primary" @click="openDeptDialog()">+ 新增部门</el-button>
        <el-button v-else type="primary" @click="openUserDialog()">+ 新增用户</el-button>
      </template>

      <el-tabs v-model="activeTab">
        <!-- 部门管理 -->
        <el-tab-pane label="部门管理" name="dept">
          <TableWrapper :data="deptList" :empty="deptList.length === 0">
            <el-table-column label="部门名称" prop="name" width="160" />
            <el-table-column label="负责人" prop="manager" width="120" />
            <el-table-column label="人数" prop="memberCount" width="80" />
            <el-table-column label="预算总额" width="140">
              <template #default="{ row }">¥{{ row.totalBudget.toLocaleString() }}</template>
            </el-table-column>
            <el-table-column label="操作" width="180">
              <template #default="{ row }">
                <el-button size="small" text type="primary" @click="openDeptDialog(row)">编辑</el-button>
                <el-popconfirm title="确认删除？" @confirm="handleDeleteDept(row.id)">
                  <template #reference>
                    <el-button size="small" text type="danger">删除</el-button>
                  </template>
                </el-popconfirm>
              </template>
            </el-table-column>
          </TableWrapper>
        </el-tab-pane>

        <!-- 用户管理 -->
        <el-tab-pane label="用户管理" name="user">
          <TableWrapper :data="userList" :empty="userList.length === 0" :show-pagination="true" :total="userTotal" :current-page="userPage" :page-size="userPageSize" @page-change="handleUserPageChange" @size-change="handleUserSizeChange">
            <el-table-column label="用户名" prop="username" width="120" />
            <el-table-column label="姓名" prop="realName" width="100" />
            <el-table-column label="部门" prop="deptName" width="120" />
            <el-table-column label="角色" width="100">
              <template #default="{ row }">{{ RoleMap[row.role] || row.role }}</template>
            </el-table-column>
            <el-table-column label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.status === 'active' ? 'success' : 'info'" size="small">{{ row.status === 'active' ? '正常' : '禁用' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="220">
              <template #default="{ row }">
                <el-button size="small" text type="primary" @click="openUserDialog(row)">编辑</el-button>
                <el-button size="small" text type="warning" @click="openRoleDialog(row)">角色</el-button>
                <el-popconfirm title="确认删除？" @confirm="handleDeleteUser(row.id)">
                  <template #reference>
                    <el-button size="small" text type="danger">删除</el-button>
                  </template>
                </el-popconfirm>
              </template>
            </el-table-column>
          </TableWrapper>
        </el-tab-pane>
      </el-tabs>
    </PageCard>

    <!-- 部门 Dialog -->
    <el-dialog v-model="deptDialogVisible" :title="deptIsEdit ? '编辑部门' : '新增部门'" width="420px">
      <el-form :model="deptForm" label-width="80px">
        <el-form-item label="部门名称" required><el-input v-model="deptForm.name" /></el-form-item>
        <el-form-item label="负责人"><el-input v-model="deptForm.manager" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="deptDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveDept">保存</el-button>
      </template>
    </el-dialog>

    <!-- 用户 Dialog -->
    <el-dialog v-model="userDialogVisible" :title="userIsEdit ? '编辑用户' : '新增用户'" width="420px">
      <el-form :model="userForm" label-width="80px">
        <el-form-item label="用户名" required><el-input v-model="userForm.username" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="userForm.realName" /></el-form-item>
        <el-form-item label="部门"><el-select v-model="userForm.deptId" placeholder="请选择"><el-option v-for="d in deptList" :key="d.id" :label="d.name" :value="d.id" /></el-select></el-form-item>
        <el-form-item label="角色"><el-select v-model="userForm.role"><el-option v-for="(label, value) in RoleMap" :key="value" :label="label" :value="value" /></el-select></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="userDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveUser">保存</el-button>
      </template>
    </el-dialog>

    <!-- 分配角色 Dialog -->
    <el-dialog v-model="roleDialogVisible" title="分配角色" width="350px">
      <el-form label-width="80px">
        <el-form-item label="角色">
          <el-select v-model="assignRoleValue">
            <el-option v-for="(label, value) in RoleMap" :key="value" :label="label" :value="value" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAssignRole">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import PageCard from '@/components/PageCard.vue'
import TableWrapper from '@/components/TableWrapper.vue'
import { RoleMap, type DeptItem, type DeptForm, type UserItem, type UserForm } from '@/types/organization'
import { getDeptList, createDept, updateDept, deleteDept, getUserList, createUser, updateUser, deleteUser } from '@/api/modules/organization'

const activeTab = ref('dept')

const deptList = ref<DeptItem[]>([])
const deptDialogVisible = ref(false)
const deptIsEdit = ref(false)
const deptEditId = ref<number | null>(null)
const deptForm = ref<DeptForm>({ name: '', manager: '' })

const userList = ref<UserItem[]>([])
const userTotal = ref(0)
const userPage = ref(1)
const userPageSize = ref(10)
const userDialogVisible = ref(false)
const userIsEdit = ref(false)
const userEditId = ref<number | null>(null)
const userForm = ref<UserForm>({ username: '', realName: '', deptId: null, role: 'viewer' })

const roleDialogVisible = ref(false)
const assignRoleValue = ref('viewer')
const assignUserId = ref<number | null>(null)

function fetchDeptList() {
  getDeptList().then(res => { if (res.code === 0) deptList.value = res.data as DeptItem[] }).catch(() => {})
}
function fetchUserList() {
  getUserList({ page: userPage.value, page_size: userPageSize.value }).then(res => {
    if (res.code === 0) { userList.value = res.data.items; userTotal.value = res.data.total }
  }).catch(() => {})
}
function handleUserPageChange(p: number) { userPage.value = p }
function handleUserSizeChange(s: number) { userPageSize.value = s; userPage.value = 1 }

watch(activeTab, (tab) => { if (tab === 'dept') fetchDeptList(); else { userPage.value = 1; fetchUserList() } })
watch([userPage, userPageSize], () => { if (activeTab.value === 'user') fetchUserList() })

function openDeptDialog(row?: DeptItem) {
  deptIsEdit.value = !!row
  deptEditId.value = row?.id ?? null
  deptForm.value = row ? { name: row.name, manager: row.manager } : { name: '', manager: '' }
  deptDialogVisible.value = true
}
async function handleSaveDept() {
  try {
    let res
    if (deptIsEdit.value && deptEditId.value) {
      res = await updateDept(deptEditId.value, deptForm.value)
    } else {
      res = await createDept(deptForm.value)
    }
    if (res.code === 0) { ElMessage.success(deptIsEdit.value ? '编辑成功' : '新增成功'); deptDialogVisible.value = false; fetchDeptList() }
    else { ElMessage.error(res.msg || '操作失败') }
  } catch { ElMessage.error('网络错误') }
}
async function handleDeleteDept(id: number) {
  try {
    const res = await deleteDept(id)
    if (res.code === 0) { ElMessage.success('删除成功'); fetchDeptList() }
  } catch { ElMessage.error('网络错误') }
}

function openUserDialog(row?: UserItem) {
  userIsEdit.value = !!row
  userEditId.value = row?.id ?? null
  userForm.value = row
    ? { username: row.username, realName: row.realName, deptId: null, role: row.role }
    : { username: '', realName: '', deptId: null, role: 'viewer' }
  userDialogVisible.value = true
}
async function handleSaveUser() {
  try {
    let res
    if (userIsEdit.value && userEditId.value) {
      res = await updateUser(userEditId.value, userForm.value as Record<string, unknown>)
    } else {
      res = await createUser(userForm.value)
    }
    if (res.code === 0) { ElMessage.success(userIsEdit.value ? '编辑成功' : '新增成功'); userDialogVisible.value = false; fetchUserList() }
    else { ElMessage.error(res.msg || '操作失败') }
  } catch { ElMessage.error('网络错误') }
}
async function handleDeleteUser(id: number) {
  try {
    const res = await deleteUser(id)
    if (res.code === 0) { ElMessage.success('删除成功'); fetchUserList() }
  } catch { ElMessage.error('网络错误') }
}
function openRoleDialog(row: UserItem) { assignUserId.value = row.id; assignRoleValue.value = row.role; roleDialogVisible.value = true }
async function handleAssignRole() {
  if (!assignUserId.value) return
  try {
    const res = await updateUser(assignUserId.value, { role: assignRoleValue.value } as Record<string, unknown>)
    if (res.code === 0) { ElMessage.success('角色分配成功'); roleDialogVisible.value = false; fetchUserList() }
    else { ElMessage.error(res.msg || '操作失败') }
  } catch { ElMessage.error('网络错误') }
}

onMounted(() => { fetchDeptList() })
</script>