import { reactive } from 'vue'
import Taro from '@tarojs/taro'

const STORAGE_KEY = 'wishing-well-lang'

const messages = {
  zh: {
    app: {
      title: '许愿池',
      subtitle: '让每一个愿望被看见',
    },
    form: {
      titlePlaceholder: '愿望标题（必填）',
      descPlaceholder: '详细描述你的愿望...',
      categoryPlaceholder: '分类',
      contactPlaceholder: '联系方式（可选）',
      submitButton: '提交愿望',
      titleRequired: '请输入标题',
      submitSuccess: '提交成功',
      submitFailed: '提交失败',
    },
    sort: {
      label: '排序：',
      latest: '最新',
      hottest: '最热',
    },
    list: {
      title: '愿望列表',
      empty: '暂无愿望，来写下第一个吧',
    },
    status: {
      pending: '待审核',
      approved: '已采纳',
      implemented: '已实现',
      rejected: '已拒绝',
    },
    vote: {
      support: '支持一下',
      supported: '已支持',
      alreadyVoted: '已经投过票了',
      failed: '操作失败',
    },
    loadFailed: '加载失败，请检查后端',
    language: 'EN',
    addWish: {
      title: '发布愿望',
      cancel: '取消',
    },
    myWishes: {
      title: '我的愿望',
      empty: '您还没有提交过愿望',
    },
    myVotes: {
      title: '我的投票',
      empty: '您还没有支持过任何愿望',
    },
    categories: {
      title: '分类浏览',
      empty: '该分类下暂无愿望',
    },
    profile: {
      title: '我的',
      guest: '游客',
      myWishesCount: '我的愿望',
      myVotesCount: '我的投票',
      language: '语言',
    },
    auth: {
      loginRequired: '请先登录后操作',
      loginBtn: '微信登录',
      logining: '登录中...',
      loginFailed: '登录失败',
      loginSuccess: '登录成功',
    },
  },
  en: {
    app: {
      title: 'Wishing Well',
      subtitle: 'Let every wish be seen',
    },
    form: {
      titlePlaceholder: 'Wish title (required)',
      descPlaceholder: 'Describe your wish in detail...',
      categoryPlaceholder: 'Category',
      contactPlaceholder: 'Contact (optional)',
      submitButton: 'Submit Wish',
      titleRequired: 'Please enter a title',
      submitSuccess: 'Submitted successfully',
      submitFailed: 'Submission failed',
    },
    sort: {
      label: 'Sort:',
      latest: 'Latest',
      hottest: 'Hottest',
    },
    list: {
      title: 'Wish List',
      empty: 'No wishes yet, be the first to submit!',
    },
    status: {
      pending: 'Pending',
      approved: 'Approved',
      implemented: 'Implemented',
      rejected: 'Rejected',
    },
    vote: {
      support: 'Support',
      supported: 'Supported',
      alreadyVoted: 'Already voted',
      failed: 'Operation failed',
    },
    loadFailed: 'Failed to load, please check backend',
    language: '中文',
    addWish: {
      title: 'Submit Wish',
      cancel: 'Cancel',
    },
    myWishes: {
      title: 'My Wishes',
      empty: 'You have not submitted any wishes yet',
    },
    myVotes: {
      title: 'My Votes',
      empty: 'You have not supported any wishes yet',
    },
    categories: {
      title: 'Categories',
      empty: 'No wishes in this category',
    },
    profile: {
      title: 'Profile',
      guest: 'Guest',
      myWishesCount: 'My Wishes',
      myVotesCount: 'My Votes',
      language: 'Language',
    },
    auth: {
      loginRequired: 'Please login first',
      loginBtn: 'WeChat Login',
      logining: 'Logging in...',
      loginFailed: 'Login failed',
      loginSuccess: 'Login successful',
    },
  },
}

// 全局语言状态
export const localeState = reactive({
  locale: 'zh',
})

// 获取保存的语言
const saved = Taro.getStorageSync(STORAGE_KEY)
if (saved === 'en' || saved === 'zh') {
  localeState.locale = saved
}

// 切换语言
export function toggleLocale() {
  localeState.locale = localeState.locale === 'zh' ? 'en' : 'zh'
  Taro.setStorageSync(STORAGE_KEY, localeState.locale)
}

// 翻译函数
export function t(key) {
  const keys = key.split('.')
  let result = messages[localeState.locale]
  for (const k of keys) {
    result = result?.[k]
  }
  return result || key
}
