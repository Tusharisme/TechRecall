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
      <!-- Heatmap -->
      <div class="bg-white rounded-lg shadow p-6 mb-8">
        <h2 class="text-lg font-medium text-gray-900 mb-4">Study Streak</h2>
        <div class="flex gap-1 overflow-x-auto pb-2">
            <!-- Simple last 30 days heatmap -->
            <div v-for="day in heatmapData" :key="day.date" class="flex flex-col items-center">
                <div 
                    class="w-3 h-3 rounded-sm" 
                    :class="getColor(day.count)"
                    :title="`${day.date}: ${day.count} reviews`"
                ></div>
            </div>
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
import { onMounted, ref, inject } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const decks = ref([])
const toast = inject('toast')
const heatmapData = ref([])

const generateHeatmap = async () => {
    try {
        const response = await api.get('/stats/heatmap')
        const dataMap = new Map(response.data.map(d => [d.date, d.count]))
        
        // Generate last 60 days with real data or 0
        const days = []
        for (let i = 59; i >= 0; i--) {
            const d = new Date()
            d.setDate(d.getDate() - i)
            const dateStr = d.toISOString().split('T')[0]
            days.push({
                date: dateStr,
                count: dataMap.get(dateStr) || 0
            })
        }
        heatmapData.value = days
    } catch (e) {
        console.error("Failed to load heatmap", e)
    }
}

const getColor = (count) => {
    if (count === 0) return 'bg-gray-200'
    if (count < 3) return 'bg-green-200'
    if (count < 6) return 'bg-green-400'
    return 'bg-green-600'
}

const fetchDecks = async () => {
    try {
        const response = await api.get('/decks')
        decks.value = response.data
    } catch (e) {
        toast.error('Failed to load decks')
        console.error(e)
    }
}

const createDeck = async () => {
  const title = prompt("Enter deck title:")
  if (title) {
    try {
       await api.post('/decks', { title })
       toast.success('Deck created!')
       fetchDecks()
    } catch (e) {
      toast.error("Failed to create deck")
    }
  }
}

onMounted(() => {
    fetchDecks()
    generateHeatmap()
})
</script>
