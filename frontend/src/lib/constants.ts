import type { Category } from "@/types/item";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const DEFAULT_LIMIT = 20;

export interface CategoryOption {
  label: string;
  value: Category | undefined;
}

export const CATEGORIES: CategoryOption[] = [
  { label: "All", value: undefined },
  { label: "Research", value: "research" },
  { label: "Code", value: "code" },
  { label: "Community", value: "community" },
  { label: "Product", value: "product" },
  { label: "Media", value: "media" },
];
