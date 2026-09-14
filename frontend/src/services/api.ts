import axios, { AxiosInstance, AxiosError } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// ======================== Student APIs ========================
export const studentApi = {
  create: (data: any) => api.post('/api/students', data),
  getAll: (schoolId?: number, skip?: number, limit?: number) =>
    api.get('/api/students', { params: { school_id: schoolId, skip, limit } }),
  getById: (id: number) => api.get(`/api/students/${id}`),
  update: (id: number, data: any) => api.put(`/api/students/${id}`, data),
  delete: (id: number) => api.delete(`/api/students/${id}`),
}

// ======================== Attendance APIs ========================
export const attendanceApi = {
  add: (studentId: number, data: any) => api.post(`/api/attendance/${studentId}`, data),
  get: (studentId: number, days?: number) =>
    api.get(`/api/attendance/${studentId}`, { params: { days } }),
  getPercentage: (studentId: number, days?: number) =>
    api.get(`/api/attendance/percentage/${studentId}`, { params: { days } }),
}

// ======================== Grade APIs ========================
export const gradeApi = {
  add: (studentId: number, data: any) => api.post(`/api/grades/${studentId}`, data),
  get: (studentId: number, term?: string) =>
    api.get(`/api/grades/${studentId}`, { params: { term } }),
  getAverage: (studentId: number) => api.get(`/api/grades/average/${studentId}`),
}

// ======================== Health APIs ========================
export const healthApi = {
  add: (studentId: number, data: any) => api.post(`/api/health/${studentId}`, data),
  get: (studentId: number) => api.get(`/api/health/${studentId}`),
}

// ======================== Prediction APIs ========================
export const predictionApi = {
  predict: (studentId: number) => api.post('/api/predictions/predict', { student_id: studentId }),
  batchPredict: (schoolId?: number) =>
    api.post('/api/predictions/batch-predict', {}, { params: { school_id: schoolId } }),
  getHistory: (studentId: number) => api.get(`/api/predictions/${studentId}`),
}

// ======================== Dashboard APIs ========================
export const dashboardApi = {
  getStats: (schoolId?: number) => api.get('/api/dashboard/stats', { params: { school_id: schoolId } }),
  getRiskDistribution: (schoolId?: number) =>
    api.get('/api/dashboard/risk-distribution', { params: { school_id: schoolId } }),
  getStudentDetails: (studentId: number) =>
    api.get(`/api/dashboard/student-details/${studentId}`),
}

export default api
