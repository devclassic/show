import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      component: () => import('../views/index/Index.vue'),
    },
    {
      path: '/voice/asr',
      component: () => import('../views/voice/asr/Asr.vue'),
    },
    {
      path: '/voice/multi',
      component: () => import('../views/voice/multi/Multi.vue'),
    },
    {
      path: '/voice/form',
      component: () => import('../views/voice/form/Form.vue'),
    },
    {
      path: '/health/triage',
      component: () => import('../views/health/triage/Triage.vue'),
    },
    {
      path: '/health/assist',
      component: () => import('../views/health/assist/Assist.vue'),
    },
    {
      path: '/health/check',
      component: () => import('../views/health/check/Check.vue'),
    },
    {
      path: '/health/image',
      component: () => import('../views/health/image/Image.vue'),
    },
  ],
})

export default router
