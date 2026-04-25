<template>
  <view class="page">
    <view class="header">
      <text class="title">{{ t('myWishes.title') }}</text>
    </view>

    <view class="list">
      <view v-if="myWishes.length === 0" class="empty">{{ t('myWishes.empty') }}</view>
      <view v-for="wish in myWishes" :key="wish.id" class="card">
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
import { ref, onMounted } from "vue";
import Taro, { useDidShow } from "@tarojs/taro";
import { wishApi } from "../../api/wish";
import { t, localeState } from "../../locales";

const myWishes = ref([]);

// 强制刷新页面
function refreshPage() {
  myWishes.value = [];
  fetchMyWishes();
}

async function fetchMyWishes() {
  try {
    const res = await wishApi.list({});
    myWishes.value = res.data;
  } catch (e) {
    Taro.showToast({ title: t('loadFailed'), icon: "none" });
  }
}

function formatTime(time) {
  return time ? time.slice(0, 10) : "";
}

onMounted(() => {
  fetchMyWishes();
});

// 每次页面显示时刷新（解决 tabBar 切换不重新渲染问题）
useDidShow(() => {
  // 引用 localeState 触发依赖
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
  margin-bottom: 24px;

  .title {
    font-size: 24px;
    font-weight: bold;
    color: #333;
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
