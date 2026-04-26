<template>
  <view class="page" :key="localeState.locale">
    <view class="header">
      <text class="title">{{ t('addWish.title') }}</text>
      <view class="header-right">
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
        <picker class="picker" mode="selector" :range="categories" :value="categoryIndex" @change="onCategoryChange">
          <view class="picker-text">{{ form.category || t('form.categoryPlaceholder') }}</view>
        </picker>
        <input class="input-small" v-model="form.contact" :placeholder="t('form.contactPlaceholder')" />
      </view>
      <button class="btn-primary" @tap="submitWish">{{ t('form.submitButton') }}</button>
      <button class="btn-secondary" @tap="goBack">{{ t('addWish.cancel') }}</button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Taro from "@tarojs/taro";
import { wishApi } from "../../api/wish";
import { t, localeState, toggleLocale } from "../../locales";

const categories = ["生活", "工作", "学习", "健康", "娱乐", "其他", "财务", "社交", "旅行", "科技", "家居", "技能", "情感", "美食", "运动", "公益"];
const categoryIndex = ref(0);

const form = ref({ title: "", description: "", category: "", contact: "" });

function onCategoryChange(e) {
  categoryIndex.value = e.detail.value;
  form.value.category = categories[e.detail.value];
}

async function submitWish() {
  if (!form.value.title?.trim()) {
    Taro.showToast({ title: t('form.titleRequired'), icon: "none" });
    return;
  }
  try {
    await wishApi.create({ ...form.value });
    Taro.showToast({ title: t('form.submitSuccess'), icon: "success" });
    // 清空表单
    form.value = { title: "", description: "", category: "", contact: "" };
    // 返回首页
    setTimeout(() => {
      Taro.switchTab({ url: '/pages/index/index' });
    }, 1500);
  } catch (e) {
    console.error("提交失败:", e);
    Taro.showToast({ title: t('form.submitFailed'), icon: "none" });
  }
}

function goBack() {
  Taro.switchTab({ url: '/pages/index/index' });
}

onMounted(() => {
  // nothing to init
});
</script>

<style lang="scss">
.page {
  padding: var(--spacing-lg) var(--spacing-md);
  background: var(--color-bg);
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);

  .title {
    font-size: var(--font-xl);
    font-weight: bold;
    color: var(--color-text);
  }

  .header-right {
    .lang-btn {
      font-size: var(--font-sm);
      color: var(--color-primary);
      padding: 4px 12px;
      border: 1px solid var(--color-primary);
      border-radius: var(--radius-md);
      background: var(--color-card);
    }
  }
}

.form {
  background: var(--color-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  padding: var(--spacing-md);

  .input {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: 10px 12px;
    font-size: var(--font-md);
    margin-bottom: var(--spacing-sm);
    width: 100%;
    box-sizing: border-box;
  }

  .textarea {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: 10px 12px;
    font-size: var(--font-md);
    margin-bottom: var(--spacing-sm);
    width: 100%;
    box-sizing: border-box;
    height: 120px;
    resize: none;
  }

  .row {
    display: flex;
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-sm);

    .picker {
      flex: 1;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-sm);
      padding: 10px 12px;
      font-size: var(--font-md);
      background: var(--color-card);

      .picker-text {
        color: var(--color-text-muted);
      }
    }

    .input-small {
      flex: 1;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-sm);
      padding: 10px 12px;
      font-size: var(--font-md);
    }
  }

  .btn-primary {
    width: 100%;
    background: var(--color-primary);
    color: #fff;
    border-radius: var(--radius-sm);
    padding: 12px;
    font-size: var(--font-lg);
    border: none;
    margin-bottom: var(--spacing-sm);

    &:active {
      background: var(--color-primary-dark);
    }
  }

  .btn-secondary {
    width: 100%;
    background: var(--color-card);
    color: var(--color-text-secondary);
    border-radius: var(--radius-sm);
    padding: 12px;
    font-size: var(--font-lg);
    border: 1px solid var(--color-border);
  }
}
</style>
