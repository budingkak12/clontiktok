<template>
  <div class="search-page">
    <div class="search-header">
      <a-button class="back-button" type="text" size="large" @click="closeSearch">
        <template #icon>
          <icon-arrow-left />
        </template>
      </a-button>
      <h2>搜索</h2>
    </div>

    <!-- 标签搜索框 -->
    <div class="search-bar">
      <a-input-search
        v-model="searchInput"
        placeholder="输入标签搜索"
        search-button
        @search="addTagFromInput"
        @press-enter="addTagFromInput"
        class="custom-search"
      >
        <template #prefix>
          <div class="selected-tags-container" v-if="selectedTags.length > 0">
            <a-tag
              v-for="tag in selectedTags"
              :key="tag"
              color="#666"
              bordered
              closable
              @close="removeTag(tag)"
            >
              {{ tag }}
            </a-tag>
          </div>
        </template>
      </a-input-search>
    </div>

    <!-- 过滤开关 -->
    <div class="filter-switches">
      <div class="switch-container">
        <a-switch v-model="showLiked" @change="onLikedToggle" />
        <span class="switch-label">查看喜欢</span>
      </div>
      
      <div class="switch-container">
        <a-switch v-model="showCollected" @change="onCollectedToggle" />
        <span class="switch-label">查看收藏</span>
      </div>
    </div>

    <!-- 常用标签 -->
    <div class="common-tags">
      <h3>常用标签</h3>
      <div class="tags-container">
        <a-tag
          v-for="tag in commonTags"
          :key="tag"
          :color="selectedTags.includes(tag) ? '#666' : ''"
          bordered
          checkable
          :checked="selectedTags.includes(tag)"
          @click="addTag(tag)"
          class="custom-tag"
        >
          {{ tag }}
        </a-tag>
        <a-tag class="add-tag" @click="showAddCommonTagDialog = true">
          <template #icon>
            <icon-plus />
          </template>
          添加
        </a-tag>
      </div>
    </div>

    <!-- 添加常用标签弹窗 -->
    <a-modal
      v-model:visible="showAddCommonTagDialog"
      title="添加常用标签"
      @cancel="showAddCommonTagDialog = false"
      simple
    >
      <div class="custom-tag-input">
        <a-input
          v-model="newCommonTag"
          placeholder="输入常用标签"
          allow-clear
          @press-enter="addCommonTag"
        />
      </div>
      <template #footer>
        <a-button type="primary" @click="addCommonTag" style="background-color: #666; border-color: #666;">添加</a-button>
      </template>
    </a-modal>

    <!-- 搜索结果网格 -->
    <div class="search-results">
      <a-empty v-if="searchResults.length === 0" description="暂无搜索结果" />
      <div v-else class="results-grid">
        <div class="grid-item" v-for="(item, index) in searchResults" :key="index">
          <div class="item-placeholder">
            <div class="item-tags">
              <a-tag
                class="item-tag"
                v-for="tag in item.tags"
                :key="tag"
                color="#666"
                size="small"
                bordered
              >
                {{ tag }}
              </a-tag>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchPage',
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      searchInput: '',
      selectedTags: [],
      showLiked: false,
      showCollected: false,
      commonTags: ['搞笑', '生活', '美食', '旅行', '音乐'],
      showAddCommonTagDialog: false,
      newCommonTag: '',
      searchResults: []
    }
  },
  watch: {
    visible(newVal) {
      if (newVal) {
        // 当搜索页面显示时，重置搜索状态
        this.resetSearch();
      }
    }
  },
  methods: {
    closeSearch() {
      this.$emit('close');
    },
    
    resetSearch() {
      this.searchInput = '';
      this.selectedTags = [];
      this.showLiked = false;
      this.showCollected = false;
      this.searchResults = [];
    },
    
    addTagFromInput() {
      if (!this.searchInput.trim()) return;
      
      // 添加标签
      if (!this.selectedTags.includes(this.searchInput.trim())) {
        this.selectedTags.push(this.searchInput.trim());
      }
      
      // 清空输入
      this.searchInput = '';
      
      // 自动搜索
      this.search();
    },
    
    addTag(tag) {
      const index = this.selectedTags.indexOf(tag);
      if (index === -1) {
        this.selectedTags.push(tag);
      } else {
        this.selectedTags.splice(index, 1);
      }
      this.search();
    },
    
    removeTag(tag) {
      const index = this.selectedTags.indexOf(tag);
      if (index !== -1) {
        this.selectedTags.splice(index, 1);
        this.search();
      }
    },
    
    onLikedToggle() {
      // 互斥处理
      if (this.showLiked && this.showCollected) {
        this.showCollected = false;
      }
      this.search();
    },
    
    onCollectedToggle() {
      // 互斥处理
      if (this.showCollected && this.showLiked) {
        this.showLiked = false;
      }
      this.search();
    },
    
    addCommonTag() {
      if (!this.newCommonTag.trim()) return;
      
      // 检查是否已存在相同标签
      if (!this.commonTags.includes(this.newCommonTag.trim())) {
        this.commonTags.push(this.newCommonTag.trim());
      }
      
      // 清空输入
      this.newCommonTag = '';
      
      // 关闭对话框
      this.showAddCommonTagDialog = false;
    },
    
    search() {
      // 模拟搜索结果，实际应用中这里应该调用API
      // 根据选中的标签、喜欢和收藏状态过滤结果
      
      // 如果没有选择任何条件，则显示空结果
      if (this.selectedTags.length === 0 && !this.showLiked && !this.showCollected) {
        this.searchResults = [];
        return;
      }
      
      // 模拟一些搜索结果
      const mockResults = [
        { id: 1, tags: ['搞笑', '生活'], liked: true, collected: false },
        { id: 2, tags: ['美食', '生活'], liked: false, collected: true },
        { id: 3, tags: ['旅行', '音乐'], liked: true, collected: true },
        { id: 4, tags: ['搞笑', '音乐'], liked: false, collected: false },
        { id: 5, tags: ['美食', '旅行'], liked: true, collected: false },
        { id: 6, tags: ['生活', '音乐'], liked: false, collected: true }
      ];
      
      // 根据条件过滤
      this.searchResults = mockResults.filter(item => {
        // 标签过滤
        const hasAllTags = this.selectedTags.length === 0 || 
          this.selectedTags.every(tag => item.tags.includes(tag));
        
        // 喜欢和收藏过滤
        const matchesLiked = !this.showLiked || item.liked;
        const matchesCollected = !this.showCollected || item.collected;
        
        return hasAllTags && matchesLiked && matchesCollected;
      });
    }
  }
}
</script>

<style scoped>
.search-page {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #333;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  color: #fff;
  overflow-y: auto;
}

.search-header {
  display: flex;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.back-button {
  margin-right: 16px;
  color: #fff !important;
}

.search-bar {
  padding: 16px;
}

.custom-search :deep(.arco-input-wrapper) {
  background-color: rgba(255, 255, 255, 0.1) !important;
  border-color: transparent !important;
}

.custom-search :deep(.arco-input) {
  color: #fff !important;
}

.custom-search :deep(.arco-input-search-btn) {
  background-color: #666 !important;
  border-color: #666 !important;
}

.selected-tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-right: 8px;
}

.filter-switches {
  display: flex;
  padding: 16px;
  gap: 24px;
}

.switch-container {
  display: flex;
  align-items: center;
}

.switch-label {
  margin-left: 8px;
}

.common-tags {
  padding: 16px;
}

.common-tags h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 16px;
  font-weight: normal;
  color: rgba(255, 255, 255, 0.6);
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

/* 统一所有标签样式 */
:deep(.arco-tag) {
  background-color: rgba(255, 255, 255, 0.1) !important;
  border-color: transparent !important;
  color: #fff !important;
}

:deep(.arco-tag.arco-tag-checked) {
  background-color: rgba(102, 102, 102, 0.2) !important;
  border-color: #666 !important;
  color: #fff !important;
}

:deep(.arco-tag-close-btn) {
  color: #fff !important;
}

.custom-tag {
  background-color: rgba(255, 255, 255, 0.1) !important;
  border-color: transparent !important;
  color: #fff !important;
}

.custom-tag.arco-tag-checked {
  background-color: rgba(102, 102, 102, 0.2) !important;
  border-color: #666 !important;
  color: #fff !important;
}

.add-tag {
  cursor: pointer;
  background-color: rgba(255, 255, 255, 0.1) !important;
  border-color: transparent !important;
  color: #fff !important;
}

.custom-tag-input {
  margin-bottom: 16px;
}

.search-results {
  flex: 1;
  padding: 16px;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.grid-item {
  aspect-ratio: 1/1;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.item-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-tags {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 8px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* 移动设备优化 */
@media (max-width: 767px) {
  .results-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style> 