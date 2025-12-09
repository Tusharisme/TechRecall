import { defineStore } from 'pinia'
import axios from 'axios'
import router from '../router'



const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(email, password) {
      try {
        const response = await axios.post(`${BASE_URL}/login?include_auth_token`, {
          email,
          password
        }, {
          headers: { 'Content-Type': 'application/json' }
        })
        
        // Flask-Security returns response.user and response.response.user.authentication_token usually
        // But with standard config it might be different. 
        // Let's assume standard FS JSON response for now.
        const token = response.data.response.user.authentication_token
        this.token = token
        this.user = response.data.response.user
        
        localStorage.setItem('token', token)
        axios.defaults.headers.common['Authentication-Token'] = token
        
        router.push('/dashboard')
      } catch (error) {
        console.error('Login failed', error)
        throw error
      }
    },
    async register(email, username, password) {
       try {
        await axios.post(`${BASE_URL}/register`, {
          email,
          password,
          username,  // Custom field
          active: true // Backend might need this if confirm disabled
        }, {
           headers: { 'Content-Type': 'application/json' }
        })
        // Auto login or redirect?
        await this.login(email, password)
      } catch (error) {
        console.error('Registration failed', error)
        throw error
      }
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authentication-Token']
      router.push('/login')
    }
  }
})
