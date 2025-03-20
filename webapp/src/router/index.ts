import { createRouter, createWebHistory } from 'vue-router'
import RequestLogListPage from '@/components/pages/RequestLog/RequestLogListPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: RequestLogListPage
    }
  ]
})

export default router
