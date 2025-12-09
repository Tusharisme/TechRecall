import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue') },
  { path: '/study/:id', name: 'Study', component: () => import('../views/StudyView.vue') },
  { path: '/decks/:id', name: 'DeckEditor', component: () => import('../views/DeckEditor.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
