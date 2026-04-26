import { reactive } from "vue";
import { login as loginApi, logout as logoutApi } from "../api/auth";
import { getToken, getUserInfo, setUserInfo, removeToken } from "../utils/auth";
import Taro from "@tarojs/taro";
import { t } from "../locales";

/** 登录状态管理 */
export const authState = reactive({
  isLoggedIn: false,
  userId: null,
  openid: null,
});

/** 初始化登录状态（从本地存储恢复） */
export function initAuthState() {
  const token = getToken();
  const userInfo = getUserInfo();
  authState.isLoggedIn = !!token;
  authState.userId = userInfo.userId || null;
  authState.openid = userInfo.openid || null;
}

/** 登录 */
export async function login(): Promise<boolean> {
  try {
    Taro.showLoading({ title: t("auth.logining") });
    const data = await loginApi();
    authState.isLoggedIn = true;
    authState.userId = data.user_id;
    authState.openid = data.openid;
    setUserInfo(data.user_id, data.openid);
    Taro.hideLoading();
    Taro.showToast({ title: t("auth.loginSuccess"), icon: "success" });
    return true;
  } catch (e: any) {
    Taro.hideLoading();
    Taro.showToast({ title: e.message || t("auth.loginFailed"), icon: "none" });
    return false;
  }
}

/** 登出 */
export function logout() {
  logoutApi();
  authState.isLoggedIn = false;
  authState.userId = null;
  authState.openid = null;
}

/** 检查是否已登录，未登录则提示 */
export function requireLogin(): boolean {
  if (!authState.isLoggedIn) {
    Taro.showModal({
      title: t("auth.loginRequired"),
      confirmText: t("auth.logining"),
      success: (res) => {
        if (res.confirm) {
          login();
        }
      },
    });
    return false;
  }
  return true;
}
