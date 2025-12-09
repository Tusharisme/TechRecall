<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full space-y-8 p-8 bg-white rounded-xl shadow-lg">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Create Account</h2>
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        
        <div>
            <label for="username" class="sr-only">Username</label>
            <input id="username" name="username" type="text" required class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm mb-2" placeholder="Username" v-model="username">
        </div>
        <div>
            <label for="email-address" class="sr-only">Email address</label>
            <input id="email-address" name="email" type="email" autocomplete="email" required class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm mb-2" placeholder="Email address" v-model="email">
        </div>
        <div>
            <label for="password" class="sr-only">Password</label>
            <input id="password" name="password" type="password" autocomplete="new-password" required class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm mb-2" placeholder="Password" v-model="password">
        </div>

        <div>
          <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
            Sign up
          </button>
        </div>
      </form>
       <div class="text-center">
        <router-link to="/login" class="text-sm text-blue-600 hover:text-blue-500">Already have an account? Sign in</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const username = ref('')
const password = ref('')
const authStore = useAuthStore()
const toast = inject('toast')

const handleRegister = async () => {
  try {
    await authStore.register(email.value, username.value, password.value)
    toast.success('Registration successful! Logging you in...')
  } catch (e) {
    toast.error('Registration failed. Username or Email might be taken.')
  }
}
</script>
