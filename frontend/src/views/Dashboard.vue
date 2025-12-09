<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-bold text-blue-600">TechRecall</h1>
          </div>
          <div class="flex items-center">
            <span class="mr-4 text-gray-700">Hello, {{ authStore.user?.username }}</span>
            <button @click="authStore.logout()" class="text-red-600 hover:text-red-800 font-medium">Logout</button>
          </div>
        </div>
      </div>
    </nav>
    
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Heatmap Placeholder -->
      <div class="mb-8 bg-white p-6 rounded-lg shadow-sm">
        <h2 class="text-lg font-medium text-gray-900 mb-4">Study Connectivity</h2>
         <div class="h-32 bg-gray-100 flex items-center justify-center rounded border border-dashed border-gray-300">
           <span class="text-gray-500">Heatmap visualization coming soon</span>
         </div>
      </div>

      <!-- Decks -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-900">Your Decks</h2>
        <button @click="createDeck" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 shadow-sm">+ New Deck</button>
      </div>
      
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div v-for="deck in decks" :key="deck.id" class="bg-white overflow-hidden shadow rounded-lg border hover:border-blue-500 transition cursor-pointer">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center justify-between mb-2">
                <h3 class="text-lg leading-6 font-medium text-gray-900">{{ deck.title }}</h3>
                <span class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded text-blue-600 bg-blue-200 last:mr-0 mr-1">{{ deck.card_count }} cards</span>
            </div>
            <p class="text-sm text-gray-500 truncate mb-4">{{ deck.description || 'No description' }}</p>
            <div class="flex justify-between space-x-2">
               <button @click="router.push(`/study/${deck.id}`)" class="flex-1 bg-green-50 text-green-700 hover:bg-green-100 px-3 py-2 rounded text-sm font-medium">Study Now</button>
               <button @click="router.push(`/decks/${deck.id}`)" class="flex-1 bg-gray-50 text-gray-700 hover:bg-gray-100 px-3 py-2 rounded text-sm font-medium">Edit</button>
            </div>
          </div>
        </div>
        
        <!-- Empty State -->
        <div v-if="decks.length === 0" class="col-span-full text-center py-12 bg-white rounded-lg border border-dashed border-gray-300">
          <p class="text-gray-500">No decks yet. Create one to get started!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const decks = ref([])

const fetchDecks = async () => {
    try {
        const response = await api.get('/decks')
        decks.value = response.data
    } catch (e) {
        console.error(e)
    }
}

const createDeck = async () => {
  const title = prompt("Enter deck title:")
  if (title) {
    try {
       await api.post('/decks', { title })
       fetchDecks()
    } catch (e) {
      alert("Failed to create deck")
    }
  }
}

onMounted(() => {
    fetchDecks()
})
</script>
