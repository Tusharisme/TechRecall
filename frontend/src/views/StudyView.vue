<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center p-4">
    <!-- Header -->
    <div class="w-full max-w-lg flex justify-between items-center mb-6">
      <button @click="router.back()" class="text-gray-600 hover:text-gray-900">
         &larr; Back
      </button>
      <h1 class="text-xl font-bold text-gray-800">Study Session</h1>
      <div class="w-10"></div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center mt-20">
      <p class="text-gray-500">Loading cards...</p>
    </div>

    <!-- No Cards State -->
    <div v-else-if="cards.length === 0" class="text-center mt-20 p-8 bg-white rounded-xl shadow-sm">
      <h2 class="text-2xl font-bold text-green-600 mb-2">All Caught Up!</h2>
      <p class="text-gray-600">You have no due cards for this deck right now.</p>
      <button @click="router.push('/dashboard')" class="mt-6 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">Back to Dashboard</button>
    </div>

    <!-- Card Interface -->
    <div v-else class="w-full max-w-lg perspective-1000 relative h-96">
      <div 
        class="card-container w-full h-full relative cursor-pointer transition-transform duration-500 transform-style-3d"
        :class="{ 'rotate-y-180': isFlipped }"
        @click="isFlipped = !isFlipped"
      >
        <!-- Front -->
        <div class="absolute w-full h-full bg-white rounded-xl shadow-xl p-8 flex items-center justify-center backface-hidden z-10">
          <p class="text-2xl font-medium text-center text-gray-800">{{ currentCard.front }}</p>
          <p class="absolute bottom-4 text-xs text-gray-400 uppercase tracking-wide">Tap to flip</p>
        </div>

        <!-- Back -->
        <div class="absolute w-full h-full bg-blue-50 rounded-xl shadow-xl p-8 flex items-center justify-center backface-hidden rotate-y-180">
          <p class="text-xl text-center text-gray-800">{{ currentCard.back }}</p>
        </div>
      </div>
    </div>

    <!-- Controls -->
    <div v-if="!loading && cards.length > 0 && isFlipped" class="w-full max-w-lg mt-8 grid grid-cols-4 gap-4">
       <button @click="rateCard(1)" class="py-3 rounded-lg bg-red-100 text-red-700 font-medium hover:bg-red-200">Again</button>
       <button @click="rateCard(3)" class="py-3 rounded-lg bg-yellow-100 text-yellow-700 font-medium hover:bg-yellow-200">Hard</button>
       <button @click="rateCard(4)" class="py-3 rounded-lg bg-green-100 text-green-700 font-medium hover:bg-green-200">Good</button>
       <button @click="rateCard(5)" class="py-3 rounded-lg bg-blue-100 text-blue-700 font-medium hover:bg-blue-200">Easy</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const cards = ref([])
const currentIndex = ref(0)
const isFlipped = ref(false)

const currentCard = computed(() => {
  if (currentIndex.value < cards.value.length) {
    return cards.value[currentIndex.value]
  }
  return null
})

const fetchCards = async () => {
  try {
    // Actually we implemented /cards/due globally, but getting cards for specific deck
    // requires logic update or filter. For now let's use global due endpoint and filter client side
    // OR endpoints for deck cards. 
    // Wait, the Algorithm runs on /cards/due endpoint which returns all due cards.
    // If the user clicked "Study" on a specific deck, we should filter by deck_id.
    
    // Let's implement /decks/:id/cards (GET) to get ALL cards, but for Study Mode we want DUE cards.
    // I will use /cards/due and filter by deck if needed.
    // Ideally backend accepts ?deck_id param. But I didn't verify that.
    // Let's fetch all due cards and filter client side for now.
    
    const response = await axios.get('http://localhost:5000/api/cards/due', {
      headers: { 'Authentication-Token': authStore.token }
    })
    
    // Filter by deckId from route
    const deckId = parseInt(route.params.id)
    // The DUE endpoint returns: id, front, back, deck_title. It doesn't return deck_id.
    // I need to update GET /cards/due to return deck_id.
    // Or I can just fetch ALL cards for the deck and filter those where next_review <= now.
    // Re-fetching deck cards is easier given current API limitations.
    // Wait, get_cards endpoint returns 'next_review'. I can use that!
    
    const deckCardsResponse = await axios.get(`http://localhost:5000/api/decks/${deckId}/cards`)
    const now = new Date().toISOString()
    
    cards.value = deckCardsResponse.data.filter(c => c.next_review <= now).sort((a,b) => a.next_review.localeCompare(b.next_review))
    
    loading.value = false
  } catch (e) {
    console.error(e)
    loading.value = false
  }
}

const rateCard = async (rating) => {
  const card = currentCard.value
  try {
    await axios.post(`http://localhost:5000/api/cards/${card.id}/review`, { rating })
    
    // Move to next
    isFlipped.value = false
    currentIndex.value++
    
    // If done
    if (currentIndex.value >= cards.value.length) {
        cards.value = [] // clear to trigger empty state
    }
  } catch (e) {
    alert("Error submitting review")
  }
}

onMounted(() => {
  fetchCards()
})
</script>

<style scoped>
.perspective-1000 {
  perspective: 1000px;
}
.transform-style-3d {
  transform-style: preserve-3d;
}
.backface-hidden {
  backface-visibility: hidden;
}
.rotate-y-180 {
  transform: rotateY(180deg);
}
</style>
