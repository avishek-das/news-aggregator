import { describe, it, expect, vi, beforeEach } from "vitest";
import { fetchItems, markRead } from "../api";

const mockItem = {
  id: "abc",
  source_id: "s1",
  source_name: "arXiv",
  title: "Test",
  url: "https://example.com",
  excerpt: "excerpt",
  summary: null,
  published_at: "2026-03-04T00:00:00Z",
  category: "research" as const,
  is_paywalled: false,
  is_read: false,
  created_at: "2026-03-04T00:00:00Z",
};

const mockResponse = {
  success: true,
  data: [mockItem],
  error: null,
  meta: { total: 1, limit: 20, offset: 0 },
};

beforeEach(() => {
  vi.restoreAllMocks();
});

describe("fetchItems", () => {
  it("calls the correct URL with no params", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      })
    );
    await fetchItems();
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/items"),
      expect.objectContaining({ credentials: "include" })
    );
  });

  it("appends category and pagination query params", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      })
    );
    await fetchItems({ category: "research", limit: 10, offset: 20 });
    const url = (fetch as ReturnType<typeof vi.fn>).mock.calls[0][0] as string;
    expect(url).toContain("category=research");
    expect(url).toContain("limit=10");
    expect(url).toContain("offset=20");
  });

  it("returns parsed ItemsListResponse on success", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      })
    );
    const result = await fetchItems();
    expect(result.data).toHaveLength(1);
    expect(result.data[0].title).toBe("Test");
    expect(result.meta.total).toBe(1);
  });

  it("throws when success is false", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: () =>
          Promise.resolve({ success: false, error: "DB error", data: [], meta: {} }),
      })
    );
    await expect(fetchItems()).rejects.toThrow("DB error");
  });

  it("throws on network error", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockRejectedValue(new Error("Network failed"))
    );
    await expect(fetchItems()).rejects.toThrow("Network failed");
  });
});

describe("markRead", () => {
  it("calls POST /items/{id}/read", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: true, status: 204 })
    );
    await markRead("abc");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/items/abc/read"),
      expect.objectContaining({ method: "POST", credentials: "include" })
    );
  });

  it("does not throw on 204", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: true, status: 204 })
    );
    await expect(markRead("abc")).resolves.toBeUndefined();
  });

  it("throws on non-2xx response", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: false, status: 500 })
    );
    await expect(markRead("abc")).rejects.toThrow();
  });
});
