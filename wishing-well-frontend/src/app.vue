<template>
  <view class="app" />
</template>

<script setup>
</script>

<style lang="scss">
/* 全局样式变量 - 微信小程序兼容 */
page {
  --color-primary: #4a90e2;
  --color-primary-dark: #3a7bc8;
  --color-bg: #f5f5f5;
  --color-card: #ffffff;
  --color-text: #333333;
  --color-text-secondary: #666666;
  --color-text-muted: #999999;
  --color-border: #eeeeee;
  --color-vote: #e74c3c;
  --color-vote-bg: #fff3f3;
  --color-success: #27ae60;
  --color-warning: #e67e22;
  --color-info: #2980b9;
  --color-danger: #c0392b;
  --color-status-pending-bg: #fff3e0;
  --color-status-approved-bg: #e8f5e9;
  --color-status-implementing-bg: #e3f2fd;
  --color-status-implemented-bg: #e8f5e9;
  --color-status-rejected-bg: #fce4ec;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --shadow-card: 0 2px 12px rgba(0, 0, 0, 0.08);
  --shadow-fab: 0 4px 16px rgba(74, 144, 226, 0.4);
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --font-xs: 15px;
  --font-sm: 17px;
  --font-md: 20px;
  --font-lg: 26px;
  --font-xl: 32px;
  --font-xxl: 40px;

  background: var(--color-bg);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

text {
  color: var(--color-text);
}
</style>