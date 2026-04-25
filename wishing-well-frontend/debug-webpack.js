// Debug script to print webpack module rules
const path = require('path');

// Patch the taro webpack5-runner to print rules
const originalRequire = require;
const Module = require('module');
const originalLoad = Module._load;
Module._load = function(request, parent) {
  const result = originalLoad.apply(this, arguments);
  return result;
};

// Just print the webpack module setup
const WebpackModule = require('/mnt/d/proj/wishing-well/wishing-well-frontend/node_modules/@tarojs/webpack5-runner/dist/webpack/WebpackModule');
console.log('getScriptRule:', WebpackModule.WebpackModule.getScriptRule.toString().slice(0, 200));
