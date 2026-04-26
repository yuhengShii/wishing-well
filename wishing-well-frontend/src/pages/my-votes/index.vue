<template>
  <view class="page">
    <view class="header">
      <text class="title">{{ t('myVotes.title') }}</text>
    </view>

    <!-- 未登录提示 -->
    <view v-if="!authState.isLoggedIn" class="login-prompt">
      <text class="login-text">{{ t('auth.loginRequired') }}</text>
      <button class="login-btn" @tap="goToLogin">{{ t('auth.loginBtn') }}</button>
    </view>

    <!-- 投票列表 -->
    <view v-else class="list">
      <view v-if="votedWishes.length === 0" class="empty">{{ t('myVotes.empty') }}</view>
      <view v-for="wish in votedWishes" :key="wish.id" class="card">
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
          <text class="voted-badge">已支持 ❤️ {{ wish.vote_count }}</text>
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
import { initAuthState, authState, login } from "../../stores/auth";

const votedWishes = ref([]);

async function goToLogin() {
  await login();
  if (authState.isLoggedIn) {
    refreshPage();
  }
}

function refreshPage() {
  if (authState.isLoggedIn) {
    votedWishes.value = [];
    fetchVotedWishes();
  }
}

async function fetchVotedWishes() {
  try {
    const res = await wishApi.list({});
    votedWishes.value = res.data.filter(w => w.vote_count > 0);
  } catch (e) {
    Taro.showToast({ title: t('loadFailed'), icon: "none" });
  }
}

function formatTime(time) {
  return time ? time.slice(0, 10) : "";
}

onMounted(() => {
  initAuthState();
  refreshPage();
});

useDidShow(() => {
  initAuthState();
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
    font-size: 36px;
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

.login-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;

  .login-text {
    font-size: 20px;
    color: #666;
    margin-bottom: 20px;
  }

  .login-btn {
    background: #4a90e2;
    color: #fff;
    font-size: 18px;
    padding: 12px 32px;
    border-radius: 8px;
    border: none;
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
      font-size: 26px;
      font-weight: 600;
      color: #333;
    }

    .card-status {
      font-size: 26px;
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
    font-size: 20px;
    color: #666;
    margin-bottom: 8px;
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;

    .tag {
      font-size: 26px;
      background: #f0f4ff;
      color: #4a90e2;
      padding: 2px 8px;
      border-radius: 6px;
    }

    .card-time {
      font-size: 26px;
      color: #bbb;
    }
  }

  .vote-bar {
    padding-top: 8px;
    border-top: 1px solid #f0f0f0;

    .voted-badge {
      font-size: 20px;
      color: #c0392b;
    }
  }
}
</style>
