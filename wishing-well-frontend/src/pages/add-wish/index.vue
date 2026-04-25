<template>
  <view class="page" :key="localeState.locale">
    <view class="header">
      <text class="title">{{ t('addWish.title') }}</text>
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
      <button class="btn-secondary" @tap="goBack">{{ t('addWish.cancel') }}</button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Taro from "@tarojs/taro";
import { wishApi } from "../../api/wish";
import { t, localeState } from "../../locales";

const form = ref({ title: "", description: "", category: "", contact: "" });

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

.form {
  background: #fff;
  border-radius: 12px;
  padding: 16px;

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
    height: 120px;
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
    margin-bottom: 10px;
  }

  .btn-secondary {
    width: 100%;
    background: #fff;
    color: #666;
    border-radius: 8px;
    padding: 12px;
    font-size: 16px;
    border: 1px solid #ddd;
  }
}
</style>
