<template>
  <div id="app">
    <div class="video-container">
      <div class="video-placeholder">
        <div class="video-placeholder-text">视频内容区域</div>
        
        <!-- 显示当前标签 -->
        <div class="current-tags" v-if="videoTags.length > 0">
          <div class="tag-list">
            <a-tag 
              v-for="tag in videoTags" 
              :key="tag" 
              class="video-tag"
            >
              {{ tag }}
            </a-tag>
          </div>
        </div>
      </div>
      
      <!-- 搜索按钮 - 右上角 -->
      <div class="search-button-container">
        <a-button 
          class="search-button" 
          type="primary" 
          shape="circle" 
          size="large" 
          @click="showSearchPage = true"
        >
          <template #icon>
            <icon-search />
          </template>
        </a-button>
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
    
    <!-- 搜索页面组件 -->
    <SearchPage 
      v-if="showSearchPage" 
      :visible="showSearchPage" 
      @close="showSearchPage = false"
    />
  </div>
</template>

<script>
import VideoInteractions from './components/VideoInteractions.vue'
import SearchPage from './components/SearchPage.vue'

export default {
  name: 'App',
  components: {
    VideoInteractions,
    SearchPage
  },
  data() {
    return {
      videoTags: ['搞笑', '生活'],  // 初始标签
      showSearchPage: false        // 控制搜索页面的显示/隐藏
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
  background-color: #333;
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
  background-color: #333;
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

/* 视频标签样式 */
.video-tag {
  background-color: rgba(255, 255, 255, 0.1) !important;
  border-color: transparent !important;
  color: #fff !important;
}

/* 搜索按钮样式 */
.search-button-container {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 100;
}

.search-button {
  background-color: #666 !important;
  border-color: #666 !important;
  font-size: 18px !important;
  width: 44px !important;
  height: 44px !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
}

/* 移动设备优化 */
@media (max-width: 767px) {
  #app {
    padding: 10px 0;
  }
  
  .search-button-container {
    top: 12px;
    right: 12px;
  }
}
</style>
