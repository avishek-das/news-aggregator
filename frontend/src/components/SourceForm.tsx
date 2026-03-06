"use client";
import { useState } from "react";
import type { Source, SourceCreatePayload, SourceUpdatePayload } from "@/types/source";

const SOURCE_TYPES = ["rss", "api", "scrape"] as const;
const CATEGORIES = ["research", "code", "community", "product", "media"] as const;
const PRIORITIES = ["high", "medium", "low"] as const;

interface SourceFormProps {
  initial?: Source;
  onSubmit: (payload: SourceCreatePayload | SourceUpdatePayload) => Promise<void>;
  onCancel: () => void;
  submitLabel?: string;
}

export function SourceForm({
  initial,
  onSubmit,
  onCancel,
  submitLabel = "Save",
}: SourceFormProps) {
  const [name, setName] = useState(initial?.name ?? "");
  const [url, setUrl] = useState(initial?.url ?? "");
  const [type, setType] = useState<(typeof SOURCE_TYPES)[number]>(
    initial?.type ?? "rss"
  );
  const [category, setCategory] = useState<(typeof CATEGORIES)[number]>(
    initial?.category ?? "research"
  );
  const [priority, setPriority] = useState<(typeof PRIORITIES)[number]>(
    initial?.priority ?? "medium"
  );
  const [adapter, setAdapter] = useState(
    (initial?.fetch_config?.adapter as string) ?? ""
  );
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const fetch_config = adapter ? { adapter } : {};
      if (initial) {
        const payload: SourceUpdatePayload = { name, url, type, category, priority };
        if (adapter) payload.fetch_config = fetch_config;
        await onSubmit(payload);
      } else {
        await onSubmit({ name, url, type, category, priority, fetch_config });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4" aria-label="Source form">
      {error && (
        <p role="alert" className="text-sm text-red-600 dark:text-red-400">
          {error}
        </p>
      )}

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="sm:col-span-2">
          <label
            htmlFor="source-name"
            className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1"
          >
            Name
          </label>
          <input
            id="source-name"
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full rounded-md border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-2 text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-zinc-500"
            placeholder="arXiv cs.AI"
          />
        </div>

        <div className="sm:col-span-2">
          <label
            htmlFor="source-url"
            className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1"
          >
            URL
          </label>
          <input
            id="source-url"
            type="url"
            required
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full rounded-md border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-2 text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-zinc-500"
            placeholder="https://..."
          />
        </div>

        <div>
          <label
            htmlFor="source-type"
            className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1"
          >
            Type
          </label>
          <select
            id="source-type"
            value={type}
            onChange={(e) => setType(e.target.value as (typeof SOURCE_TYPES)[number])}
            className="w-full rounded-md border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-2 text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-zinc-500"
          >
            {SOURCE_TYPES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label
            htmlFor="source-category"
            className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1"
          >
            Category
          </label>
          <select
            id="source-category"
            value={category}
            onChange={(e) => setCategory(e.target.value as (typeof CATEGORIES)[number])}
            className="w-full rounded-md border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-2 text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-zinc-500"
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label
            htmlFor="source-priority"
            className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1"
          >
            Priority
          </label>
          <select
            id="source-priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value as (typeof PRIORITIES)[number])}
            className="w-full rounded-md border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-2 text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-zinc-500"
          >
            {PRIORITIES.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label
            htmlFor="source-adapter"
            className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1"
          >
            Adapter <span className="text-zinc-400 font-normal">(optional)</span>
          </label>
          <input
            id="source-adapter"
            type="text"
            value={adapter}
            onChange={(e) => setAdapter(e.target.value)}
            className="w-full rounded-md border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-2 text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-zinc-500"
            placeholder="e.g. arxiv, hackernews"
          />
        </div>
      </div>

      <div className="flex items-center gap-3 pt-2">
        <button
          type="submit"
          disabled={submitting}
          className="px-4 py-2 text-sm font-medium rounded-md bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 hover:bg-zinc-700 dark:hover:bg-zinc-300 disabled:opacity-50 transition-colors"
        >
          {submitting ? "Saving…" : submitLabel}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium rounded-md border border-zinc-300 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
