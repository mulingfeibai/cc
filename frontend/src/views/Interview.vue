<template>
  <div class="page">
    <el-card class="panel" shadow="always">
      <div class="interview-header">
        <div>
          <h2 class="panel-title">模拟面试进行中</h2>
          <p class="panel-subtitle">
            岗位：{{ jobType }} · 难度：{{ difficulty }}
          </p>
        </div>
        <el-tag type="info">已答 {{ answeredCount }} / 5 题</el-tag>
      </div>

      <el-progress
        :percentage="progress"
        :stroke-width="10"
        :color="progressColor"
        class="progress"
      />

      <!-- 已完成（刷新后进入的兜底状态） -->
      <div v-if="completed" class="completed-block">
        <el-result
          icon="success"
          title="面试已完成"
          sub-title="你已完成全部题目，快去看看评估报告吧"
        >
          <template #extra>
            <el-button type="primary" @click="goReport">查看面试报告</el-button>
          </template>
        </el-result>
      </div>

      <template v-else>
        <!-- 题目 -->
        <div v-loading="loading" class="question-block">
          <h3 class="question-title">题目</h3>
          <p class="question-text">{{ question?.question }}</p>
        </div>

        <!-- 回答输入 -->
        <el-input
          v-model="answer"
          type="textarea"
          :rows="6"
          placeholder="请在这里输入你的回答..."
          class="answer-input"
          :disabled="!!result"
        />

        <el-button
          v-if="!result"
          type="primary"
          size="large"
          class="submit-btn"
          :loading="submitting"
          :disabled="!answer.trim()"
          @click="handleSubmit"
        >
          提交回答
        </el-button>

        <!-- 评估结果 -->
        <div v-if="result" class="result-block">
          <el-divider content-position="left">AI 评估结果</el-divider>

          <div class="score-row">
            <span class="score-label">得分</span>
            <span class="score-value">{{ result.score }}</span>
            <span class="score-unit">分</span>
          </div>

          <el-alert type="success" :closable="false" class="eval-alert">
            <p class="evaluation-text">{{ result.evaluation }}</p>
          </el-alert>

          <el-button
            type="primary"
            size="large"
            class="submit-btn"
            @click="nextQuestion"
          >
            {{ answeredCount >= 5 ? '查看面试报告' : '下一题' }}
          </el-button>
        </div>
      </template>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  getQuestion,
  submitAnswer,
  type AnswerResult,
  type QuestionResult,
} from '@/api'

const route = useRoute()
const router = useRouter()

const sessionId = Number(route.params.id)
const jobType = (route.query.job_type as string) || '—'
const difficulty = (route.query.difficulty as string) || '—'

const question = ref<QuestionResult | null>(null)
const answer = ref('')
const result = ref<AnswerResult | null>(null)
const loading = ref(false)
const submitting = ref(false)
const answeredCount = ref(0)
const completed = ref(false)

const progress = computed(() => Math.round((answeredCount.value / 5) * 100))

const progressColor = computed(() => {
  if (progress.value >= 100) return '#67c23a'
  if (progress.value >= 60) return '#409eff'
  return '#e6a23c'
})

async function fetchQuestion() {
  loading.value = true
  try {
    question.value = await getQuestion(sessionId)
    answer.value = ''
    result.value = null
  } catch (e) {
    // 400 表示面试已完成（刷新后进入已完成会话的场景）
    if ((e as { response?: { status?: number } }).response?.status === 400) {
      completed.value = true
    }
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  if (!question.value || !answer.value.trim()) return
  submitting.value = true
  try {
    result.value = await submitAnswer(sessionId, {
      question_id: question.value.id,
      answer: answer.value.trim(),
    })
    answeredCount.value += 1
  } catch {
    // 错误提示已由 axios 拦截器统一处理
  } finally {
    submitting.value = false
  }
}

function nextQuestion() {
  if (answeredCount.value >= 5) {
    goReport()
    return
  }
  fetchQuestion()
}

function goReport() {
  router.push(`/report/${sessionId}`)
}

onMounted(fetchQuestion)
</script>

<style scoped>
.interview-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.progress {
  margin-bottom: 20px;
}

.question-block {
  min-height: 120px;
  margin-bottom: 16px;
}

.question-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.question-text {
  font-size: 16px;
  line-height: 1.7;
  color: #303133;
  white-space: pre-wrap;
}

.answer-input {
  margin-bottom: 16px;
}

.submit-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
}

.result-block {
  margin-top: 8px;
}

.score-row {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 12px;
}

.score-label {
  color: #606266;
  font-size: 14px;
}

.score-value {
  font-size: 40px;
  font-weight: 700;
  color: #409eff;
}

.score-unit {
  color: #909399;
  font-size: 14px;
}

.eval-alert {
  margin-bottom: 16px;
}

.evaluation-text {
  line-height: 1.7;
  white-space: pre-wrap;
}

.completed-block {
  padding: 20px 0;
}
</style>
