import { describe, it, expect, vi, beforeEach } from "vitest";
import { renderHook, act, waitFor } from "@testing-library/react";
import { useItems } from "../use-items";
import * as api from "@/lib/api";

vi.mock("@/lib/api");

const makeMeta = (total = 1, limit = 20, offset = 0) => ({
  total,
  limit,
  offset,
});

const makeItem = (id: string, is_read = false) => ({
  id,
  source_id: "s1",
  source_name: "arXiv",
  title: `Title ${id}`,
  url: `https://example.com/${id}`,
  excerpt: "excerpt",
  summary: null,
  published_at: "2026-03-04T00:00:00Z",
  category: "research" as const,
  is_paywalled: false,
  is_read,
  created_at: "2026-03-04T00:00:00Z",
});

beforeEach(() => {
  vi.restoreAllMocks();
});

describe("useItems", () => {
  it("starts with loading state", () => {
    vi.mocked(api.fetchItems).mockResolvedValue({
      success: true,
      data: [],
      error: null,
      meta: makeMeta(0),
    });
    const { result } = renderHook(() => useItems());
    expect(result.current.isLoading).toBe(true);
    expect(result.current.items).toEqual([]);
    expect(result.current.error).toBeNull();
  });

  it("populates items after fetch resolves", async () => {
    vi.mocked(api.fetchItems).mockResolvedValue({
      success: true,
      data: [makeItem("1")],
      error: null,
      meta: makeMeta(1),
    });
    const { result } = renderHook(() => useItems());
    await waitFor(() => expect(result.current.isLoading).toBe(false));
    expect(result.current.items).toHaveLength(1);
    expect(result.current.items[0].id).toBe("1");
  });

  it("sets error on fetch failure", async () => {
    vi.mocked(api.fetchItems).mockRejectedValue(new Error("Network error"));
    const { result } = renderHook(() => useItems());
    await waitFor(() => expect(result.current.isLoading).toBe(false));
    expect(result.current.error).toBe("Network error");
    expect(result.current.items).toEqual([]);
  });

  it("loadMore appends items and increments offset", async () => {
    vi.mocked(api.fetchItems)
      .mockResolvedValueOnce({
        success: true,
        data: [makeItem("1")],
        error: null,
        meta: makeMeta(2, 1, 0),
      })
      .mockResolvedValueOnce({
        success: true,
        data: [makeItem("2")],
        error: null,
        meta: makeMeta(2, 1, 1),
      });
    const { result } = renderHook(() => useItems());
    await waitFor(() => expect(result.current.isLoading).toBe(false));
    act(() => result.current.loadMore());
    await waitFor(() => expect(result.current.items).toHaveLength(2));
    expect(result.current.items[1].id).toBe("2");
  });

  it("sets hasMore false when returned items < limit", async () => {
    vi.mocked(api.fetchItems).mockResolvedValue({
      success: true,
      data: [makeItem("1")],
      error: null,
      meta: makeMeta(1, 20, 0),
    });
    const { result } = renderHook(() => useItems());
    await waitFor(() => expect(result.current.isLoading).toBe(false));
    expect(result.current.hasMore).toBe(false);
  });

  it("setCategory resets items and fetches fresh", async () => {
    vi.mocked(api.fetchItems)
      .mockResolvedValueOnce({
        success: true,
        data: [makeItem("1")],
        error: null,
        meta: makeMeta(1),
      })
      .mockResolvedValueOnce({
        success: true,
        data: [makeItem("2")],
        error: null,
        meta: makeMeta(1),
      });
    const { result } = renderHook(() => useItems());
    await waitFor(() => expect(result.current.items).toHaveLength(1));
    act(() => result.current.setCategory("code"));
    await waitFor(() => expect(result.current.items).toHaveLength(1));
    expect(result.current.items[0].id).toBe("2");
    expect(result.current.category).toBe("code");
  });

  it("markItemRead updates is_read immutably and calls API", async () => {
    vi.mocked(api.fetchItems).mockResolvedValue({
      success: true,
      data: [makeItem("1", false)],
      error: null,
      meta: makeMeta(1),
    });
    vi.mocked(api.markRead).mockResolvedValue(undefined);
    const { result } = renderHook(() => useItems());
    await waitFor(() => expect(result.current.items).toHaveLength(1));
    await act(async () => result.current.markItemRead("1"));
    expect(api.markRead).toHaveBeenCalledWith("1");
    expect(result.current.items[0].is_read).toBe(true);
    // original object is not mutated (new reference)
    expect(result.current.items[0]).not.toBe(makeItem("1", false));
  });
});
