import Taro from "@tarojs/taro";

const TOKEN_KEY = "auth_token";

/** 获取本地存储的 token */
export function getToken(): string | null {
  return Taro.getStorageSync(TOKEN_KEY);
}

/** 存储 token */
export function setToken(token: string): void {
  Taro.setStorageSync(TOKEN_KEY, token);
}

/** 删除 token */
export function removeToken(): void {
  Taro.removeStorageSync(TOKEN_KEY);
}

/** 读取用户信息 */
export function getUserInfo(): { userId?: number; openid?: string } {
  const userId = Taro.getStorageSync("user_id");
  const openid = Taro.getStorageSync("openid");
  return { userId, openid };
}

/** 存储用户信息 */
export function setUserInfo(userId: number, openid: string): void {
  Taro.setStorageSync("user_id", userId);
  Taro.setStorageSync("openid", openid);
}
