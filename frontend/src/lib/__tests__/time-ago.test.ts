import { describe, it, expect } from "vitest";
import { timeAgo } from "../time-ago";

const now = new Date("2026-03-05T12:00:00Z").getTime();

describe("timeAgo", () => {
  it("returns empty string for null", () => {
    expect(timeAgo(null, now)).toBe("");
  });

  it("returns empty string for undefined", () => {
    expect(timeAgo(undefined, now)).toBe("");
  });

  it("returns 'just now' for < 60s ago", () => {
    const date = new Date(now - 30 * 1000).toISOString();
    expect(timeAgo(date, now)).toBe("just now");
  });

  it("returns minutes ago", () => {
    const date = new Date(now - 5 * 60 * 1000).toISOString();
    expect(timeAgo(date, now)).toBe("5m ago");
  });

  it("returns hours ago", () => {
    const date = new Date(now - 3 * 60 * 60 * 1000).toISOString();
    expect(timeAgo(date, now)).toBe("3h ago");
  });

  it("returns days ago", () => {
    const date = new Date(now - 2 * 24 * 60 * 60 * 1000).toISOString();
    expect(timeAgo(date, now)).toBe("2d ago");
  });

  it("returns weeks ago", () => {
    const date = new Date(now - 10 * 24 * 60 * 60 * 1000).toISOString();
    expect(timeAgo(date, now)).toBe("1w ago");
  });

  it("returns months ago", () => {
    const date = new Date(now - 60 * 24 * 60 * 60 * 1000).toISOString();
    expect(timeAgo(date, now)).toBe("2mo ago");
  });

  it("returns years ago", () => {
    const date = new Date(now - 400 * 24 * 60 * 60 * 1000).toISOString();
    expect(timeAgo(date, now)).toBe("1y ago");
  });
});
