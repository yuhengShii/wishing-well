<template>
  <view class="page" :key="localeState.locale">
    <!-- 浮动添加按钮 -->
    <view class="fab" @tap="goToAddWish">
      <text class="fab-text">+</text>
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
import { t, localeState } from "../../locales";

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

.fab {
  position: fixed;
  right: 24px;
  bottom: 120px;
  width: 56px;
  height: 56px;
  border-radius: 28px;
  background: #4a90e2;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.4);

  .fab-text {
    font-size: 32px;
    color: #fff;
    font-weight: 300;
  }
}

.sort-bar {
  display: flex;
  align-items: center;
  margin-bottom: 12px;

  .sort-label {
    font-size: 14px;
    color: #666;
    margin-right: 8px;
  }

  .sort-tabs {
    display: flex;
    gap: 8px;
  }

  .sort-tab {
    font-size: 14px;
    color: #999;
    padding: 4px 12px;
    border-radius: 14px;
    background: #e8e8e8;

    &.active {
      background: #4a90e2;
      color: #fff;
    }
  }
}

.list {
  .list-title {
    font-size: 18px;
    font-weight: bold;
    color: #333;
    margin-bottom: 12px;
    display: block;
  }

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
    display: flex;
    align-items: center;
    gap: 8px;
    padding-top: 8px;
    border-top: 1px solid #f0f0f0;

    .vote-btn {
      font-size: 14px;
      padding: 4px 14px;
      border-radius: 16px;
      background: #fff3f3;
      color: #e74c3c;
      border: 1px solid #fdd;
      line-height: 1.6;

      &.voted {
        background: #fdeaea;
        color: #c0392b;
      }
    }

    .vote-hint {
      font-size: 12px;
      color: #bbb;
    }
  }
}
</style>
