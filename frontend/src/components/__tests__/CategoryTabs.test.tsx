import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { CategoryTabs } from "../CategoryTabs";

describe("CategoryTabs", () => {
  it("renders all 6 tabs", () => {
    render(<CategoryTabs active={undefined} onSelect={vi.fn()} />);
    expect(screen.getAllByRole("tab")).toHaveLength(6);
  });

  it("renders a tablist", () => {
    render(<CategoryTabs active={undefined} onSelect={vi.fn()} />);
    expect(screen.getByRole("tablist")).toBeInTheDocument();
  });

  it("marks the active tab with aria-selected", () => {
    render(<CategoryTabs active="research" onSelect={vi.fn()} />);
    const activeTab = screen.getByRole("tab", { name: "Research" });
    expect(activeTab).toHaveAttribute("aria-selected", "true");
  });

  it("calls onSelect with undefined for 'All'", async () => {
    const onSelect = vi.fn();
    render(<CategoryTabs active="research" onSelect={onSelect} />);
    await userEvent.click(screen.getByRole("tab", { name: "All" }));
    expect(onSelect).toHaveBeenCalledWith(undefined);
  });

  it("calls onSelect with category value on tab click", async () => {
    const onSelect = vi.fn();
    render(<CategoryTabs active={undefined} onSelect={onSelect} />);
    await userEvent.click(screen.getByRole("tab", { name: "Code" }));
    expect(onSelect).toHaveBeenCalledWith("code");
  });
});
