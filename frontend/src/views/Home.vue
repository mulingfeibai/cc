<template>
  <div class="page">
    <el-card class="panel" shadow="always">
      <h2 class="panel-title">开始模拟面试</h2>
      <p class="panel-subtitle">
        你好，{{ store.username }}！选择目标岗位与难度，开启你的面试之旅
      </p>

      <el-form label-position="top">
        <el-form-item label="岗位类型">
          <el-radio-group v-model="jobType" class="option-group">
            <el-radio-button v-for="j in jobTypes" :key="j" :value="j">
              {{ j }}
            </el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="难度">
          <el-radio-group v-model="difficulty" class="option-group">
            <el-radio-button v-for="d in difficulties" :key="d" :value="d">
              {{ d }}
            </el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-button
          type="primary"
          size="large"
          class="start-btn"
          :loading="loading"
          @click="handleStart"
        >
          开始面试
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { startInterview } from '@/api'
import { useUserStore } from '@/stores/user'

const store = useUserStore()
const router = useRouter()

const jobTypes = ['Java', '前端', '算法', '测试']
const difficulties = ['简单', '中等', '困难']

const jobType = ref('Java')
const difficulty = ref('中等')
const loading = ref(false)

async function handleStart() {
  loading.value = true
  try {
    const data = await startInterview({
      job_type: jobType.value,
      difficulty: difficulty.value,
    })
    router.push({
      path: `/interview/${data.session_id}`,
      query: { job_type: data.job_type, difficulty: data.difficulty },
    })
  } catch {
    // 错误提示已由 axios 拦截器统一处理
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.option-group {
  width: 100%;
}

.option-group :deep(.el-radio-button__inner) {
  min-width: 96px;
}

.start-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
  margin-top: 8px;
}
</style>
