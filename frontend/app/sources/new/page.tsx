"use client";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useSources } from "@/hooks/use-sources";
import { SourceForm } from "@/components/SourceForm";
import type { SourceCreatePayload } from "@/types/source";

export default function NewSourcePage() {
  const router = useRouter();
  const { create } = useSources();

  const handleSubmit = async (payload: SourceCreatePayload) => {
    await create(payload as SourceCreatePayload);
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
            Add Source
          </h1>
        </div>
      </header>

      <div className="max-w-2xl mx-auto px-4 py-6">
        <SourceForm
          onSubmit={(payload) => handleSubmit(payload as SourceCreatePayload)}
          onCancel={() => router.push("/sources")}
          submitLabel="Create Source"
        />
      </div>
    </main>
  );
}
