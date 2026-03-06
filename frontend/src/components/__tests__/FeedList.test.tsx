import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { FeedList } from "../FeedList";
import * as useItemsModule from "@/hooks/use-items";
import type { FeedItem } from "@/types/item";

vi.mock("@/hooks/use-items");
// Stub IntersectionObserver — must be a real constructor for `new` to work
const mockObserve = vi.fn();
const mockDisconnect = vi.fn();
class MockIntersectionObserver {
  observe = mockObserve;
  disconnect = mockDisconnect;
  // eslint-disable-next-line @typescript-eslint/no-useless-constructor
  constructor(_callback: IntersectionObserverCallback) {}
}
vi.stubGlobal("IntersectionObserver", MockIntersectionObserver);

const makeItem = (id: string): FeedItem => ({
  id,
  source_id: "s1",
  source_name: "arXiv",
  title: `Item ${id}`,
  url: `https://example.com/${id}`,
  excerpt: "excerpt",
  summary: null,
  published_at: "2026-03-04T00:00:00Z",
  category: "research",
  is_paywalled: false,
  is_read: false,
  created_at: "2026-03-04T00:00:00Z",
});

const baseHook = {
  items: [],
  isLoading: false,
  error: null,
  hasMore: false,
  category: undefined,
  setCategory: vi.fn(),
  loadMore: vi.fn(),
  markItemRead: vi.fn(),
};

beforeEach(() => {
  vi.restoreAllMocks();
  vi.stubGlobal("IntersectionObserver", MockIntersectionObserver);
});

describe("FeedList", () => {
  it("renders skeleton cards when loading", () => {
    vi.mocked(useItemsModule.useItems).mockReturnValue({
      ...baseHook,
      isLoading: true,
    });
    const { container } = render(<FeedList />);
    const busy = container.querySelectorAll("[aria-busy='true']");
    expect(busy.length).toBeGreaterThanOrEqual(3);
  });

  it("renders error message when error is set", () => {
    vi.mocked(useItemsModule.useItems).mockReturnValue({
      ...baseHook,
      error: "Network error",
    });
    render(<FeedList />);
    expect(screen.getByText(/Network error/i)).toBeInTheDocument();
  });

  it("renders empty state when no items and not loading", () => {
    vi.mocked(useItemsModule.useItems).mockReturnValue(baseHook);
    render(<FeedList />);
    expect(screen.getByText(/no items/i)).toBeInTheDocument();
  });

  it("renders item cards for each item", () => {
    vi.mocked(useItemsModule.useItems).mockReturnValue({
      ...baseHook,
      items: [makeItem("1"), makeItem("2")],
    });
    render(<FeedList />);
    expect(screen.getByText("Item 1")).toBeInTheDocument();
    expect(screen.getByText("Item 2")).toBeInTheDocument();
  });

  it("renders CategoryTabs", () => {
    vi.mocked(useItemsModule.useItems).mockReturnValue(baseHook);
    render(<FeedList />);
    expect(screen.getByRole("tablist")).toBeInTheDocument();
  });

  it("calls setCategory when a tab is clicked", async () => {
    const setCategory = vi.fn();
    vi.mocked(useItemsModule.useItems).mockReturnValue({
      ...baseHook,
      setCategory,
    });
    render(<FeedList />);
    await userEvent.click(screen.getByRole("tab", { name: "Research" }));
    expect(setCategory).toHaveBeenCalledWith("research");
  });

  it("renders scroll sentinel when hasMore is true", () => {
    vi.mocked(useItemsModule.useItems).mockReturnValue({
      ...baseHook,
      items: [makeItem("1")],
      hasMore: true,
    });
    const { container } = render(<FeedList />);
    expect(container.querySelector("[data-sentinel]")).toBeInTheDocument();
  });

  it("does not render sentinel when hasMore is false", () => {
    vi.mocked(useItemsModule.useItems).mockReturnValue({
      ...baseHook,
      items: [makeItem("1")],
      hasMore: false,
    });
    const { container } = render(<FeedList />);
    expect(container.querySelector("[data-sentinel]")).not.toBeInTheDocument();
  });
});
