import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomePage.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutPage.vue')
    },
    {
      path: '/interests',
      name: 'interests',
      component: () => import('../views/InterestsPage.vue')
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/ContactPage.vue')
    },
    // 废弃的博客路由 - 重定向到 404
    {
      path: '/blog',
      name: 'blog',
      component: () => import('../views/NotFound.vue')
    },
    {
      path: '/blog/:id',
      name: 'post',
      component: () => import('../views/NotFound.vue')
    },
    {
      path: '/blog/:id/preview',
      name: 'post-preview',
      component: () => import('../views/NotFound.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginPage.vue')
    },
    {
      path: '/management',
      name: 'management',
      component: () => import('../views/ManagementPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'notfound',
      component: () => import('../views/NotFound.vue')
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    } else {
      return { top: 0 }
    }
  }
})

export default router
