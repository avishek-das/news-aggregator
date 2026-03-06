"use client";
import { useState, useEffect, useCallback, useRef } from "react";
import { fetchItems, markRead } from "@/lib/api";
import { DEFAULT_LIMIT } from "@/lib/constants";
import type { FeedItem, Category } from "@/types/item";

interface UseItemsResult {
  items: FeedItem[];
  isLoading: boolean;
  error: string | null;
  hasMore: boolean;
  category: Category | undefined;
  setCategory: (category: Category | undefined) => void;
  loadMore: () => void;
  markItemRead: (id: string) => Promise<void>;
}

export function useItems(): UseItemsResult {
  const [items, setItems] = useState<FeedItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const [category, setCategory] = useState<Category | undefined>(undefined);
  const offsetRef = useRef(0);
  const abortRef = useRef<AbortController | null>(null);

  const load = useCallback(
    async (cat: Category | undefined, offset: number, replace: boolean) => {
      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      setIsLoading(true);
      setError(null);
      try {
        const result = await fetchItems({
          category: cat,
          limit: DEFAULT_LIMIT,
          offset,
        });
        if (controller.signal.aborted) return;
        const newItems = result.data;
        setItems((prev) => (replace ? newItems : [...prev, ...newItems]));
        const newOffset = offset + newItems.length;
        setHasMore(newOffset < result.meta.total);
        offsetRef.current = newOffset;
      } catch (err) {
        if (controller.signal.aborted) return;
        setError(err instanceof Error ? err.message : "Failed to load items");
        if (replace) setItems([]);
      } finally {
        if (!controller.signal.aborted) setIsLoading(false);
      }
    },
    []
  );

  useEffect(() => {
    offsetRef.current = 0;
    load(category, 0, true);
    return () => {
      abortRef.current?.abort();
    };
  }, [category, load]);

  const loadMore = useCallback(() => {
    if (!isLoading && hasMore) {
      load(category, offsetRef.current, false);
    }
  }, [isLoading, hasMore, category, load]);

  const handleSetCategory = useCallback((cat: Category | undefined) => {
    setCategory(cat);
  }, []);

  const markItemRead = useCallback(async (id: string) => {
    await markRead(id);
    setItems((prev) =>
      prev.map((item) =>
        item.id === id ? { ...item, is_read: true } : item
      )
    );
  }, []);

  return {
    items,
    isLoading,
    error,
    hasMore,
    category,
    setCategory: handleSetCategory,
    loadMore,
    markItemRead,
  };
}
