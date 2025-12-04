<template>
  <DefaultLayout>
    <main class="error-container theme-transition">
      <section class="error-card">
        <div class="error-hero" aria-hidden="true">
          <span class="d1">{{ content.errorCode[0] }}</span>
          <span class="d2">{{ content.errorCode[1] }}</span>
          <span class="d3">{{ content.errorCode[2] }}</span>
        </div>
        <h1 class="error-title">{{ content.title }}</h1>
        <p class="error-desc">{{ content.description }}</p>
        <div class="error-actions">
          <RouterLink class="btn primary" to="/">{{ content.buttons.home }}</RouterLink>
          <button class="btn" type="button" @click="goBack">{{ content.buttons.back }}</button>
        </div>
      </section>
    </main>
  </DefaultLayout>
</template>

<script setup>
import { useRouter, RouterLink } from 'vue-router'
import { useHead } from '@vueuse/head';
import DefaultLayout from '../components/DefaultLayout.vue'
import { pages } from '@/utils/content'

const content = pages.notFound
const router = useRouter()

useHead ({
  title: content.meta.title,
  meta: [
    { name: 'description', content: content.meta.description }
  ]
})

const goBack = () => {
  router.go(-1)
}
</script>

<style>
@import '../assets/css/error.css';
</style>
