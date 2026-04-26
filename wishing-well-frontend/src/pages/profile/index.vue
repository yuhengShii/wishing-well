<template>
  <view class="page">
    <view class="header">
      <text class="title">{{ t('profile.title') }}</text>
    </view>

    <!-- 用户信息卡片 -->
    <view class="user-card">
      <view class="avatar">
        <text class="avatar-text">{{ userInfo.avatarText }}</text>
      </view>
      <view class="user-info">
        <text class="nickname">{{ userInfo.nickname || t('profile.guest') }}</text>
        <text class="user-id" v-if="userInfo.openid">ID: {{ userInfo.openid.slice(0, 8) }}...</text>
      </view>
    </view>

    <!-- 统计数据 -->
    <view class="stats">
      <view class="stat-item">
        <text class="stat-value">{{ stats.wishCount }}</text>
        <text class="stat-label">{{ t('profile.myWishesCount') }}</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ stats.voteCount }}</text>
        <text class="stat-label">{{ t('profile.myVotesCount') }}</text>
      </view>
    </view>

    <!-- 设置列表 -->
    <view class="settings">
      <view class="setting-item" @tap="toggleLocale">
        <text class="setting-label">{{ t('profile.language') }}</text>
        <text class="setting-value">{{ localeState.locale === 'zh' ? '中文' : 'English' }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import Taro, { useDidShow } from "@tarojs/taro";
import { t, toggleLocale, localeState } from "../../locales";

const userInfo = reactive({
  nickname: "",
  openid: "",
  avatarText: "?",
});

const stats = reactive({
  wishCount: 0,
  voteCount: 0,
});

function refreshPage() {
  // 强制触发 UI 更新
  userInfo.avatarText = localeState.locale === 'zh' ? '游' : 'G';
}

onMounted(() => {
  userInfo.avatarText = localeState.locale === 'zh' ? '游' : 'G';
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
  margin-bottom: 24px;

  .title {
    font-size: 36px;
    font-weight: bold;
    color: #333;
  }
}

.user-card {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;

  .avatar {
    width: 60px;
    height: 60px;
    border-radius: 30px;
    background: #4a90e2;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 16px;

    .avatar-text {
      font-size: 36px;
      color: #fff;
    }
  }

  .user-info {
    flex: 1;

    .nickname {
      display: block;
      font-size: 26px;
      font-weight: 600;
      color: #333;
      margin-bottom: 4px;
    }

    .user-id {
      font-size: 26px;
      color: #999;
    }
  }
}

.stats {
  display: flex;
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;

  .stat-item {
    flex: 1;
    text-align: center;

    .stat-value {
      display: block;
      font-size: 36px;
      font-weight: bold;
      color: #4a90e2;
      margin-bottom: 4px;
    }

    .stat-label {
      font-size: 26px;
      color: #999;
    }
  }
}

.settings {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;

  .setting-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid #f0f0f0;

    &:last-child {
      border-bottom: none;
    }

    .setting-label {
      font-size: 26px;
      color: #333;
    }

    .setting-value {
      font-size: 20px;
      color: #999;
    }
  }
}
</style>
