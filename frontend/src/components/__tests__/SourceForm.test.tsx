import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { SourceForm } from "../SourceForm";
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

describe("SourceForm", () => {
  it("renders empty form for new source", () => {
    render(<SourceForm onSubmit={vi.fn()} onCancel={vi.fn()} />);
    expect(screen.getByLabelText(/name/i)).toHaveValue("");
    expect(screen.getByLabelText(/url/i)).toHaveValue("");
  });

  it("pre-fills form with initial source values", () => {
    render(<SourceForm initial={baseSource} onSubmit={vi.fn()} onCancel={vi.fn()} />);
    expect(screen.getByLabelText(/name/i)).toHaveValue("arXiv cs.AI");
    expect(screen.getByLabelText(/url/i)).toHaveValue("https://export.arxiv.org/rss/cs.AI");
  });

  it("uses custom submit label", () => {
    render(<SourceForm onSubmit={vi.fn()} onCancel={vi.fn()} submitLabel="Create Source" />);
    expect(screen.getByRole("button", { name: "Create Source" })).toBeInTheDocument();
  });

  it("calls onCancel when Cancel is clicked", async () => {
    const onCancel = vi.fn();
    render(<SourceForm onSubmit={vi.fn()} onCancel={onCancel} />);
    await userEvent.click(screen.getByRole("button", { name: /cancel/i }));
    expect(onCancel).toHaveBeenCalledOnce();
  });

  it("calls onSubmit with payload when form submitted", async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    render(<SourceForm onSubmit={onSubmit} onCancel={vi.fn()} />);

    await userEvent.clear(screen.getByLabelText(/name/i));
    await userEvent.type(screen.getByLabelText(/name/i), "Hacker News");
    await userEvent.clear(screen.getByLabelText(/url/i));
    await userEvent.type(screen.getByLabelText(/url/i), "https://hn.com");

    await userEvent.click(screen.getByRole("button", { name: /save/i }));
    await waitFor(() => expect(onSubmit).toHaveBeenCalledOnce());

    const payload = onSubmit.mock.calls[0][0];
    expect(payload.name).toBe("Hacker News");
    expect(payload.url).toBe("https://hn.com");
  });

  it("shows error message when onSubmit throws", async () => {
    const onSubmit = vi.fn().mockRejectedValue(new Error("Server error"));
    render(<SourceForm onSubmit={onSubmit} onCancel={vi.fn()} />);

    await userEvent.type(screen.getByLabelText(/name/i), "Test");
    await userEvent.type(screen.getByLabelText(/url/i), "https://test.com");
    await userEvent.click(screen.getByRole("button", { name: /save/i }));

    await waitFor(() =>
      expect(screen.getByRole("alert")).toHaveTextContent("Server error")
    );
  });

  it("disables submit button while submitting", async () => {
    let resolve: () => void;
    const onSubmit = vi.fn().mockReturnValue(new Promise<void>((r) => { resolve = r; }));
    render(<SourceForm onSubmit={onSubmit} onCancel={vi.fn()} />);

    await userEvent.type(screen.getByLabelText(/name/i), "Test");
    await userEvent.type(screen.getByLabelText(/url/i), "https://test.com");
    await userEvent.click(screen.getByRole("button", { name: /save/i }));

    await waitFor(() =>
      expect(screen.getByRole("button", { name: /saving/i })).toBeDisabled()
    );
    resolve!();
  });
});
