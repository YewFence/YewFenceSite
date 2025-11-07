<template>
  <DefaultLayout>
    <section class="page-hero mini">
      <div class="container">
        <h1>兴趣</h1>
        <p class="subtitle">爱打游戏 · 喜欢编程 · 二次元</p>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="large-cards-list">
          <article id="p1" class="large-card">
            <h2>游戏成分</h2>
            <p class="meta">包括但不限于Steam单机游戏和二次元手游
            </p>
            <ul class="bullets">
              <li>鸣潮</li>
              <li>战双</li>
              <li>卡拉彼丘</li>
              <li>第五人格</li>
              <li>星露谷物语</li>
              <li>剑星</li>
              <li>地平线4</li>
              <li>主播女孩重度依赖</li>
              <li>Far：LoneSail</li>
              <li>饥荒</li>
              <li>异形工厂</li>
              <li>人类一败涂地</li>
            </ul>
          </article>
          <article id="p2" class="large-card">
            <h2>兴趣编程</h2>
            <p class="meta">前端，后端，运维，算法，AI</p>
            <ul class="bullets">
              <li>前端：HTML CSS JavaScript <p class="future">Vue Typescripts</p></li>
              <li>后端：flask SQLite<p class="future"> MySQL Node.js</p></li>
              <li>运维：Linux，Docker，Nginx<p class="future">CI/CD</p></li>
              <li>算法：<p class="future">C++</p></li>
              <li>AI：Stable Diffusion , Claude Code, Github Copilot<p class="future">SillyTavern, ComfyUI</p></li>
            </ul>
          </article>
          <article id="p3" class="large-card">
            <h2>二次元</h2>
            <p class="meta">番剧，轻小说</p>
            <ul class="bullets">
              <li>鬼灭之刃</li>
              <li>刀剑神域</li>
              <li>Re:从零开始的异世界生活</li>
              <li>间谍过家家</li>
              <li>86</li>
              <li>青之箱</li>
              <li>我推的孩子</li>
              <li>义妹生活</li>
              <li>游戏人生</li>
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

useHead({
  title: "我的兴趣 - YewFenceSite",
  meta: [
    { name: 'description', content: '了解YewFence的兴趣爱好' },
    { name: 'author', content: 'YewFence' }
  ]
})
</script>

<style scoped>
/* 页面样式已在全局CSS中定义 */
</style>
