"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useSources } from "@/hooks/use-sources";
import { SourcesTable } from "@/components/SourcesTable";
import type { Source } from "@/types/source";

export default function SourcesPage() {
  const router = useRouter();
  const { sources, loading, error, retire, reactivate, remove } = useSources();
  const [actionError, setActionError] = useState<string | null>(null);

  const handleRetire = async (id: string) => {
    setActionError(null);
    try {
      await retire(id);
    } catch (err) {
      setActionError(err instanceof Error ? err.message : "Failed to retire source");
    }
  };

  const handleReactivate = async (id: string) => {
    setActionError(null);
    try {
      await reactivate(id);
    } catch (err) {
      setActionError(err instanceof Error ? err.message : "Failed to reactivate source");
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this source? This cannot be undone.")) return;
    setActionError(null);
    try {
      await remove(id);
    } catch (err) {
      setActionError(err instanceof Error ? err.message : "Failed to delete source");
    }
  };

  return (
    <main className="min-h-screen">
      <header className="sticky top-0 z-10 border-b border-zinc-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-sm">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center gap-4">
          <Link
            href="/"
            className="text-sm text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
          >
            ← Feed
          </Link>
          <h1 className="text-lg font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            Sources
          </h1>
          <div className="ml-auto">
            <Link
              href="/sources/new"
              className="inline-block px-3 py-1.5 text-sm font-medium rounded-md bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 hover:bg-zinc-700 dark:hover:bg-zinc-300 transition-colors"
            >
              + Add Source
            </Link>
          </div>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-6 space-y-4">
        {actionError && (
          <p role="alert" className="text-sm text-red-600 dark:text-red-400">
            {actionError}
          </p>
        )}

        {loading ? (
          <p className="text-center text-zinc-500 dark:text-zinc-400 py-12">
            Loading sources…
          </p>
        ) : error ? (
          <p role="alert" className="text-center text-red-600 dark:text-red-400 py-12">
            {error}
          </p>
        ) : (
          <SourcesTable
            sources={sources}
            onEdit={(source: Source) => router.push(`/sources/${source.id}/edit`)}
            onRetire={handleRetire}
            onReactivate={handleReactivate}
            onDelete={handleDelete}
          />
        )}
      </div>
    </main>
  );
}
