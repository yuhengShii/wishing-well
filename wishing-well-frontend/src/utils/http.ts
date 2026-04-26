import Taro from "@tarojs/taro";
import { baseUrl } from "../constants";
import { getToken } from "./auth";

interface RequestOptions {
  url: string;
  method?: "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
  data?: any;
  header?: Record<string, string>;
}

/** 统一的请求封装，自动附加 token */
export function request(options: RequestOptions) {
  const token = getToken();
  const header: Record<string, string> = {
    "Content-Type": "application/json",
    ...options.header,
  };

  // 如果有 token，附加到请求头
  if (token) {
    header["Authorization"] = `Bearer ${token}`;
  }

  // 如果 url 不是完整路径，拼上 baseUrl
  const fullUrl = options.url.startsWith("http")
    ? options.url
    : `${baseUrl}${options.url}`;

  return Taro.request({
    url: fullUrl,
    method: options.method || "GET",
    data: options.data,
    header,
  });
}
