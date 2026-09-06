import axios from 'axios'
import { ElMessage } from 'element-plus'

// ---------- 类型定义 ----------

export interface LoginParams {
  username: string
  password: string
}

export interface TokenData {
  token: string
  username: string
  user_id: number
}

export interface InterviewStartParams {
  job_type: string
  difficulty: string
}

export interface InterviewStartResult {
  session_id: number
  job_type: string
  difficulty: string
  status: string
}

export interface QuestionResult {
  id: number
  question: string
}

export interface AnswerParams {
  question_id: number
  answer: string
}

export interface AnswerResult {
  question_id: number
  score: number
  evaluation: string
}

export interface ReportItem {
  id: number
  question: string
  answer: string
  evaluation: string
  score: number
}

export interface ReportResult {
  session_id: number
  job_type: string
  difficulty: string
  status: string
  total_score: number | null
  questions: ReportItem[]
}

export interface HistoryItem {
  id: number
  job_type: string
  difficulty: string
  status: string
  score: number | null
  created_at: string
}

export interface HistoryResult {
  sessions: HistoryItem[]
}

// ---------- axios 实例 ----------

const service = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

// 请求拦截器：自动携带 token
service.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器：统一错误提示与 401 处理
service.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status
    let message = '请求失败，请稍后重试'
    const detail = error.response?.data?.detail

    if (typeof detail === 'string') {
      message = detail
    } else if (Array.isArray(detail)) {
      message = detail.map((d: { msg?: string }) => d.msg || '').join('；')
    }

    ElMessage.error(message)

    if (status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('user_id')
      const path = window.location.pathname
      if (path !== '/login' && path !== '/register') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

// ---------- 请求封装 ----------

const get = <T>(url: string): Promise<T> =>
  service.get<T>(url).then((res) => res.data)

const post = <T>(url: string, data?: unknown): Promise<T> =>
  service.post<T>(url, data).then((res) => res.data)

// ---------- 认证接口 ----------

export const login = (data: LoginParams) => post<TokenData>('/auth/login', data)

export const register = (data: LoginParams) =>
  post<TokenData>('/auth/register', data)

// ---------- 面试接口 ----------

export const startInterview = (data: InterviewStartParams) =>
  post<InterviewStartResult>('/interview/start', data)

export const getQuestion = (sessionId: number) =>
  get<QuestionResult>(`/interview/${sessionId}/question`)

export const submitAnswer = (sessionId: number, data: AnswerParams) =>
  post<AnswerResult>(`/interview/${sessionId}/answer`, data)

export const getReport = (sessionId: number) =>
  get<ReportResult>(`/interview/${sessionId}/report`)

export const getHistory = () => get<HistoryResult>('/interview/history')
