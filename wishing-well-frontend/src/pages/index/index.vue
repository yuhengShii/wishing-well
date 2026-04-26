<template>
  <view class="page" :key="localeState.locale">
    <!-- 浮动按钮 -->
    <view class="fab" @tap="goToAddWish">
      <text class="fab-text">+</text>
    </view>
    <view class="lang-btn-fixed" @tap="toggleLocale">
      <text>{{ t('language') }}</text>
    </view>

    <!-- 统计 Banner -->
    <view class="banner">
      <view class="banner-item">
        <text class="banner-num">{{ totalWishes }}</text>
        <text class="banner-label">愿望总数</text>
      </view>
      <view class="banner-divider" />
      <view class="banner-item">
        <text class="banner-num">{{ totalVotes }}</text>
        <text class="banner-label">总投票数</text>
      </view>
    </view>

    <!-- 排序切换 -->
    <view class="sort-bar">
      <text class="sort-label">{{ t('sort.label') }}</text>
      <view class="sort-tabs">
        <text
          class="sort-tab"
          :class="{ active: sort === 'latest' }"
          @tap="switchSort('latest')"
        >{{ t('sort.latest') }}</text>
        <text
          class="sort-tab"
          :class="{ active: sort === 'votes' }"
          @tap="switchSort('votes')"
        >{{ t('sort.hottest') }}</text>
      </view>
    </view>

    <!-- 愿望列表 -->
    <view class="list">
      <text class="list-title">{{ t('list.title') }}</text>
      <view v-if="wishes.length === 0" class="empty">{{ t('list.empty') }}</view>
      <view v-for="wish in wishes" :key="wish.id" class="card">
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
        <!-- 投票区 -->
        <view class="vote-bar">
          <button
            class="vote-btn"
            :class="{ voted: votedMap[wish.id] }"
            @tap="toggleVote(wish)"
          >
            ❤️ {{ wish.vote_count }}
          </button>
          <text class="vote-hint">{{ votedMap[wish.id] ? t('vote.supported') : t('vote.support') }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import Taro from "@tarojs/taro";
import { wishApi } from "../../api/wish";
import { t, localeState, toggleLocale } from "../../locales";
import { initAuthState, requireLogin } from "../../stores/auth";

const wishes = ref([]);
const sort = ref("latest");
const votedMap = reactive({});
const totalWishes = ref(0);
const totalVotes = ref(0);

async function fetchWishes() {
  try {
    const res = await wishApi.list({ sort: sort.value });
    wishes.value = res.data;
    // 计算统计数据
    totalWishes.value = res.data.length;
    totalVotes.value = res.data.reduce((sum, w) => sum + (w.vote_count || 0), 0);
    for (const wish of wishes.value) {
      checkVotedStatus(wish.id);
    }
  } catch (e) {
    Taro.showToast({ title: t('loadFailed'), icon: "none" });
  }
}

async function checkVotedStatus(id) {
  try {
    const res = await wishApi.checkVoted(id);
    votedMap[id] = res.data.voted;
  } catch {
    // 忽略查询失败
  }
}

async function toggleVote(wish) {
  // 检查登录状态
  if (!requireLogin()) {
    return;
  }

  try {
    if (votedMap[wish.id]) {
      const res = await wishApi.unvote(wish.id);
      wish.vote_count = res.data.vote_count;
      votedMap[wish.id] = false;
    } else {
      const res = await wishApi.vote(wish.id);
      wish.vote_count = res.data.vote_count;
      votedMap[wish.id] = true;
    }
  } catch (e) {
    const msg = e?.errMsg || "";
    if (msg.includes("已经投过票") || msg.includes("already voted")) {
      Taro.showToast({ title: t('vote.alreadyVoted'), icon: "none" });
    } else {
      Taro.showToast({ title: t('vote.failed'), icon: "none" });
    }
  }
}

function switchSort(newSort) {
  sort.value = newSort;
  fetchWishes();
}

function formatTime(time) {
  return time ? time.slice(0, 10) : "";
}

function goToAddWish() {
  Taro.navigateTo({ url: '/pages/add-wish/index' });
}

onMounted(() => {
  initAuthState();
  fetchWishes();
});
</script>

<style lang="scss">
.page {
  padding: var(--spacing-lg) var(--spacing-md);
  background: var(--color-bg);
  min-height: 100vh;
}

.lang-btn-fixed {
  position: fixed;
  top: var(--spacing-lg);
  right: var(--spacing-md);
  font-size: var(--font-sm);
  color: var(--color-primary);
  padding: 6px 14px;
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-lg);
  z-index: 100;
  background: var(--color-card);
}

.banner {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg) var(--spacing-md);
  margin-bottom: var(--spacing-md);
  box-shadow: var(--shadow-card);

  .banner-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;

    .banner-num {
      font-size: var(--font-xxl);
      font-weight: bold;
      color: #fff;
    }

    .banner-label {
      font-size: var(--font-sm);
      color: rgba(255, 255, 255, 0.85);
      margin-top: 4px;
    }
  }

  .banner-divider {
    width: 1px;
    height: 40px;
    background: rgba(255, 255, 255, 0.3);
    margin: 0 var(--spacing-md);
  }
}

.fab {
  position: fixed;
  right: 20px;
  bottom: 80px;
  width: 54px;
  height: 54px;
  border-radius: 27px;
  background: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-fab);

  .fab-text {
    font-size: 36px;
    color: #fff;
    font-weight: 300;
  }
}

.sort-bar {
  display: flex;
  align-items: center;
  margin-bottom: var(--spacing-md);

  .sort-label {
    font-size: var(--font-sm);
    color: var(--color-text-secondary);
    margin-right: var(--spacing-sm);
  }

  .sort-tabs {
    display: flex;
    gap: var(--spacing-sm);
  }

  .sort-tab {
    font-size: var(--font-md);
    color: var(--color-text-muted);
    padding: 6px 16px;
    border-radius: var(--radius-lg);
    background: var(--color-card);

    &.active {
      background: var(--color-primary);
      color: #fff;
    }
  }
}

.list {
  .list-title {
    font-size: var(--font-lg);
    font-weight: bold;
    color: var(--color-text);
    margin-bottom: var(--spacing-md);
    display: block;
  }

  .empty {
    text-align: center;
    color: var(--color-text-muted);
    font-size: var(--font-md);
    padding: 80px 0;
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
    margin-bottom: var(--spacing-sm);

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
    line-height: 1.5;
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
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding-top: var(--spacing-sm);
    border-top: 1px solid var(--color-border);

    .vote-btn {
      font-size: var(--font-md);
      padding: 6px 16px;
      border-radius: var(--radius-lg);
      background: var(--color-vote-bg);
      color: var(--color-vote);
      border: 1px solid #fdd;
      line-height: 1.5;

      &.voted {
        background: #fdeaea;
        color: var(--color-danger);
      }
    }

    .vote-hint {
      font-size: var(--font-sm);
      color: var(--color-text-muted);
    }
  }
}
</style>
