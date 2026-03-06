import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ItemCard } from "../ItemCard";
import type { FeedItem } from "@/types/item";

const baseItem: FeedItem = {
  id: "item-1",
  source_id: "s1",
  source_name: "arXiv cs.AI",
  title: "Test Paper Title",
  url: "https://arxiv.org/abs/1234",
  excerpt: "A short excerpt about the paper.",
  summary: null,
  published_at: "2026-03-04T00:00:00Z",
  category: "research",
  is_paywalled: false,
  is_read: false,
  created_at: "2026-03-04T00:00:00Z",
};

describe("ItemCard", () => {
  it("renders title as external link", () => {
    render(<ItemCard item={baseItem} onMarkRead={vi.fn()} />);
    const link = screen.getByRole("link", { name: /Test Paper Title/i });
    expect(link).toHaveAttribute("href", "https://arxiv.org/abs/1234");
    expect(link).toHaveAttribute("target", "_blank");
    expect(link).toHaveAttribute("rel", expect.stringContaining("noopener"));
  });

  it("renders the excerpt", () => {
    render(<ItemCard item={baseItem} onMarkRead={vi.fn()} />);
    expect(screen.getByText("A short excerpt about the paper.")).toBeInTheDocument();
  });

  it("renders the source badge", () => {
    render(<ItemCard item={baseItem} onMarkRead={vi.fn()} />);
    expect(screen.getByText("arXiv cs.AI")).toBeInTheDocument();
  });

  it("renders the category badge", () => {
    render(<ItemCard item={baseItem} onMarkRead={vi.fn()} />);
    expect(screen.getByText("research")).toBeInTheDocument();
  });

  it("has reduced opacity when is_read is true", () => {
    const { container } = render(
      <ItemCard item={{ ...baseItem, is_read: true }} onMarkRead={vi.fn()} />
    );
    expect(container.firstChild).toHaveClass("opacity-60");
  });

  it("has full opacity when is_read is false", () => {
    const { container } = render(<ItemCard item={baseItem} onMarkRead={vi.fn()} />);
    expect(container.firstChild).not.toHaveClass("opacity-60");
  });

  it("calls onMarkRead with item id when clicked and not read", async () => {
    const onMarkRead = vi.fn();
    render(<ItemCard item={baseItem} onMarkRead={onMarkRead} />);
    await userEvent.click(screen.getByRole("article"));
    expect(onMarkRead).toHaveBeenCalledWith("item-1");
  });

  it("does not call onMarkRead when already read", async () => {
    const onMarkRead = vi.fn();
    render(
      <ItemCard item={{ ...baseItem, is_read: true }} onMarkRead={onMarkRead} />
    );
    await userEvent.click(screen.getByRole("article"));
    expect(onMarkRead).not.toHaveBeenCalled();
  });
});
