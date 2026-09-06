<template>
  <header class="navbar">
    <div class="navbar-inner">
      <div class="brand" @click="router.push('/')">
        <el-icon :size="22" color="#409eff"><ChatDotRound /></el-icon>
        <span class="brand-name">AI面试系统</span>
      </div>

      <nav class="nav-links">
        <router-link to="/" class="nav-link">开始面试</router-link>
        <router-link to="/history" class="nav-link">面试历史</router-link>
      </nav>

      <div class="nav-user">
        <span class="username">{{ store.username }}</span>
        <el-button size="small" plain @click="handleLogout">退出登录</el-button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ChatDotRound } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const store = useUserStore()
const router = useRouter()

function handleLogout() {
  store.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.navbar-inner {
  max-width: 1000px;
  margin: 0 auto;
  height: 60px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  gap: 32px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.brand-name {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.nav-links {
  display: flex;
  gap: 8px;
  flex: 1;
}

.nav-link {
  padding: 6px 14px;
  border-radius: 6px;
  color: #606266;
  text-decoration: none;
  font-size: 15px;
  transition: all 0.2s;
}

.nav-link:hover {
  color: #409eff;
  background: #ecf5ff;
}

.nav-link.router-link-active {
  color: #409eff;
  font-weight: 600;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  color: #606266;
  font-size: 14px;
}
</style>
