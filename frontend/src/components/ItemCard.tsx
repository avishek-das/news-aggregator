"use client";
import { timeAgo } from "@/lib/time-ago";
import type { FeedItem } from "@/types/item";

const CATEGORY_COLORS: Record<string, string> = {
  research: "bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300",
  code: "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300",
  community: "bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300",
  product: "bg-orange-100 text-orange-700 dark:bg-orange-900 dark:text-orange-300",
  media: "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300",
};

interface ItemCardProps {
  item: FeedItem;
  onMarkRead: (id: string) => void;
}

export function ItemCard({ item, onMarkRead }: ItemCardProps) {
  const handleClick = () => {
    if (!item.is_read) onMarkRead(item.id);
  };

  return (
    <article
      role="article"
      onClick={handleClick}
      className={[
        "border border-zinc-200 dark:border-zinc-800 rounded-lg p-4 space-y-2",
        "hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-colors cursor-pointer",
        item.is_read ? "opacity-60" : "",
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <a
        href={item.url}
        target="_blank"
        rel="noopener noreferrer"
        onClick={(e) => e.stopPropagation()}
        className="font-semibold text-zinc-900 dark:text-zinc-50 hover:underline leading-snug flex items-start gap-1"
      >
        {item.title}
        <svg
          aria-hidden="true"
          className="shrink-0 mt-0.5 w-3.5 h-3.5 text-zinc-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
          />
        </svg>
      </a>

      {item.excerpt && (
        <p className="text-sm text-zinc-600 dark:text-zinc-400 line-clamp-2">
          {item.excerpt}
        </p>
      )}

      <div className="flex flex-wrap items-center gap-2 text-xs">
        <span className="bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 px-2 py-0.5 rounded-full">
          {item.source_name}
        </span>
        <span
          className={`px-2 py-0.5 rounded-full ${CATEGORY_COLORS[item.category] ?? ""}`}
        >
          {item.category}
        </span>
        {item.is_paywalled && (
          <span className="text-amber-600 dark:text-amber-400">paywall</span>
        )}
        <span className="ml-auto text-zinc-400 dark:text-zinc-500">
          {timeAgo(item.published_at)}
        </span>
      </div>
    </article>
  );
}
