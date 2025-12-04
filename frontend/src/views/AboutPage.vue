<template>
  <DefaultLayout>
    <section class="page-hero mini">
      <div class="container">
        <h1>{{ content.hero.title }}</h1>
        <p class="subtitle">{{ content.hero.subtitle }}</p>
      </div>
    </section>
    <section class="section">
      <div class="container narrow">
        <h2>{{ content.intro.title }}</h2>
        <p id="about-me">特别鸣谢：Gemini 2.5pro，GPT 5。即使我没HTML+CSS+JavaScript基础也能写出自己的个人网站。<br>
            懂一些Python，也是重新捡起来了。<s>虽然不知道能干嘛</s><br>
            慢悠悠开始学cpp，也是接触了新世界啊（指相对于Python而言。<br>
            回头就去学Typescripts<br>
            研究AI画图ing，以后想画啥画啥<br>
            正在严肃学习Vue<br>
            所以谁来和我玩<RouterLink to="/interests#p1">游戏</RouterLink>啊！那我问你!<br>
            </p>
        <h2>{{ content.skills.title }}</h2>
        <ul class="tag-list large">
          <li v-for="tag in content.skills.tags" :key="tag">{{ tag }}</li>
        </ul>
        <h2>{{ timelineData.title }}</h2>
        <ul class="timeline">
          <li v-for="event in timelineData.events" :key="event.date">
            <span class="time">{{ event.date }}</span>
            <div class="event" v-html="event.content"></div>
          </li>
        </ul>
      </div>
    </section>
  </DefaultLayout>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useHead } from '@vueuse/head'
import DefaultLayout from '../components/DefaultLayout.vue'
import { pages, timeline } from '@/utils/content'

const content = pages.about
const timelineData = timeline

// 设置页面标题和描述
useHead({
  title: content.meta.title,
  meta: [
    { name: 'description', content: content.meta.description }
  ]
})

</script>

<style scoped>
/* 时间轴 Timeline */
.timeline {
    list-style: none;
    margin: 1.5rem 0 0;
    padding: 0;
    border-left: 2px solid var(--color-border);
}

.timeline li {
    position: relative;
    padding: .75rem 0 .75rem 1.25rem;
}

.timeline li:before {
    content: "";
    position: absolute;
    left: -6px;
    top: 1.15rem;
    width: 10px;
    height: 10px;
    background: var(--color-accent);
    border-radius: 50%;
    box-shadow: 0 0 0 3px var(--color-bg);
}

.timeline .time {
    font-weight: 600;
    display: inline-block;
    min-width: 3.5rem;
}

.timeline .event {
    display: inline-block;
    color: var(--color-text);
}

</style>
