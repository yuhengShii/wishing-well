<template>
  <view class="app" />
</template>

<script setup>
</script>

<style lang="scss">
@import "./styles/tokens.scss";
@import "./styles/mixins.scss";

page {
  background: var(--color-bg);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* 全局文本样式 */
text {
  color: var(--color-text);
}
</style>