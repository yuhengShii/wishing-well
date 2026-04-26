<template>
  <view class="page" :key="localeState.locale">
    <!-- 浮动按钮 -->
    <view class="fab" @tap="goToAddWish">
      <text class="fab-text">+</text>
    </view>
    <view class="lang-btn-fixed" @tap="toggleLocale">
      <text>{{ t('language') }}</text>
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

const wishes = ref([]);
const sort = ref("latest");
const votedMap = reactive({});

async function fetchWishes() {
  try {
    const res = await wishApi.list({ sort: sort.value });
    wishes.value = res.data;
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
  fetchWishes();
});
</script>

<style lang="scss">
.page {
  padding: 24px 16px;
  background: #f5f5f5;
  min-height: 100vh;
}

.lang-btn-fixed {
  position: fixed;
  top: 24px;
  right: 16px;
  font-size: 19px;
  color: #4a90e2;
  padding: 6px 14px;
  border: 1px solid #4a90e2;
  border-radius: 14px;
  z-index: 100;
}

.fab {
  position: fixed;
  right: 20px;
  bottom: 80px;
  width: 54px;
  height: 54px;
  border-radius: 27px;
  background: #4a90e2;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.4);

  .fab-text {
    font-size: 36px;
    color: #fff;
    font-weight: 300;
  }
}

.sort-bar {
  display: flex;
  align-items: center;
  margin-bottom: 16px;

  .sort-label {
    font-size: 19px;
    color: #555;
    margin-right: 10px;
  }

  .sort-tabs {
    display: flex;
    gap: 10px;
  }

  .sort-tab {
    font-size: 20px;
    color: #888;
    padding: 6px 16px;
    border-radius: 16px;
    background: #e8e8e8;

    &.active {
      background: #4a90e2;
      color: #fff;
    }
  }
}

.list {
  .list-title {
    font-size: 26px;
    font-weight: bold;
    color: #333;
    margin-bottom: 16px;
    display: block;
  }

  .empty {
    text-align: center;
    color: #999;
    font-size: 20px;
    padding: 80px 0;
  }
}

.card {
  background: #fff;
  border-radius: 12px;
  padding: 18px;
  margin-bottom: 14px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;

    .card-title {
      font-size: 26px;
      font-weight: 600;
      color: #333;
    }

    .card-status {
      font-size: 26px;
      padding: 3px 10px;
      border-radius: 10px;

      &.status-pending { background: #fff3e0; color: #e67e22; }
      &.status-approved { background: #e8f5e9; color: #27ae60; }
      &.status-implemented { background: #e3f2fd; color: #2980b9; }
      &.status-rejected { background: #fce4ec; color: #c0392b; }
    }
  }

  .card-desc {
    display: block;
    font-size: 19px;
    color: #555;
    margin-bottom: 12px;
    line-height: 1.5;
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;

    .tag {
      font-size: 19px;
      background: #f0f4ff;
      color: #4a90e2;
      padding: 3px 12px;
      border-radius: 12px;
    }

    .card-time {
      font-size: 19px;
      color: #999;
    }
  }

  .vote-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    padding-top: 12px;
    border-top: 1px solid #f0f0f0;

    .vote-btn {
      font-size: 26px;
      padding: 6px 16px;
      border-radius: 18px;
      background: #fff3f3;
      color: #e74c3c;
      border: 1px solid #fdd;
      line-height: 1.5;

      &.voted {
        background: #fdeaea;
        color: #c0392b;
      }
    }

    .vote-hint {
      font-size: 19px;
      color: #aaa;
    }
  }
}
</style>
