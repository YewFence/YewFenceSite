import { createRouter, createWebHistory } from 'vue-router'

// 博客重定向地址
const blogRedirectUrl = import.meta.env.VITE_BLOG_REDIRECT_URL

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
    // 废弃的博客路由 - 重定向到外部链接，如果环境变量为空则 404
    {
      path: '/blog',
      name: 'blog',
      component: () => import('../views/NotFound.vue'),
      beforeEnter: () => {
        if (blogRedirectUrl) {
          window.location.href = blogRedirectUrl
          return false
        }
      }
    },
    {
      path: '/blog/:id',
      name: 'post',
      component: () => import('../views/NotFound.vue'),
      beforeEnter: () => {
        if (blogRedirectUrl) {
          window.location.href = blogRedirectUrl
          return false
        }
      }
    },
    {
      path: '/blog/:id/preview',
      name: 'post-preview',
      component: () => import('../views/NotFound.vue'),
      beforeEnter: () => {
        if (blogRedirectUrl) {
          window.location.href = blogRedirectUrl
          return false
        }
      }
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
