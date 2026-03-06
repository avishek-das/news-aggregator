import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  fetchSources,
  createSource,
  updateSource,
  retireSource,
  reactivateSource,
  deleteSource,
} from "../sources-api";
import type { Source } from "@/types/source";

const mockSource: Source = {
  id: "src-1",
  name: "arXiv cs.AI",
  url: "https://export.arxiv.org/rss/cs.AI",
  type: "rss",
  category: "research",
  priority: "high",
  status: "active",
  fetch_config: { adapter: "arxiv" },
  last_fetched_at: null,
  last_error: null,
  consecutive_failures: 0,
  updated_at: null,
  created_at: "2026-01-01T00:00:00Z",
};

beforeEach(() => {
  vi.restoreAllMocks();
});

describe("fetchSources", () => {
  it("calls GET /sources with credentials", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () => Promise.resolve({ success: true, data: [mockSource], error: null }),
      })
    );
    await fetchSources();
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/sources"),
      expect.objectContaining({ credentials: "include" })
    );
  });

  it("returns source array on success", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () => Promise.resolve({ success: true, data: [mockSource], error: null }),
      })
    );
    const result = await fetchSources();
    expect(result).toHaveLength(1);
    expect(result[0].name).toBe("arXiv cs.AI");
  });

  it("throws when success is false", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () => Promise.resolve({ success: false, data: [], error: "DB down" }),
      })
    );
    await expect(fetchSources()).rejects.toThrow("DB down");
  });
});

describe("createSource", () => {
  it("calls POST /sources with JSON body", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () => Promise.resolve({ success: true, data: mockSource, error: null }),
      })
    );
    await createSource({
      name: "arXiv cs.AI",
      url: "https://export.arxiv.org/rss/cs.AI",
      type: "rss",
      category: "research",
      priority: "high",
    });
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/sources"),
      expect.objectContaining({ method: "POST" })
    );
  });

  it("returns created source on success", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () => Promise.resolve({ success: true, data: mockSource, error: null }),
      })
    );
    const result = await createSource({
      name: "arXiv cs.AI",
      url: "https://example.com",
      type: "rss",
      category: "research",
      priority: "high",
    });
    expect(result.id).toBe("src-1");
  });

  it("throws when success is false", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () =>
          Promise.resolve({ success: false, data: null, error: "Validation error" }),
      })
    );
    await expect(
      createSource({ name: "", url: "", type: "rss", category: "research", priority: "high" })
    ).rejects.toThrow("Validation error");
  });
});

describe("updateSource", () => {
  it("calls PATCH /sources/{id}", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () =>
          Promise.resolve({ success: true, data: { ...mockSource, name: "Updated" }, error: null }),
      })
    );
    const result = await updateSource("src-1", { name: "Updated" });
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/sources/src-1"),
      expect.objectContaining({ method: "PATCH" })
    );
    expect(result.name).toBe("Updated");
  });
});

describe("retireSource", () => {
  it("calls POST /sources/{id}/retire", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () =>
          Promise.resolve({ success: true, data: { ...mockSource, status: "inactive" }, error: null }),
      })
    );
    const result = await retireSource("src-1");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/sources/src-1/retire"),
      expect.objectContaining({ method: "POST" })
    );
    expect(result.status).toBe("inactive");
  });
});

describe("reactivateSource", () => {
  it("calls POST /sources/{id}/reactivate", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () =>
          Promise.resolve({ success: true, data: mockSource, error: null }),
      })
    );
    await reactivateSource("src-1");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/sources/src-1/reactivate"),
      expect.objectContaining({ method: "POST" })
    );
  });
});

describe("deleteSource", () => {
  it("calls DELETE /sources/{id}", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: true, status: 204 })
    );
    await deleteSource("src-1");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/sources/src-1"),
      expect.objectContaining({ method: "DELETE" })
    );
  });

  it("throws on 409 with detail message", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 409,
        json: () => Promise.resolve({ detail: "Cannot delete source with existing items. Retire it instead." }),
      })
    );
    await expect(deleteSource("src-1")).rejects.toThrow("Cannot delete");
  });

  it("throws on generic non-ok response", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: false, status: 500 })
    );
    await expect(deleteSource("src-1")).rejects.toThrow("Delete failed: 500");
  });
});
