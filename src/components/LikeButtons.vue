<script setup>
import { ref } from 'vue'
import { Icon } from '@iconify/vue'

const likes = ref({
  button1: 0,
  button2: 0,
  button3: 0,
  button4: 0,
  button5: 0,
  button6: 0,
  button7: 0,
  button8: 0,
  button9: 0,
  button10: 0
})

const incrementLike = (button) => {
  likes.value[button]++
}

const iconSets = [
  { icon: 'mdi:heart', style: 'text-red-500' },
  { icon: 'mdi:thumb-up', style: 'text-blue-500' },
  { icon: 'ph:heart-fill', style: 'text-pink-500' },
  { icon: 'solar:heart-bold', style: 'text-purple-500' },
  { icon: 'icon-park-outline:like', style: 'text-green-500' },
  { icon: 'ri:heart-3-fill', style: 'text-orange-500' },
  { icon: 'tabler:thumb-up-filled', style: 'text-yellow-500' },
  { icon: 'octicon:heart-fill-24', style: 'text-rose-500' },
  { icon: 'fluent:heart-28-filled', style: 'text-indigo-500' },
  { icon: 'carbon:favorite-filled', style: 'text-cyan-500' }
]
</script>

<template>
  <div class="container">
    <h2>请选择一种点赞按钮风格</h2>
    
    <div class="buttons-grid">
      <div v-for="(iconSet, index) in iconSets" :key="index" class="button-wrapper">
        <button 
          class="like-button" 
          @click="incrementLike(`button${index + 1}`)"
        >
          <Icon :icon="iconSet.icon" :class="iconSet.style" width="24" height="24" />
          <span>{{ likes[`button${index + 1}`] }}</span>
        </button>
        <div class="button-label">风格 {{ index + 1 }}: {{ iconSet.icon }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  margin: 2rem auto;
  text-align: center;
}

.buttons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.button-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.like-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.like-button:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.button-label {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #666;
}
</style> 