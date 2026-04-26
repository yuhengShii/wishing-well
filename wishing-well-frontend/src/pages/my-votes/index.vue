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
  padding: var(--spacing-lg) var(--spacing-md);
  background: var(--color-bg);
  min-height: 100vh;
}

.header {
  margin-bottom: var(--spacing-lg);

  .title {
    font-size: var(--font-xl);
    font-weight: bold;
    color: var(--color-text);
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

.login-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;

  .login-text {
    font-size: var(--font-md);
    color: var(--color-text-secondary);
    margin-bottom: var(--spacing-md);
  }

  .login-btn {
    background: var(--color-primary);
    color: #fff;
    font-size: var(--font-sm);
    padding: 12px 32px;
    border-radius: var(--radius-sm);
    border: none;

    &:active {
      background: var(--color-primary-dark);
    }
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

    .voted-badge {
      font-size: var(--font-sm);
      color: var(--color-danger);
    }
  }
}
</style>
