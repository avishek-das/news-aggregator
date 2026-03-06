import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import Page from "../app/page";

vi.mock("@/hooks/use-items", () => ({
  useItems: () => ({
    items: [],
    isLoading: false,
    error: null,
    hasMore: false,
    category: undefined,
    setCategory: vi.fn(),
    loadMore: vi.fn(),
    markItemRead: vi.fn(),
  }),
}));

// Stub IntersectionObserver — must be a class for `new` to work
class MockIntersectionObserver {
  observe = vi.fn();
  disconnect = vi.fn();
  constructor(_cb: IntersectionObserverCallback) {}
}
vi.stubGlobal("IntersectionObserver", MockIntersectionObserver);

describe("Home page", () => {
  it("renders the app heading", () => {
    render(<Page />);
    expect(screen.getByText(/AI News/i)).toBeInTheDocument();
  });
});
