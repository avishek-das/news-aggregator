"use client";
import { useItems } from "@/hooks/use-items";
import { useIntersection } from "@/hooks/use-intersection";
import { CategoryTabs } from "@/components/CategoryTabs";
import { ItemCard } from "@/components/ItemCard";
import { SkeletonCard } from "@/components/SkeletonCard";

export function FeedList() {
  const {
    items,
    isLoading,
    error,
    hasMore,
    category,
    setCategory,
    loadMore,
    markItemRead,
  } = useItems();

  const sentinelRef = useIntersection(loadMore);

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 space-y-4">
      <CategoryTabs active={category} onSelect={setCategory} />

      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 dark:border-red-900 dark:bg-red-950 p-4 text-sm text-red-700 dark:text-red-400">
          {error}
        </div>
      )}

      {isLoading && items.length === 0 && (
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      )}

      {!isLoading && !error && items.length === 0 && (
        <p className="text-center text-zinc-500 dark:text-zinc-400 py-12">
          No items found.
        </p>
      )}

      {items.length > 0 && (
        <div className="space-y-3">
          {items.map((item) => (
            <ItemCard key={item.id} item={item} onMarkRead={markItemRead} />
          ))}

          {isLoading && (
            <div className="flex justify-center py-4">
              <div className="h-5 w-5 animate-spin rounded-full border-2 border-zinc-300 border-t-zinc-700 dark:border-zinc-700 dark:border-t-zinc-300" />
            </div>
          )}

          {hasMore && (
            <div ref={sentinelRef} data-sentinel className="h-1" />
          )}
        </div>
      )}
    </div>
  );
}
