<script setup>
import { ref, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import gsap from 'gsap'

const activeStates = ref({
  like: false,
  favorite: false,
  tag: false,
  delete: false
})

// 创建动画时间线引用
const animationTimelines = ref({
  like: null,
  favorite: null,
  tag: null,
  delete: null
})

// 触摸反馈状态
const touchFeedback = ref({
  like: false,
  favorite: false,
  tag: false,
  delete: false
})

const toggleState = (type) => {
  activeStates.value[type] = !activeStates.value[type]
  
  // 使用GSAP执行动画
  const timeline = animationTimelines.value[type]
  if (timeline) {
    timeline.restart()
  }
}

onMounted(() => {
  // 为每个按钮创建GSAP动画时间线
  buttons.forEach(button => {
    const iconSelector = `.${button.type}-icon`
    
    // 创建动画时间线但不自动播放
    const tl = gsap.timeline({ paused: true })
    
    // 所有按钮使用同样优雅的动画
    tl.to(iconSelector, { 
      scale: 0.92, 
      duration: 0.3, 
      ease: "power2.out" 
    })
    .to(iconSelector, { 
      scale: 1.05, 
      duration: 0.5, 
      ease: "sine.out" 
    })
    .to(iconSelector, { 
      scale: 1, 
      duration: 0.4, 
      ease: "power1.out" 
    })
    
    animationTimelines.value[button.type] = tl
  })
})

// 触摸反馈函数
const handleTouchStart = (type) => {
  touchFeedback.value[type] = true
}

const handleTouchEnd = (type) => {
  touchFeedback.value[type] = false
}

const buttons = [
  {
    type: 'like',
    name: "点赞",
    outline: "ph:heart",
    filled: "ph:heart-fill",
    size: 28,
    color: "#FF2C55"
  },
  {
    type: 'favorite',
    name: "收藏",
    outline: "ph:bookmark-simple",
    filled: "ph:bookmark-simple-fill",
    size: 28,
    color: "#FFD426"
  },
  {
    type: 'tag',
    name: "标签",
    outline: "ph:tag",
    filled: "ph:tag-fill",
    size: 28,
    color: "#3DB4F2"
  },
  {
    type: 'delete',
    name: "删除",
    outline: "ph:trash",
    filled: "ph:trash-fill",
    size: 28,
    color: "#FF3B30"
  }
]
</script>

<template>
  <div class="tiktok-buttons-container">
    <div class="buttons-row">
      <div v-for="button in buttons" :key="button.type" class="button-container">
        <button 
          class="tiktok-action-button" 
          :class="{ 'is-active': activeStates[button.type], 'touch-feedback': touchFeedback[button.type] }"
          @click="toggleState(button.type)"
          @touchstart="handleTouchStart(button.type)"
          @touchend="handleTouchEnd(button.type)"
          @touchcancel="handleTouchEnd(button.type)"
          :aria-label="button.name"
        >
          <Icon 
            :icon="activeStates[button.type] ? button.filled : button.outline" 
            :width="button.size" 
            :height="button.size" 
            :class="['action-icon', `${button.type}-icon`]"
            :style="`--active-color: ${button.color}`"
          />
        </button>
        <div class="button-label">{{ button.name }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tiktok-buttons-container {
  width: 100%;
  padding: 20px;
  display: flex;
  justify-content: center;
}

.buttons-row {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 500px;
  margin-top: 2rem;
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.button-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  margin-top: 12px;
  text-align: center;
}

.tiktok-action-button {
  background: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  position: relative;
  outline: none;
  -webkit-tap-highlight-color: transparent; /* 移除iOS上的点击高亮 */
  touch-action: manipulation; /* 优化触摸行为，减少延迟 */
}

.action-icon {
  color: white;
  transition: color 0.5s ease;
}

.is-active .action-icon {
  color: var(--active-color);
}

/* 点击反馈效果 */
.touch-feedback {
  transform: scale(0.92);
}

/* 为每个按钮设置颜色 */
.like-icon {
  --active-color-rgb: 255, 44, 85;
}

.favorite-icon {
  --active-color-rgb: 255, 212, 38;
}

.tag-icon {
  --active-color-rgb: 61, 180, 242;
}

.delete-icon {
  --active-color-rgb: 255, 59, 48;
}
</style>

<style>
/* 全局样式，确保移动端优化 */
html {
  touch-action: manipulation;
}

@media (hover: none) {
  /* 只在触摸设备上应用这些样式 */
  .tiktok-action-button {
    padding: 12px;
  }
}
</style> 