"use client";
import type { Source } from "@/types/source";

const STATUS_COLORS: Record<string, string> = {
  active: "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300",
  inactive: "bg-zinc-100 text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400",
  flagged: "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300",
};

const PRIORITY_COLORS: Record<string, string> = {
  high: "text-red-600 dark:text-red-400",
  medium: "text-amber-600 dark:text-amber-400",
  low: "text-zinc-500 dark:text-zinc-400",
};

interface SourcesTableProps {
  sources: Source[];
  onEdit: (source: Source) => void;
  onRetire: (id: string) => void;
  onReactivate: (id: string) => void;
  onDelete: (id: string) => void;
}

export function SourcesTable({
  sources,
  onEdit,
  onRetire,
  onReactivate,
  onDelete,
}: SourcesTableProps) {
  if (sources.length === 0) {
    return (
      <p className="text-center text-zinc-500 dark:text-zinc-400 py-12">
        No sources yet. Add one above.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-zinc-200 dark:border-zinc-800">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900">
            <th className="text-left px-4 py-3 font-medium text-zinc-600 dark:text-zinc-400">
              Name
            </th>
            <th className="text-left px-4 py-3 font-medium text-zinc-600 dark:text-zinc-400">
              Type
            </th>
            <th className="text-left px-4 py-3 font-medium text-zinc-600 dark:text-zinc-400">
              Category
            </th>
            <th className="text-left px-4 py-3 font-medium text-zinc-600 dark:text-zinc-400">
              Priority
            </th>
            <th className="text-left px-4 py-3 font-medium text-zinc-600 dark:text-zinc-400">
              Status
            </th>
            <th className="text-left px-4 py-3 font-medium text-zinc-600 dark:text-zinc-400">
              Failures
            </th>
            <th className="px-4 py-3" />
          </tr>
        </thead>
        <tbody>
          {sources.map((source) => (
            <tr
              key={source.id}
              className="border-b border-zinc-100 dark:border-zinc-800 last:border-0 hover:bg-zinc-50 dark:hover:bg-zinc-900"
            >
              <td className="px-4 py-3">
                <span className="font-medium text-zinc-900 dark:text-zinc-50">
                  {source.name}
                </span>
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="ml-2 text-xs text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300"
                  aria-label={`Open ${source.name}`}
                >
                  ↗
                </a>
              </td>
              <td className="px-4 py-3 text-zinc-600 dark:text-zinc-400">
                {source.type}
              </td>
              <td className="px-4 py-3 text-zinc-600 dark:text-zinc-400">
                {source.category}
              </td>
              <td className={`px-4 py-3 font-medium ${PRIORITY_COLORS[source.priority] ?? ""}`}>
                {source.priority}
              </td>
              <td className="px-4 py-3">
                <span
                  className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${STATUS_COLORS[source.status] ?? ""}`}
                >
                  {source.status}
                </span>
              </td>
              <td className="px-4 py-3 text-zinc-500 dark:text-zinc-400">
                {source.consecutive_failures > 0 ? (
                  <span className="text-red-600 dark:text-red-400">
                    {source.consecutive_failures}
                  </span>
                ) : (
                  "0"
                )}
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center gap-2 justify-end">
                  <button
                    onClick={() => onEdit(source)}
                    className="text-xs text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
                    aria-label={`Edit ${source.name}`}
                  >
                    Edit
                  </button>
                  {source.status === "active" || source.status === "flagged" ? (
                    <button
                      onClick={() => onRetire(source.id)}
                      className="text-xs text-amber-600 hover:text-amber-800 dark:hover:text-amber-400 transition-colors"
                      aria-label={`Retire ${source.name}`}
                    >
                      Retire
                    </button>
                  ) : (
                    <button
                      onClick={() => onReactivate(source.id)}
                      className="text-xs text-green-600 hover:text-green-800 dark:hover:text-green-400 transition-colors"
                      aria-label={`Reactivate ${source.name}`}
                    >
                      Activate
                    </button>
                  )}
                  <button
                    onClick={() => onDelete(source.id)}
                    className="text-xs text-red-500 hover:text-red-700 dark:hover:text-red-400 transition-colors"
                    aria-label={`Delete ${source.name}`}
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
