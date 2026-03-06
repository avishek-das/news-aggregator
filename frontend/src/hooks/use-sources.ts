"use client";

import { useState, useEffect, useCallback } from "react";
import type { Source, SourceCreatePayload, SourceUpdatePayload } from "@/types/source";
import {
  fetchSources,
  createSource,
  updateSource,
  retireSource,
  reactivateSource,
  deleteSource,
} from "@/lib/sources-api";

interface UseSourcesReturn {
  sources: Source[];
  loading: boolean;
  error: string | null;
  reload: () => void;
  create: (payload: SourceCreatePayload) => Promise<Source>;
  update: (id: string, payload: SourceUpdatePayload) => Promise<Source>;
  retire: (id: string) => Promise<void>;
  reactivate: (id: string) => Promise<void>;
  remove: (id: string) => Promise<void>;
}

export function useSources(): UseSourcesReturn {
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchSources();
      setSources(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const create = useCallback(async (payload: SourceCreatePayload): Promise<Source> => {
    const newSource = await createSource(payload);
    setSources((prev) => [...prev, newSource].sort((a, b) => a.name.localeCompare(b.name)));
    return newSource;
  }, []);

  const update = useCallback(async (id: string, payload: SourceUpdatePayload): Promise<Source> => {
    const updated = await updateSource(id, payload);
    setSources((prev) => prev.map((s) => (s.id === id ? updated : s)));
    return updated;
  }, []);

  const retire = useCallback(async (id: string): Promise<void> => {
    const updated = await retireSource(id);
    setSources((prev) => prev.map((s) => (s.id === id ? updated : s)));
  }, []);

  const reactivate = useCallback(async (id: string): Promise<void> => {
    const updated = await reactivateSource(id);
    setSources((prev) => prev.map((s) => (s.id === id ? updated : s)));
  }, []);

  const remove = useCallback(async (id: string): Promise<void> => {
    await deleteSource(id);
    setSources((prev) => prev.filter((s) => s.id !== id));
  }, []);

  return { sources, loading, error, reload: load, create, update, retire, reactivate, remove };
}
