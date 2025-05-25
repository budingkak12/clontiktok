<script setup>
import { ref } from 'vue'
import { Icon } from '@iconify/vue'

const isLiked = ref(false)
const isAnimating = ref(false)

const toggleLike = () => {
  isLiked.value = !isLiked.value
  
  if (isLiked.value) {
    isAnimating.value = true
    setTimeout(() => {
      isAnimating.value = false
    }, 800)
  }
}
</script>

<template>
  <div class="tiktok-like-container">
    <button 
      class="tiktok-like-button" 
      :class="{ 'is-liked': isLiked, 'is-animating': isAnimating }"
      @click="toggleLike"
      aria-label="点赞"
    >
      <Icon 
        :icon="isLiked ? 'ph:heart-fill' : 'ph:heart'" 
        width="24" 
        height="24" 
        class="heart-icon"
      />
    </button>
  </div>
</template>

<style scoped>
.tiktok-like-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.tiktok-like-button {
  background: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  position: relative;
  outline: none;
}

.heart-icon {
  color: white;
  stroke-width: 0;
  transition: all 0.2s ease;
  font-size: 28px;
}

.is-liked .heart-icon {
  color: #FF2C55; /* 抖音红色 */
}

.is-animating .heart-icon {
  animation: heartBeat 0.8s;
}

@keyframes heartBeat {
  0% {
    transform: scale(1);
  }
  15% {
    transform: scale(1.3);
  }
  30% {
    transform: scale(0.95);
  }
  45% {
    transform: scale(1.2);
  }
  60% {
    transform: scale(0.95);
  }
  100% {
    transform: scale(1);
  }
}
</style> 