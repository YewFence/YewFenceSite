<template>
  <DefaultLayout>
    <section class="page-hero mini">
      <div class="container">
        <h1>关于我</h1>
        <p class="subtitle">一点背景 · 一些技能 · 一点展望</p>
      </div>
    </section>
    <section class="section">
      <div class="container narrow">
        <h2>简介</h2>
        <p id="about-me">特别鸣谢：Gemini 2.5pro，GPT 5。即使我没HTML+CSS+JavaScript基础也能写出自己的个人网站。<br>
            懂一些Python，也是重新捡起来了。<s>虽然不知道能干嘛</s><br>
            慢悠悠开始学cpp，也是接触了新世界啊（指相对于Python而言。<br>
            回头就去学Typescripts<br>
            研究AI画图ing，以后想画啥画啥<br>
            正在严肃学习Vue<br>
            所以谁来和我玩<RouterLink to="/interests#p1">游戏</RouterLink>啊！那我问你!<br>
            </p>
        <h2>技能图谱</h2>
        <ul class="tag-list large">
          <li>宅家大王，死不出门</li>
          <li>抱着电脑不松手</li>
          <li>刷一天短视频(下次一定戒掉)</li>
          <li>想多做少</li>
          <li>AI绘图</li>
          <li>AI api调用怎么整啊谁教教</li>
          <li>前端开发</li>
          <li>买一大堆史低游戏来吃灰</li>
        </ul>
        <h2>时间线</h2>
        <ul class="timeline">
          <li><span class="time">2025.11.3</span><div class="event">正式部署自己的网站，拥有了自己的域名和服务器，可喜可贺</div></li>
          <li><span class="time">2025.10.24</span><div class="event">个人博客的后端基本完工，Python救我</div></li>
          <li><span class="time">2025.10</span><div class="event">摸摸前端，YewFence's Site的伊始，希望还有未来</div></li>
          <li><span class="time">2025.8</span><div class="event">看看AI绘图是个啥</div></li>
          <li><span class="time">2025.6</span><div class="event">买一大堆steam游戏</div></li>
          <li><span class="time">2022</span><div class="event">来点二次元游戏<s>黑暗降临</s></div></li>
          <li><span class="time">2021</span><div class="event">学习python</div></li>
          <li><span class="time">2020</span><div class="event">看点番剧，好看爱看</div></li>
        </ul>
      </div>
    </section>
  </DefaultLayout>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useHead } from '@vueuse/head'
import DefaultLayout from '../components/DefaultLayout.vue'

// 设置页面标题和描述
useHead({
  title: '关于我 - YewFenceSite',
  meta: [
    { name: 'description', content: '了解YewFence的背景、技能、成分和时间线' }
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
