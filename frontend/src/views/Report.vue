<template>
  <div class="page">
    <div v-loading="loading">
      <template v-if="report">
        <!-- 综合得分 -->
        <el-card class="panel summary-card" shadow="always">
          <div class="summary">
            <div class="summary-main">
              <p class="summary-label">综合得分</p>
              <p class="summary-score">
                {{ report.total_score ?? '—' }}
                <span v-if="report.total_score != null" class="unit">分</span>
              </p>
            </div>
            <div class="summary-meta">
              <el-tag size="large">{{ report.job_type }}</el-tag>
              <el-tag size="large" type="warning">{{ report.difficulty }}</el-tag>
              <el-tag
                size="large"
                :type="report.status === 'completed' ? 'success' : 'info'"
              >
                {{ report.status === 'completed' ? '已完成' : '进行中' }}
              </el-tag>
            </div>
          </div>
        </el-card>

        <!-- 逐题评估 -->
        <el-card class="panel" shadow="always">
          <template #header>
            <span class="card-title">逐题评估</span>
          </template>

          <div v-if="report.questions.length === 0" class="empty-tip">
            暂无已作答的题目。
          </div>

          <div
            v-for="(q, i) in report.questions"
            :key="q.id"
            class="question-item"
          >
            <div class="question-head">
              <span class="question-index">{{ i + 1 }}</span>
              <span class="question-text">{{ q.question }}</span>
              <el-tag :type="scoreTag(q.score)">{{ q.score }} 分</el-tag>
            </div>
            <p class="answer-text">
              <strong>我的回答：</strong>{{ q.answer || '（未回答）' }}
            </p>
            <el-alert type="info" :closable="false" class="eval-alert">
              <p class="evaluation-text">{{ q.evaluation || '暂无评估' }}</p>
            </el-alert>
          </div>
        </el-card>

        <!-- 改进建议 -->
        <el-card class="panel" shadow="always">
          <template #header>
            <span class="card-title">改进建议</span>
          </template>
          <ul class="suggestions">
            <li v-for="(s, i) in suggestions" :key="i">{{ s }}</li>
          </ul>
        </el-card>

        <div class="actions">
          <el-button @click="router.push('/')">返回首页</el-button>
          <el-button type="primary" @click="router.push('/history')">
            查看历史记录
          </el-button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getReport, type ReportResult } from '@/api'

const route = useRoute()
const router = useRouter()

const sessionId = Number(route.params.id)
const report = ref<ReportResult | null>(null)
const loading = ref(false)

function scoreTag(score: number) {
  if (score >= 85) return 'success'
  if (score >= 70) return 'warning'
  return 'danger'
}

const suggestions = computed(() => {
  const list: string[] = []
  const total = report.value?.total_score

  if (total != null) {
    if (total >= 85) {
      list.push('整体表现优秀，回答结构清晰、要点完整，继续保持并挑战更高难度。')
    } else if (total >= 70) {
      list.push('整体表现良好，建议针对失分题目查漏补缺，提升回答的条理性与深度。')
    } else {
      list.push('整体还有较大提升空间，建议系统梳理相关知识点，多做模拟练习。')
    }
  }

  report.value?.questions.forEach((q, i) => {
    if (q.score < 70) {
      list.push(`第 ${i + 1} 题得分偏低（${q.score} 分），建议围绕该知识点深入学习并加强表达。`)
    }
  })

  if (list.length === 0) {
    list.push('暂无具体改进建议，请继续完成更多面试以获取更全面的评估。')
  }
  return list
})

async function loadReport() {
  loading.value = true
  try {
    report.value = await getReport(sessionId)
  } catch {
    // 错误提示已由 axios 拦截器统一处理
  } finally {
    loading.value = false
  }
}

onMounted(loadReport)
</script>

<style scoped>
.summary-card {
  padding: 8px 0;
}

.summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.summary-label {
  color: #909399;
  font-size: 14px;
}

.summary-score {
  font-size: 48px;
  font-weight: 700;
  color: #409eff;
  line-height: 1.2;
}

.summary-score .unit {
  font-size: 16px;
  font-weight: 400;
  color: #909399;
  margin-left: 4px;
}

.summary-meta {
  display: flex;
  gap: 8px;
}

.question-item {
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.question-item:last-child {
  border-bottom: none;
}

.question-head {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 10px;
}

.question-index {
  flex-shrink: 0;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #409eff;
  color: #fff;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.question-text {
  flex: 1;
  font-size: 15px;
  line-height: 1.6;
  color: #303133;
}

.answer-text {
  color: #606266;
  font-size: 14px;
  line-height: 1.7;
  margin-bottom: 10px;
  white-space: pre-wrap;
}

.eval-alert {
  border-radius: 8px;
}

.evaluation-text {
  line-height: 1.7;
  white-space: pre-wrap;
}

.empty-tip {
  color: #909399;
  text-align: center;
  padding: 24px 0;
}

.suggestions {
  padding-left: 20px;
}

.suggestions li {
  line-height: 2;
  color: #606266;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 8px;
}
</style>
