import Link from "next/link";
import { FeedList } from "@/components/FeedList";

export default function Home() {
  return (
    <main className="min-h-screen">
      <header className="sticky top-0 z-10 border-b border-zinc-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-sm">
        <div className="max-w-2xl mx-auto px-4 py-3 flex items-center gap-4">
          <h1 className="text-lg font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            AI News
          </h1>
          <nav className="ml-auto">
            <Link
              href="/sources"
              className="text-sm text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
            >
              Sources
            </Link>
          </nav>
        </div>
      </header>
      <FeedList />
    </main>
  );
}
