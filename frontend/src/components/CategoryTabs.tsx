"use client";
import { CATEGORIES } from "@/lib/constants";
import type { Category } from "@/types/item";

interface CategoryTabsProps {
  active: Category | undefined;
  onSelect: (category: Category | undefined) => void;
}

export function CategoryTabs({ active, onSelect }: CategoryTabsProps) {
  return (
    <div
      role="tablist"
      aria-label="Filter by category"
      className="flex gap-1 overflow-x-auto pb-1 scrollbar-none"
    >
      {CATEGORIES.map(({ label, value }) => {
        const isActive = value === active;
        return (
          <button
            key={label}
            role="tab"
            aria-selected={isActive}
            onClick={() => onSelect(value)}
            className={[
              "px-3 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors",
              isActive
                ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900"
                : "text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100",
            ].join(" ")}
          >
            {label}
          </button>
        );
      })}
    </div>
  );
}
