import { request } from "../utils/http";

/** 封装所有愿望相关的 API 调用，便于统一管理 */
export const wishApi = {
  /** 获取愿望列表 */
  list(filters) {
    const params = new URLSearchParams();
    if (filters && filters.category) params.set("category", filters.category);
    if (filters && filters.status) params.set("status", filters.status);
    if (filters && filters.sort) params.set("sort", filters.sort);
    const query = params.toString();

    return request({
      url: `/wishes${query ? "?" + query : ""}`,
    });
  },

  /** 获取单个愿望 */
  get(id) {
    return request({ url: `/wishes/${id}` });
  },

  /** 创建愿望 */
  create(data) {
    return request({
      url: "/wishes/",
      method: "POST",
      data,
    });
  },

  /** 更新愿望 */
  update(id, data) {
    return request({
      url: `/wishes/${id}`,
      method: "PUT",
      data,
    });
  },

  /** 删除愿望 */
  delete(id) {
    return request({ url: `/wishes/${id}`, method: "DELETE" });
  },

  /** 投票 */
  vote(id) {
    return request({
      url: `/wishes/${id}/vote`,
      method: "POST",
    });
  },

  /** 取消投票 */
  unvote(id) {
    return request({
      url: `/wishes/${id}/vote`,
      method: "DELETE",
    });
  },

  /** 查询投票状态 */
  checkVoted(id) {
    return request({ url: `/wishes/${id}/voted` });
  },
};
