export type SourceType = "rss" | "api" | "scrape";
export type SourceCategory = "research" | "code" | "community" | "product" | "media";
export type SourcePriority = "high" | "medium" | "low";
export type SourceStatus = "active" | "inactive" | "flagged";

export interface Source {
  id: string;
  name: string;
  url: string;
  type: SourceType;
  category: SourceCategory;
  priority: SourcePriority;
  status: SourceStatus;
  fetch_config: Record<string, unknown>;
  last_fetched_at: string | null;
  last_error: string | null;
  consecutive_failures: number;
  updated_at: string | null;
  created_at: string | null;
}

export interface SourcesListResponse {
  success: boolean;
  data: Source[];
  error: string | null;
}

export interface SourceSingleResponse {
  success: boolean;
  data: Source | null;
  error: string | null;
}

export interface SourceCreatePayload {
  name: string;
  url: string;
  type: SourceType;
  category: SourceCategory;
  priority: SourcePriority;
  fetch_config?: Record<string, unknown>;
}

export interface SourceUpdatePayload {
  name?: string;
  url?: string;
  type?: SourceType;
  category?: SourceCategory;
  priority?: SourcePriority;
  status?: SourceStatus;
  fetch_config?: Record<string, unknown>;
}
