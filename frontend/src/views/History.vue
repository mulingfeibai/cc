<template>
  <div class="page">
    <el-card class="panel" shadow="always">
      <template #header>
        <div class="header-row">
          <span class="card-title">面试历史</span>
          <el-button type="primary" size="small" @click="router.push('/')">
            开始新面试
          </el-button>
        </div>
      </template>

      <div v-loading="loading">
        <el-empty
          v-if="!loading && list.length === 0"
          description="暂无面试记录，快去开始第一场面试吧"
        />

        <el-table v-else :data="list" stripe>
          <el-table-column prop="id" label="编号" width="80" />
          <el-table-column prop="job_type" label="岗位类型" width="120" />
          <el-table-column prop="difficulty" label="难度" width="100" />
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === 'completed' ? 'success' : 'info'">
                {{ row.status === 'completed' ? '已完成' : '进行中' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="得分" width="100">
            <template #default="{ row }">
              <span v-if="row.score != null" class="score">{{ row.score }}</span>
              <span v-else class="muted">—</span>
            </template>
          </el-table-column>
          <el-table-column label="创建时间">
            <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-button type="primary" link @click="router.push(`/report/${row.id}`)">
                查看报告
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getHistory, type HistoryItem } from '@/api'

const router = useRouter()
const list = ref<HistoryItem[]>([])
const loading = ref(false)

function formatTime(iso: string) {
  if (!iso) return '—'
  const d = new Date(iso)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

async function loadHistory() {
  loading.value = true
  try {
    const data = await getHistory()
    list.value = data.sessions
  } catch {
    // 错误提示已由 axios 拦截器统一处理
  } finally {
    loading.value = false
  }
}

onMounted(loadHistory)
</script>

<style scoped>
.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.score {
  color: #409eff;
  font-weight: 600;
}

.muted {
  color: #c0c4cc;
}
</style>
