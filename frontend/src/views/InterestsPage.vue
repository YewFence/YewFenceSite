<template>
  <DefaultLayout>
    <section class="page-hero mini">
      <div class="container">
        <h1>{{ content.hero.title }}</h1>
        <p class="subtitle">{{ content.hero.subtitle }}</p>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="large-cards-list">
          <!-- 游戏成分 -->
          <article :id="content.sections[0].id" class="large-card">
            <h2>{{ content.sections[0].title }}</h2>
            <p class="meta">{{ content.sections[0].description }}</p>
            <ul class="bullets">
              <li v-for="item in content.sections[0].items" :key="item">{{ item }}</li>
            </ul>
          </article>
          <!-- 兴趣编程 -->
          <article :id="content.sections[1].id" class="large-card">
            <h2>{{ content.sections[1].title }}</h2>
            <p class="meta">{{ content.sections[1].description }}</p>
            <ul class="bullets">
              <li v-for="item in content.sections[1].items" :key="item.category">
                {{ item.category }}：{{ item.current }}<p v-if="item.future" class="future">{{ item.future }}</p>
              </li>
            </ul>
          </article>
          <!-- 二次元 -->
          <article :id="content.sections[2].id" class="large-card">
            <h2>{{ content.sections[2].title }}</h2>
            <p class="meta">{{ content.sections[2].description }}</p>
            <ul class="bullets">
              <li v-for="item in content.sections[2].items" :key="item">{{ item }}</li>
            </ul>
          </article>
        </div>
      </div>
    </section>
  </DefaultLayout>
</template>

<script setup>
import { useHead } from '@vueuse/head';
import DefaultLayout from '../components/DefaultLayout.vue'
import { pages } from '@/utils/content'

const content = pages.interests

useHead({
  title: content.meta.title,
  meta: [
    { name: 'description', content: content.meta.description },
    { name: 'author', content: content.meta.author }
  ]
})
</script>

<style scoped>
/* 页面样式已在全局CSS中定义 */
</style>
