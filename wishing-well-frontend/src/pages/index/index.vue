<template>
  <view class="page">
    <view class="header">
      <view class="header-top">
        <view class="header-text">
          <text class="title">{{ t('app.title') }}</text>
          <text class="subtitle">{{ t('app.subtitle') }}</text>
        </view>
        <text class="lang-btn" @tap="toggleLocale">{{ t('language') }}</text>
      </view>
    </view>

    <!-- 发布愿望 -->
    <view class="form">
      <input
        class="input"
        v-model="form.title"
        :placeholder="t('form.titlePlaceholder')"
        maxlength="50"
      />
      <textarea
        class="textarea"
        v-model="form.description"
        :placeholder="t('form.descPlaceholder')"
        maxlength="500"
      />
      <view class="row">
        <input class="input-small" v-model="form.category" :placeholder="t('form.categoryPlaceholder')" />
        <input class="input-small" v-model="form.contact" :placeholder="t('form.contactPlaceholder')" />
      </view>
      <button class="btn-primary" @tap="submitWish">{{ t('form.submitButton') }}</button>
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
import { t, toggleLocale } from "../../locales";

const form = ref({ title: "", description: "", category: "", contact: "" });
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

async function submitWish() {
  if (!form.value.title?.trim()) {
    Taro.showToast({ title: t('form.titleRequired'), icon: "none" });
    return;
  }
  try {
    await wishApi.create({ ...form.value });
    Taro.showToast({ title: t('form.submitSuccess'), icon: "success" });
    Object.assign(form.value, { title: "", description: "", category: "", contact: "" });
    fetchWishes();
  } catch (e) {
    console.error("提交失败:", e);
    Taro.showToast({ title: t('form.submitFailed'), icon: "none" });
  }
}

function formatTime(time) {
  return time ? time.slice(0, 10) : "";
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

.header {
  margin-bottom: 24px;

  .header-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .header-text {
    flex: 1;
  }

  .title {
    display: block;
    font-size: 28px;
    font-weight: bold;
    color: #333;
  }

  .subtitle {
    display: block;
    font-size: 14px;
    color: #999;
    margin-top: 4px;
  }

  .lang-btn {
    font-size: 14px;
    color: #4a90e2;
    padding: 4px 12px;
    border: 1px solid #4a90e2;
    border-radius: 14px;
  }
}

.form {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;

  .input {
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 15px;
    margin-bottom: 10px;
    width: 100%;
    box-sizing: border-box;
  }

  .textarea {
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 15px;
    margin-bottom: 10px;
    width: 100%;
    box-sizing: border-box;
    height: 80px;
    resize: none;
  }

  .row {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;

    .input-small {
      flex: 1;
      border: 1px solid #eee;
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 15px;
    }
  }

  .btn-primary {
    width: 100%;
    background: #4a90e2;
    color: #fff;
    border-radius: 8px;
    padding: 12px;
    font-size: 16px;
    border: none;
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
