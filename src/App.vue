<template>
  <div id="app">
    <div class="video-container">
      <div class="video-placeholder">
        <div class="video-placeholder-text">视频内容区域</div>
        
        <!-- 显示当前标签 -->
        <div class="current-tags" v-if="videoTags.length > 0">
          <div class="tag-list">
            <span class="tag" v-for="tag in videoTags" :key="tag">{{ tag }}</span>
          </div>
        </div>
      </div>
      
      <VideoInteractions 
        :initialLiked="false"
        :initialCollected="false"
        :initialTags="videoTags"
        @like-change="onLikeChange"
        @collect-change="onCollectChange"
        @tags-change="onTagsChange"
        @delete-click="onDeleteClick"
      />
    </div>
  </div>
</template>

<script>
import VideoInteractions from './components/VideoInteractions.vue'

export default {
  name: 'App',
  components: {
    VideoInteractions
  },
  data() {
    return {
      videoTags: ['搞笑', '生活']  // 初始标签
    }
  },
  methods: {
    onLikeChange(status) {
      console.log('点赞状态:', status.isLiked);
    },
    onCollectChange(status) {
      console.log('收藏状态:', status.isCollected);
    },
    onTagsChange(data) {
      console.log('标签已更新:', data.tags);
      this.videoTags = data.tags;
    },
    onDeleteClick() {
      console.log('点击了删除按钮');
    }
  }
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
  background-color: #000;
  color: #fff;
  overflow: hidden;
}

#app {
  width: 100%;
  height: 100vh;
}

.video-container {
  position: relative;
  width: 100%;
  height: 100vh;
  background-color: #000;
  overflow: hidden;
}

.video-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.video-placeholder-text {
  font-size: 24px;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 20px;
}

.current-tags {
  margin-top: 10px;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  max-width: 80%;
}

.tag {
  background-color: rgba(254, 44, 85, 0.2);
  color: #fe2c55;
  border: 1px solid #fe2c55;
  border-radius: 16px;
  padding: 4px 10px;
  font-size: 13px;
}

/* 移动设备优化 */
@media (max-width: 767px) {
  #app {
    padding: 10px 0;
  }
  
  .tag {
    font-size: 12px;
    padding: 3px 8px;
  }
}
</style>
