import { FeedList } from "@/components/FeedList";

export default function Home() {
  return (
    <main className="min-h-screen">
      <header className="sticky top-0 z-10 border-b border-zinc-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-sm">
        <div className="max-w-2xl mx-auto px-4 py-3">
          <h1 className="text-lg font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            AI News
          </h1>
        </div>
      </header>
      <FeedList />
    </main>
  );
}
