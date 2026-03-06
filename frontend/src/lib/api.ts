import { API_BASE_URL } from "@/lib/constants";
import type { Category, ItemsListResponse } from "@/types/item";

interface FetchItemsParams {
  category?: Category;
  limit?: number;
  offset?: number;
}

export async function fetchItems(
  params: FetchItemsParams = {}
): Promise<ItemsListResponse> {
  const url = new URL(`${API_BASE_URL}/items`);
  if (params.category) url.searchParams.set("category", params.category);
  if (params.limit !== undefined)
    url.searchParams.set("limit", String(params.limit));
  if (params.offset !== undefined)
    url.searchParams.set("offset", String(params.offset));

  const response = await fetch(url.toString(), { credentials: "include" });
  const body: ItemsListResponse = await response.json();
  if (!body.success) throw new Error(body.error ?? "Unknown API error");
  return body;
}

export async function markRead(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/items/${id}/read`, {
    method: "POST",
    credentials: "include",
  });
  if (!response.ok) throw new Error(`markRead failed: ${response.status}`);
}
