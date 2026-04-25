export default defineAppConfig({
  pages: [
    "pages/index/index",
    "pages/my-wishes/index",
    "pages/my-votes/index",
    "pages/categories/index",
    "pages/profile/index",
  ],
  window: {
    backgroundTextStyle: "light",
    navigationBarBackgroundColor: "#fff",
    navigationBarTitleText: "许愿池",
    navigationBarTextStyle: "black",
  },
  tabBar: {
    color: "#999",
    selectedColor: "#4a90e2",
    backgroundColor: "#fff",
    borderStyle: "black",
    list: [
      {
        pagePath: "pages/index/index",
        text: "首页",
      },
      {
        pagePath: "pages/my-wishes/index",
        text: "我的愿望",
      },
      {
        pagePath: "pages/my-votes/index",
        text: "我的投票",
      },
      {
        pagePath: "pages/categories/index",
        text: "分类",
      },
      {
        pagePath: "pages/profile/index",
        text: "我的",
      },
    ],
  },
})
