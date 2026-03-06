import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { SourcesTable } from "../SourcesTable";
import type { Source } from "@/types/source";

const baseSource: Source = {
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

const noOp = vi.fn();

describe("SourcesTable", () => {
  it("shows empty state when no sources", () => {
    render(
      <SourcesTable sources={[]} onEdit={noOp} onRetire={noOp} onReactivate={noOp} onDelete={noOp} />
    );
    expect(screen.getByText(/no sources/i)).toBeInTheDocument();
  });

  it("renders source name", () => {
    render(
      <SourcesTable sources={[baseSource]} onEdit={noOp} onRetire={noOp} onReactivate={noOp} onDelete={noOp} />
    );
    expect(screen.getByText("arXiv cs.AI")).toBeInTheDocument();
  });

  it("renders status badge", () => {
    render(
      <SourcesTable sources={[baseSource]} onEdit={noOp} onRetire={noOp} onReactivate={noOp} onDelete={noOp} />
    );
    expect(screen.getByText("active")).toBeInTheDocument();
  });

  it("shows Retire button for active source", () => {
    render(
      <SourcesTable sources={[baseSource]} onEdit={noOp} onRetire={noOp} onReactivate={noOp} onDelete={noOp} />
    );
    expect(screen.getByRole("button", { name: /retire arXiv cs\.AI/i })).toBeInTheDocument();
  });

  it("shows Activate button for inactive source", () => {
    const inactive = { ...baseSource, status: "inactive" as const };
    render(
      <SourcesTable sources={[inactive]} onEdit={noOp} onRetire={noOp} onReactivate={noOp} onDelete={noOp} />
    );
    expect(screen.getByRole("button", { name: /activate arXiv cs\.AI/i })).toBeInTheDocument();
  });

  it("calls onEdit when Edit is clicked", async () => {
    const onEdit = vi.fn();
    render(
      <SourcesTable sources={[baseSource]} onEdit={onEdit} onRetire={noOp} onReactivate={noOp} onDelete={noOp} />
    );
    await userEvent.click(screen.getByRole("button", { name: /edit arXiv cs\.AI/i }));
    expect(onEdit).toHaveBeenCalledWith(baseSource);
  });

  it("calls onRetire with id when Retire is clicked", async () => {
    const onRetire = vi.fn();
    render(
      <SourcesTable sources={[baseSource]} onEdit={noOp} onRetire={onRetire} onReactivate={noOp} onDelete={noOp} />
    );
    await userEvent.click(screen.getByRole("button", { name: /retire arXiv cs\.AI/i }));
    expect(onRetire).toHaveBeenCalledWith("src-1");
  });

  it("calls onDelete with id when Delete is clicked", async () => {
    const onDelete = vi.fn();
    render(
      <SourcesTable sources={[baseSource]} onEdit={noOp} onRetire={noOp} onReactivate={noOp} onDelete={onDelete} />
    );
    await userEvent.click(screen.getByRole("button", { name: /delete arXiv cs\.AI/i }));
    expect(onDelete).toHaveBeenCalledWith("src-1");
  });

  it("highlights non-zero failures in red", () => {
    const failing = { ...baseSource, consecutive_failures: 2 };
    render(
      <SourcesTable sources={[failing]} onEdit={noOp} onRetire={noOp} onReactivate={noOp} onDelete={noOp} />
    );
    // The failure count "2" should appear in the DOM
    const failureText = screen.getByText("2");
    expect(failureText).toBeInTheDocument();
    expect(failureText.className).toContain("red");
  });

  it("shows Retire for flagged source", () => {
    const flagged = { ...baseSource, status: "flagged" as const };
    render(
      <SourcesTable sources={[flagged]} onEdit={noOp} onRetire={noOp} onReactivate={noOp} onDelete={noOp} />
    );
    expect(screen.getByRole("button", { name: /retire/i })).toBeInTheDocument();
  });
});
