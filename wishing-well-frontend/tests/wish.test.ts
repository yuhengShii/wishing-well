import { formatDate, truncate, debounce } from "../src/utils/format";

describe("formatDate", () => {
  it("应返回 YYYY-MM-DD 格式", () => {
    expect(formatDate("2026-04-24T10:30:00")).toBe("2026-04-24");
  });

  it("空字符串应返回空字符串", () => {
    expect(formatDate("")).toBe("");
  });
});

describe("truncate", () => {
  it("不超过最大长度时保持原样", () => {
    expect(truncate("你好", 10)).toBe("你好");
  });

  it("超出最大长度应截断并加省略号", () => {
    expect(truncate("你好世界", 3)).toBe("你好世…");
  });
});

describe("debounce", () => {
  jest.useFakeTimers();

  it("应在延迟后才执行函数", () => {
    const fn = jest.fn();
    const debounced = debounce(fn, 300);
    debounced();
    expect(fn).not.toHaveBeenCalled();
    jest.advanceTimersByTime(300);
    expect(fn).toHaveBeenCalledTimes(1);
  });

  it("应只执行最后一次调用", () => {
    const fn = jest.fn();
    const debounced = debounce(fn, 300);
    debounced();
    debounced();
    debounced();
    jest.advanceTimersByTime(300);
    expect(fn).toHaveBeenCalledTimes(1);
  });
});
