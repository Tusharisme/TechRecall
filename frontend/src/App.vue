<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans">
    <router-view></router-view>
    <Toast ref="toastRef" />
  </div>
</template>

<script setup>
import { provide, ref } from 'vue'
import Toast from './components/Toast.vue'

const toastRef = ref(null)

provide('toast', {
    success: (msg) => toastRef.value?.show(msg, 'success'),
    error: (msg) => toastRef.value?.show(msg, 'error')
})
</script>
