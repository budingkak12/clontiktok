<script setup>
import TikTokLikeButtons from './components/TikTokLikeButtons.vue'
</script>

<template>
  <div class="dark-app-container">
    <h1 class="app-title">抖音风格点赞按钮</h1>
    <TikTokLikeButtons />
  </div>
</template>

<style>
body {
  margin: 0;
  padding: 0;
  background-color:hsla(207, 52.20%, 54.90%, 0.86);
  color: white;
  font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  min-height: 100vh;
}

.dark-app-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.app-title {
  text-align: center;
  margin-bottom: 2rem;
  font-weight: 600;
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.9);
}
</style>
