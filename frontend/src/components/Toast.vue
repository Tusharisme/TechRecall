<template>
  <div v-if="visible" class="fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg text-white transition-all transform z-50"
       :class="type === 'error' ? 'bg-red-600' : 'bg-green-600'">
    <div class="flex items-center space-x-2">
        <span>{{ message }}</span>
        <button @click="hide" class="ml-4 font-bold">&times;</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const visible = ref(false)
const message = ref('')
const type = ref('success')

const show = (msg, t = 'success') => {
  message.value = msg
  type.value = t
  visible.value = true
  setTimeout(() => {
    visible.value = false
  }, 3000)
}

const hide = () => visible.value = false

defineExpose({ show })
</script>
