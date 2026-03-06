import { API_BASE_URL } from "@/lib/constants";
import type {
  Source,
  SourcesListResponse,
  SourceSingleResponse,
  SourceCreatePayload,
  SourceUpdatePayload,
} from "@/types/source";

export async function fetchSources(): Promise<Source[]> {
  const response = await fetch(`${API_BASE_URL}/sources`, {
    credentials: "include",
  });
  const body: SourcesListResponse = await response.json();
  if (!body.success) throw new Error(body.error ?? "Failed to load sources");
  return body.data;
}

export async function createSource(payload: SourceCreatePayload): Promise<Source> {
  const response = await fetch(`${API_BASE_URL}/sources`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const body: SourceSingleResponse = await response.json();
  if (!body.success || !body.data)
    throw new Error(body.error ?? "Failed to create source");
  return body.data;
}

export async function updateSource(
  id: string,
  payload: SourceUpdatePayload
): Promise<Source> {
  const response = await fetch(`${API_BASE_URL}/sources/${id}`, {
    method: "PATCH",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const body: SourceSingleResponse = await response.json();
  if (!body.success || !body.data)
    throw new Error(body.error ?? "Failed to update source");
  return body.data;
}

export async function retireSource(id: string): Promise<Source> {
  const response = await fetch(`${API_BASE_URL}/sources/${id}/retire`, {
    method: "POST",
    credentials: "include",
  });
  const body: SourceSingleResponse = await response.json();
  if (!body.success || !body.data)
    throw new Error(body.error ?? "Failed to retire source");
  return body.data;
}

export async function reactivateSource(id: string): Promise<Source> {
  const response = await fetch(`${API_BASE_URL}/sources/${id}/reactivate`, {
    method: "POST",
    credentials: "include",
  });
  const body: SourceSingleResponse = await response.json();
  if (!body.success || !body.data)
    throw new Error(body.error ?? "Failed to reactivate source");
  return body.data;
}

export async function deleteSource(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/sources/${id}`, {
    method: "DELETE",
    credentials: "include",
  });
  if (!response.ok) {
    if (response.status === 409) {
      const body = await response.json();
      throw new Error(body.detail ?? "Cannot delete source with existing items");
    }
    throw new Error(`Delete failed: ${response.status}`);
  }
}
