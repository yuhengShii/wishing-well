import type { UserConfig } from "@tarojs/cli";

const config: UserConfig = {
  projectName: "wishing-well",
  framework: "vue3",
  sourceRoot: "src",
  outputRoot: "dist",
  webpackChain(chain: any, webpack: any) {
    // Manually set loaderMeta for the miniPlugin to ensure Vue3 app initialization
    chain.plugin('miniPlugin').tap((args: any[]) => {
      args[0].loaderMeta = {
        importFrameworkStatement: `
import { h, createApp } from 'vue'
`,
        mockAppStatement: `
const App = createApp({})
`,
        frameworkArgs: 'h, config',
        creator: 'createVue3App',
        creatorLocation: '@tarojs/plugin-framework-vue3/dist/runtime',
        importFrameworkName: 'h',
        isNeedRawLoader: true,
        extraImportForWeb: '',
        execBeforeCreateWebApp: '',
      };
      return args;
    });
  },
};

export default config;
