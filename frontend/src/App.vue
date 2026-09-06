<template>
  <div class="app">
    <NavBar v-if="showNav" />
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

const route = useRoute()
const showNav = computed(() => route.meta.requiresAuth === true)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body,
#app {
  height: 100%;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', Arial, sans-serif;
  color: #303133;
  background: linear-gradient(135deg, #eef2ff 0%, #f7f0fb 50%, #fef7ec 100%);
  background-attachment: fixed;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-main {
  flex: 1;
  width: 100%;
}

/* 页面通用布局 */
.page {
  max-width: 900px;
  margin: 24px auto 48px;
  padding: 0 16px;
}

.panel {
  border-radius: 12px;
  margin-bottom: 16px;
}

.panel-title {
  font-size: 20px;
  color: #303133;
  margin-bottom: 8px;
}

.panel-subtitle {
  color: #909399;
  font-size: 14px;
  margin-bottom: 16px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}
</style>
