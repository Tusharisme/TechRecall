<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-4xl mx-auto bg-white rounded-lg shadow p-6">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-900">Edit Deck</h1>
        <button @click="router.push('/dashboard')" class="text-gray-600 hover:text-gray-900">Done</button>
      </div>

      <!-- Add Card Form -->
      <div class="bg-gray-50 p-4 rounded-lg mb-8 border">
        <h2 class="text-lg font-medium mb-4">Add New Card</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Front (Question)</label>
            <textarea v-model="newCard.front" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm h-20 p-2 border"></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Back (Answer)</label>
            <textarea v-model="newCard.back" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm h-20 p-2 border"></textarea>
          </div>
          <button @click="addCard" :disabled="!newCard.front || !newCard.back" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50">Add Card</button>
        </div>
      </div>

      <!-- Cards List -->
      <h2 class="text-lg font-medium mb-4">Cards ({{ cards.length }})</h2>
      <div class="space-y-4">
        <div v-for="card in cards" :key="card.id" class="border rounded-lg p-4 flex justify-between items-start bg-white">
          <div class="grid grid-cols-2 gap-4 flex-1">
            <div>
              <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Front</span>
              <p class="mt-1 text-gray-900">{{ card.front }}</p>
            </div>
            <div>
              <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Back</span>
              <p class="mt-1 text-gray-900">{{ card.back }}</p>
            </div>
          </div>
           <!-- Can add Delete button later -->
        </div>
        <div v-if="cards.length === 0" class="text-center text-gray-500 py-4">No cards yet.</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const toast = inject('toast')

const cards = ref([])
const newCard = ref({ front: '', back: '' })

const fetchCards = async () => {
  try {
    const response = await api.get(`/decks/${route.params.id}/cards`)
    cards.value = response.data
  } catch (e) {
    toast.error('Failed to load cards')
    console.error(e)
  }
}

const addCard = async () => {
  try {
    await api.post(`/decks/${route.params.id}/cards`, {
        front: newCard.value.front,
        back: newCard.value.back
    })
    newCard.value = { front: '', back: '' }
    toast.success('Card added!')
    fetchCards()
  } catch (e) {
    toast.error("Failed to add card")
  }
}

onMounted(() => {
  fetchCards()
})
</script>
