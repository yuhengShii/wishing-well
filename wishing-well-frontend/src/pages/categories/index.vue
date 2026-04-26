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
  padding: var(--spacing-lg) var(--spacing-md);
  background: var(--color-bg);
  min-height: 100vh;
}

.header {
  margin-bottom: var(--spacing-md);

  .title {
    font-size: var(--font-xl);
    font-weight: bold;
    color: var(--color-text);
  }
}

.category-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);

  .category-tab {
    font-size: var(--font-sm);
    color: var(--color-text-secondary);
    padding: 6px 14px;
    border-radius: var(--radius-lg);
    background: var(--color-card);

    &.active {
      background: var(--color-primary);
      color: #fff;
    }
  }
}

.list {
  .empty {
    text-align: center;
    color: var(--color-text-muted);
    font-size: var(--font-md);
    padding: 40px 0;
  }
}

.card {
  background: var(--color-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-sm);

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-xs);

    .card-title {
      font-size: var(--font-lg);
      font-weight: 600;
      color: var(--color-text);
      flex: 1;
      margin-right: var(--spacing-sm);
    }

    .card-status {
      font-size: var(--font-xs);
      padding: 4px 12px;
      border-radius: 10px;
      white-space: nowrap;

      &.status-pending { background: var(--color-status-pending-bg); color: var(--color-warning); }
      &.status-approved { background: var(--color-status-approved-bg); color: var(--color-success); }
      &.status-implementing { background: var(--color-status-implementing-bg); color: var(--color-info); }
      &.status-implemented { background: var(--color-status-implemented-bg); color: var(--color-success); }
      &.status-rejected { background: var(--color-status-rejected-bg); color: var(--color-danger); }
    }
  }

  .card-desc {
    display: block;
    font-size: var(--font-sm);
    color: var(--color-text-secondary);
    margin-bottom: var(--spacing-sm);
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-sm);

    .tag {
      font-size: var(--font-xs);
      background: #f0f4ff;
      color: var(--color-primary);
      padding: var(--spacing-xs) var(--spacing-sm);
      border-radius: var(--radius-sm);
    }

    .card-time {
      font-size: var(--font-xs);
      color: var(--color-text-muted);
    }
  }

  .vote-bar {
    padding-top: var(--spacing-sm);
    border-top: 1px solid var(--color-border);

    .vote-count {
      font-size: var(--font-sm);
      color: var(--color-vote);
    }
  }
}
</style>
