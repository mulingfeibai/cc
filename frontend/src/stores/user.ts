import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { login as loginApi, register as registerApi, type TokenData } from '@/api'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const username = ref<string>(localStorage.getItem('username') || '')
  const userId = ref<number>(Number(localStorage.getItem('user_id')) || 0)

  const isLoggedIn = computed(() => !!token.value)

  function setAuth(data: TokenData) {
    token.value = data.token
    username.value = data.username
    userId.value = data.user_id
    localStorage.setItem('token', data.token)
    localStorage.setItem('username', data.username)
    localStorage.setItem('user_id', String(data.user_id))
  }

  function clearAuth() {
    token.value = ''
    username.value = ''
    userId.value = 0
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('user_id')
  }

  async function login(payload: { username: string; password: string }) {
    const data = await loginApi(payload)
    setAuth(data)
  }

  async function register(payload: { username: string; password: string }) {
    const data = await registerApi(payload)
    setAuth(data)
  }

  function logout() {
    clearAuth()
  }

  return { token, username, userId, isLoggedIn, login, register, logout }
})
