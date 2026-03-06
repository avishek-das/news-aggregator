import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { SkeletonCard } from "../SkeletonCard";

describe("SkeletonCard", () => {
  it("renders an article with aria-busy", () => {
    render(<SkeletonCard />);
    expect(screen.getByRole("article")).toHaveAttribute("aria-busy", "true");
  });

  it("contains animated pulse elements", () => {
    const { container } = render(<SkeletonCard />);
    const pulseEls = container.querySelectorAll(".animate-pulse");
    expect(pulseEls.length).toBeGreaterThan(0);
  });
});
