import Taro from "@tarojs/taro";
import { baseUrl } from "../constants";
import { getToken, setToken, removeToken } from "../utils/auth";

/** 微信登录，获取 token */
export function login(): Promise<{ token: string; openid: string; user_id: number }> {
  return new Promise((resolve, reject) => {
    // 1. 获取微信登录 code
    Taro.login({
      success: async (wxLoginRes) => {
        if (!wxLoginRes.code) {
          reject(new Error("获取微信 code 失败"));
          return;
        }

        // 2. 调用后端登录接口
        try {
          const res = await Taro.request({
            url: `${baseUrl}/auth/login?code=${wxLoginRes.code}`,
            method: "POST",
          });

          if (res.statusCode === 200 && res.data.token) {
            // 3. 存储 token
            setToken(res.data.token);
            resolve(res.data);
          } else {
            reject(new Error(res.data?.detail || "登录失败"));
          }
        } catch (e) {
          reject(e);
        }
      },
      fail: (err) => {
        reject(new Error("微信登录失败: " + err.errMsg));
      },
    });
  });
}

/** 登出 */
export function logout() {
  removeToken();
}

/** 检查是否已登录 */
export function isLoggedIn(): boolean {
  return !!getToken();
}
