"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useSources } from "@/hooks/use-sources";
import { SourceForm } from "@/components/SourceForm";
import type { Source, SourceUpdatePayload } from "@/types/source";

export default function EditSourcePage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;
  const { sources, loading, update } = useSources();
  const [source, setSource] = useState<Source | null>(null);

  useEffect(() => {
    if (!loading) {
      const found = sources.find((s) => s.id === id) ?? null;
      setSource(found);
    }
  }, [loading, sources, id]);

  const handleSubmit = async (payload: SourceUpdatePayload) => {
    await update(id, payload as SourceUpdatePayload);
    router.push("/sources");
  };

  return (
    <main className="min-h-screen">
      <header className="sticky top-0 z-10 border-b border-zinc-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-sm">
        <div className="max-w-2xl mx-auto px-4 py-3 flex items-center gap-4">
          <Link
            href="/sources"
            className="text-sm text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
          >
            ← Sources
          </Link>
          <h1 className="text-lg font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            Edit Source
          </h1>
        </div>
      </header>

      <div className="max-w-2xl mx-auto px-4 py-6">
        {loading ? (
          <p className="text-zinc-500 dark:text-zinc-400">Loading…</p>
        ) : !source ? (
          <p className="text-red-600 dark:text-red-400">Source not found.</p>
        ) : (
          <SourceForm
            initial={source}
            onSubmit={(payload) => handleSubmit(payload as SourceUpdatePayload)}
            onCancel={() => router.push("/sources")}
            submitLabel="Save Changes"
          />
        )}
      </div>
    </main>
  );
}
