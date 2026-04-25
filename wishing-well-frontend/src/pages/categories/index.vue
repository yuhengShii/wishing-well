<template>
  <view class="page">
    <view class="header">
      <text class="title">{{ t('categories.title') }}</text>
    </view>

    <!-- 分类标签 -->
    <view class="category-tabs">
      <text
        v-for="cat in categories"
        :key="cat"
        class="category-tab"
        :class="{ active: selectedCategory === cat }"
        @tap="selectCategory(cat)"
      >
        {{ cat }}
      </text>
    </view>

    <!-- 愿望列表 -->
    <view class="list">
      <view v-if="filteredWishes.length === 0" class="empty">{{ t('categories.empty') }}</view>
      <view v-for="wish in filteredWishes" :key="wish.id" class="card">
        <view class="card-header">
          <text class="card-title">{{ wish.title }}</text>
          <text class="card-status" :class="'status-' + wish.status">
            {{ t('status.' + wish.status) }}
          </text>
        </view>
        <text v-if="wish.description" class="card-desc">{{ wish.description }}</text>
        <view class="card-footer">
          <text v-if="wish.category" class="tag">{{ wish.category }}</text>
          <text class="card-time">{{ formatTime(wish.created_at) }}</text>
        </view>
        <view class="vote-bar">
          <text class="vote-count">❤️ {{ wish.vote_count }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import Taro, { useDidShow } from "@tarojs/taro";
import { wishApi } from "../../api/wish";
import { t, localeState } from "../../locales";

const categories = ["全部", "生活", "工作", "学习", "健康", "娱乐", "其他", "财务", "社交", "旅行", "科技", "家居", "技能", "情感", "美食", "运动", "公益"];
const selectedCategory = ref("全部");
const allWishes = ref([]);

const filteredWishes = computed(() => {
  if (selectedCategory.value === "全部") {
    return allWishes.value;
  }
  return allWishes.value.filter(w => w.category === selectedCategory.value);
});

function selectCategory(cat) {
  selectedCategory.value = cat;
}

function refreshPage() {
  allWishes.value = [];
  fetchWishes();
}

async function fetchWishes() {
  try {
    const res = await wishApi.list({});
    allWishes.value = res.data;
  } catch (e) {
    Taro.showToast({ title: t('loadFailed'), icon: "none" });
  }
}

function formatTime(time) {
  return time ? time.slice(0, 10) : "";
}

onMounted(() => {
  fetchWishes();
});

useDidShow(() => {
  const _ = localeState.locale;
  refreshPage();
});
</script>

<style lang="scss">
.page {
  padding: 24px 16px;
  background: #f5f5f5;
  min-height: 100vh;
}

.header {
  margin-bottom: 16px;

  .title {
    font-size: 24px;
    font-weight: bold;
    color: #333;
  }
}

.category-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;

  .category-tab {
    font-size: 14px;
    color: #666;
    padding: 6px 14px;
    border-radius: 16px;
    background: #e8e8e8;

    &.active {
      background: #4a90e2;
      color: #fff;
    }
  }
}

.list {
  .empty {
    text-align: center;
    color: #999;
    padding: 40px 0;
  }
}

.card {
  background: #fff;
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 10px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;

    .card-title {
      font-size: 16px;
      font-weight: 600;
      color: #333;
    }

    .card-status {
      font-size: 12px;
      padding: 2px 8px;
      border-radius: 10px;

      &.status-pending { background: #fff3e0; color: #e67e22; }
      &.status-approved { background: #e8f5e9; color: #27ae60; }
      &.status-implemented { background: #e3f2fd; color: #2980b9; }
      &.status-rejected { background: #fce4ec; color: #c0392b; }
    }
  }

  .card-desc {
    display: block;
    font-size: 14px;
    color: #666;
    margin-bottom: 8px;
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;

    .tag {
      font-size: 12px;
      background: #f0f4ff;
      color: #4a90e2;
      padding: 2px 8px;
      border-radius: 6px;
    }

    .card-time {
      font-size: 12px;
      color: #bbb;
    }
  }

  .vote-bar {
    padding-top: 8px;
    border-top: 1px solid #f0f0f0;

    .vote-count {
      font-size: 14px;
      color: #e74c3c;
    }
  }
}
</style>
