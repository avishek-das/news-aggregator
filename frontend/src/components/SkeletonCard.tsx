"use client";

export function SkeletonCard() {
  return (
    <article
      aria-busy="true"
      className="border border-zinc-200 dark:border-zinc-800 rounded-lg p-4 space-y-3"
    >
      <div className="animate-pulse space-y-2">
        <div className="h-4 bg-zinc-200 dark:bg-zinc-700 rounded w-3/4" />
        <div className="h-4 bg-zinc-200 dark:bg-zinc-700 rounded w-1/2" />
      </div>
      <div className="animate-pulse space-y-2">
        <div className="h-3 bg-zinc-100 dark:bg-zinc-800 rounded w-full" />
        <div className="h-3 bg-zinc-100 dark:bg-zinc-800 rounded w-5/6" />
      </div>
      <div className="animate-pulse flex gap-2">
        <div className="h-3 bg-zinc-200 dark:bg-zinc-700 rounded w-16" />
        <div className="h-3 bg-zinc-200 dark:bg-zinc-700 rounded w-16" />
        <div className="h-3 bg-zinc-200 dark:bg-zinc-700 rounded w-12 ml-auto" />
      </div>
    </article>
  );
}
