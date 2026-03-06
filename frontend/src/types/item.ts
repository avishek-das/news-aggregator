export type Category = "research" | "code" | "community" | "product" | "media";

export interface FeedItem {
  id: string;
  source_id: string;
  source_name: string;
  title: string;
  url: string;
  excerpt: string;
  summary: string | null;
  published_at: string | null;
  category: Category;
  is_paywalled: boolean;
  is_read: boolean;
  created_at: string;
}

export interface Meta {
  total: number;
  limit: number;
  offset: number;
}

export interface ItemsListResponse {
  success: boolean;
  data: FeedItem[];
  error: string | null;
  meta: Meta;
}
