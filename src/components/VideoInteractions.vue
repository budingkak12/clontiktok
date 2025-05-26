<template>
  <div class="video-interactions">
    <!-- 按钮组容器 -->
    <div class="action-buttons">
      <!-- 点赞按钮 -->
      <div class="action-button" @click="handleAction('like')">
        <svg 
          class="action-icon" 
          :class="{ active: states.isLiked }" 
          viewBox="0 0 24 24" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
        </svg>
      </div>
      
      <!-- 收藏按钮 -->
      <div class="action-button" @click="handleAction('collect')">
        <svg 
          class="action-icon" 
          :class="{ active: states.isCollected }" 
          viewBox="0 0 24 24" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <path d="M17 3H7c-1.1 0-2 .9-2 2v16l7-3 7 3V5c0-1.1-.9-2-2-2z" />
        </svg>
      </div>
      
      <!-- 标签按钮 -->
      <div class="action-button" @click="openTagDialog">
        <svg 
          class="action-icon" 
          viewBox="0 0 24 24" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <path d="M21.41 11.58l-9-9C12.05 2.22 11.55 2 11 2H4c-1.1 0-2 .9-2 2v7c0 .55.22 1.05.59 1.42l9 9c.36.36.86.58 1.41.58s1.05-.22 1.41-.59l7-7c.37-.36.59-.86.59-1.41s-.23-1.06-.59-1.42zM5.5 7C4.67 7 4 6.33 4 5.5S4.67 4 5.5 4 7 4.67 7 5.5 6.33 7 5.5 7z" />
        </svg>
      </div>
      
      <!-- 删除按钮 -->
      <div class="action-button" @click="handleAction('delete')">
        <svg 
          class="action-icon" 
          viewBox="0 0 24 24" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
        </svg>
      </div>
    </div>
    
    <!-- 标签弹窗 -->
    <div v-if="isTagDialogOpen" class="dialog-overlay" @click="closeTagDialog">
      <div class="tag-dialog" @click.stop>
        <div class="dialog-header">
          <h3>添加标签</h3>
          <button class="close-button" @click="closeTagDialog">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
            </svg>
          </button>
        </div>
        
        <!-- 自定义标签输入 -->
        <div class="custom-tag-input">
          <input 
            type="text" 
            v-model="customTag" 
            placeholder="输入自定义标签" 
            @keyup.enter="addCustomTag"
          />
          <button class="add-button" @click="addCustomTag">添加</button>
        </div>
        
        <!-- 预设标签列表 -->
        <div class="preset-tags">
          <h4>常用标签</h4>
          <div class="tags-container">
            <button 
              v-for="tag in presetTags" 
              :key="tag"
              class="tag-item"
              :class="{ selected: selectedTags.includes(tag) }"
              @click="toggleTag(tag)"
            >
              {{ tag }}
            </button>
          </div>
        </div>
        
        <!-- 已选标签 -->
        <div class="selected-tags" v-if="selectedTags.length > 0">
          <h4>已选标签</h4>
          <div class="tags-container">
            <div v-for="tag in selectedTags" :key="tag" class="tag-item selected">
              {{ tag }}
              <button class="remove-tag" @click="removeTag(tag)">×</button>
            </div>
          </div>
        </div>
        
        <!-- 确认按钮 -->
        <button class="confirm-button" @click="confirmTags">确认</button>
      </div>
    </div>
    
    <!-- 通知 -->
    <div class="notification" v-if="notification.show">
      {{ notification.message }}
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import { useEventListener } from '@vueuse/core';

export default {
  name: 'VideoInteractions',
  props: {
    initialLiked: {
      type: Boolean,
      default: false
    },
    initialCollected: {
      type: Boolean,
      default: false
    },
    initialTags: {
      type: Array,
      default: () => []
    }
  },
  setup(props, { emit }) {
    const states = ref({
      isLiked: props.initialLiked,
      isCollected: props.initialCollected
    });
    
    const notification = ref({
      show: false,
      message: ''
    });
    
    // 标签相关状态
    const isTagDialogOpen = ref(false);
    const customTag = ref('');
    const selectedTags = ref([...props.initialTags]);
    const presetTags = ref([
      '搞笑', '生活', '美食', '旅行', '音乐',
      '舞蹈', '宠物', '知识', '运动', '游戏',
      '时尚', '科技', '创意', '情感', '健身'
    ]);
    
    // 处理 ESC 键关闭弹窗
    const escapeHandler = (e) => {
      if (e.key === 'Escape' && isTagDialogOpen.value) {
        closeTagDialog();
      }
    };
    
    onMounted(() => {
      document.addEventListener('keydown', escapeHandler);
    });
    
    onUnmounted(() => {
      document.removeEventListener('keydown', escapeHandler);
    });
    
    const handleAction = (type) => {
      // 为点击的按钮添加动画效果
      addClickEffect(type);
      
      switch(type) {
        case 'like':
          states.value.isLiked = !states.value.isLiked;
          showNotification(states.value.isLiked ? '已点赞视频' : '已取消点赞');
          emit('like-change', { isLiked: states.value.isLiked });
          break;
        case 'collect':
          states.value.isCollected = !states.value.isCollected;
          showNotification(states.value.isCollected ? '已收藏视频' : '已取消收藏');
          emit('collect-change', { isCollected: states.value.isCollected });
          break;
        case 'delete':
          showNotification('已删除视频');
          emit('delete-click');
          break;
      }
    };
    
    const addClickEffect = (type) => {
      // 获取对应按钮的索引
      const index = ['like', 'collect', 'tag', 'delete'].indexOf(type);
      if (index === -1) return;
      
      // 获取对应的图标元素并添加动画
      const button = document.querySelectorAll('.action-button')[index];
      if (!button) return;
      
      const icon = button.querySelector('.action-icon');
      if (!icon) return;
      
      // 先移除可能存在的动画类，避免连续点击时动画不正常
      icon.classList.remove('click-effect');
      
      // 强制浏览器重绘
      void icon.offsetWidth;
      
      // 添加动画类
      icon.classList.add('click-effect');
      
      // 一段时间后移除动画类
      setTimeout(() => {
        icon.classList.remove('click-effect');
      }, 200);
    };
    
    const showNotification = (message) => {
      notification.value.message = message;
      notification.value.show = true;
      
      setTimeout(() => {
        notification.value.show = false;
      }, 2000);
    };
    
    // 标签相关方法
    const openTagDialog = () => {
      addClickEffect('tag');
      isTagDialogOpen.value = true;
    };
    
    const closeTagDialog = () => {
      isTagDialogOpen.value = false;
    };
    
    const addCustomTag = () => {
      if (!customTag.value.trim()) return;
      
      // 检查是否已存在相同标签
      if (!selectedTags.value.includes(customTag.value.trim())) {
        selectedTags.value.push(customTag.value.trim());
      }
      
      // 清空输入
      customTag.value = '';
    };
    
    const toggleTag = (tag) => {
      const index = selectedTags.value.indexOf(tag);
      if (index === -1) {
        // 添加标签
        selectedTags.value.push(tag);
      } else {
        // 移除标签
        selectedTags.value.splice(index, 1);
      }
    };
    
    const removeTag = (tag) => {
      const index = selectedTags.value.indexOf(tag);
      if (index !== -1) {
        selectedTags.value.splice(index, 1);
      }
    };
    
    const confirmTags = () => {
      emit('tags-change', { tags: [...selectedTags.value] });
      showNotification(`已添加 ${selectedTags.value.length} 个标签`);
      closeTagDialog();
    };
    
    return {
      states,
      notification,
      isTagDialogOpen,
      customTag,
      selectedTags,
      presetTags,
      handleAction,
      addClickEffect,
      showNotification,
      openTagDialog,
      closeTagDialog,
      addCustomTag,
      toggleTag,
      removeTag,
      confirmTags
    };
  }
};
</script>

<style scoped>
.video-interactions {
  position: fixed;
  right: 16px;
  bottom: 120px;
  z-index: 100;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.action-button {
  display: flex;
  justify-content: center;
  align-items: center;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
  cursor: pointer;
}

.action-icon {
  width: 30px;
  height: 30px;
  fill: rgba(255, 255, 255, 0.9);
  stroke: rgba(255, 255, 255, 0.9);
  stroke-width: 1;
  transition: all 0.15s ease;
}

.action-icon.active {
  fill: #fe2c55;
  stroke: #fe2c55;
}

@keyframes click-effect {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(0.85);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.click-effect {
  animation: click-effect 0.2s ease-out;
}

.notification {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 14px;
  z-index: 1000;
}

/* 标签弹窗样式 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.tag-dialog {
  background-color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  max-height: 80vh;
  overflow-y: auto;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.dialog-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}

.close-button svg {
  width: 20px;
  height: 20px;
  fill: #666;
}

.custom-tag-input {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.custom-tag-input input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
}

.custom-tag-input input:focus {
  border-color: #fe2c55;
}

.add-button {
  background-color: #fe2c55;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0 15px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-button:hover {
  background-color: #e6214d;
}

.preset-tags, .selected-tags {
  margin-bottom: 20px;
}

.preset-tags h4, .selected-tags h4 {
  margin: 0 0 10px;
  font-size: 15px;
  font-weight: 500;
  color: #666;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  display: inline-flex;
  align-items: center;
  background-color: #f5f5f5;
  color: #333;
  border-radius: 16px;
  padding: 6px 12px;
  font-size: 13px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.tag-item.selected {
  background-color: #ffe8ec;
  color: #fe2c55;
  border-color: #fe2c55;
}

.remove-tag {
  background: none;
  border: none;
  color: #fe2c55;
  font-size: 16px;
  margin-left: 5px;
  cursor: pointer;
  padding: 0 0 0 5px;
}

.confirm-button {
  width: 100%;
  background-color: #fe2c55;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.confirm-button:hover {
  background-color: #e6214d;
}

/* 适配移动设备 */
@media (max-width: 767px) {
  .video-interactions {
    right: 10px;
    bottom: 100px;
  }
  
  .action-buttons {
    gap: 15px;
  }
  
  .action-icon {
    width: 28px;
    height: 28px;
  }
  
  .notification {
    font-size: 12px;
    padding: 8px 16px;
  }
  
  .tag-dialog {
    padding: 16px;
  }
  
  .dialog-header h3 {
    font-size: 16px;
  }
  
  .tag-item {
    padding: 5px 10px;
    font-size: 12px;
  }
}

/* 处理移动设备触摸反馈 */
@media (hover: hover) {
  .action-icon:hover {
    transform: scale(1.1);
  }
  
  .tag-item:hover:not(.selected) {
    background-color: #eee;
  }
}
</style> 