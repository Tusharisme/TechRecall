import axios from 'axios'
import { useAuthStore } from './stores/auth'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add token
api.interceptors.request.use(config => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers['Authentication-Token'] = authStore.token
  }
  return config
}, error => {
  return Promise.reject(error)
})

export default api
