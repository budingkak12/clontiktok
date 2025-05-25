<script setup>
import { ref } from 'vue'
import { Icon } from '@iconify/vue'

const activeStates = ref({
  button1: false,
  button2: false,
  button3: false,
  button4: false,
  button5: false,
  button6: false,
  button7: false,
  button8: false
})

const toggleLike = (button) => {
  activeStates.value[button] = !activeStates.value[button]
}

// 只保留心形图标，不要其他形状
const iconSets = [
  {
    outline: 'lucide:heart',
    filled: 'lucide:heart-filled',
    label: '简约心形'
  },
  {
    outline: 'tabler:heart',
    filled: 'tabler:heart-filled',
    label: 'Tabler心形'
  },
  {
    outline: 'ph:heart',
    filled: 'ph:heart-fill',
    label: 'Phosphor心形'
  },
  {
    outline: 'feather:heart',
    filled: 'mdi:heart',
    label: 'Feather心形'
  },
  {
    outline: 'clarity:heart-line',
    filled: 'clarity:heart-solid',
    label: 'Clarity心形'
  },
  {
    outline: 'ri:heart-line',
    filled: 'ri:heart-fill',
    label: 'Remix心形'
  },
  {
    outline: 'akar-icons:heart',
    filled: 'ant-design:heart-filled',
    label: 'Akar心形'
  },
  {
    outline: 'bi:heart',
    filled: 'bi:heart-fill',
    label: 'Bootstrap心形'
  }
]
</script>

<template>
  <div class="minimal-container">
    <h2>纯粹心形点赞按钮</h2>
    
    <div class="minimal-buttons-grid">
      <div v-for="(iconSet, index) in iconSets" :key="index" class="button-container">
        <button 
          class="pure-like-button" 
          :class="{ 'is-active': activeStates[`button${index + 1}`] }"
          @click="toggleLike(`button${index + 1}`)"
          aria-label="点赞"
        >
          <Icon 
            :icon="activeStates[`button${index + 1}`] ? iconSet.filled : iconSet.outline" 
            width="36" 
            height="36" 
            class="icon"
          />
        </button>
        <div class="minimal-button-label">{{ iconSet.label }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.minimal-container {
  padding: 2rem;
}

.minimal-buttons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.pure-like-button {
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.25s ease;
  padding: 10px;
}

.pure-like-button:hover {
  transform: scale(1.15);
}

.pure-like-button:active {
  transform: scale(0.9);
}

.pure-like-button .icon {
  color: white;
  stroke-width: 1.5;
  transition: all 0.3s ease;
}

.pure-like-button.is-active .icon {
  color: #ff5252;
  filter: drop-shadow(0 0 4px rgba(255, 82, 82, 0.7));
  transform: scale(1.2);
}

.minimal-button-label {
  margin-top: 0.75rem;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.8);
}

/* 暗色背景 */
:root {
  --app-bg: #121212;
}
</style> 