const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export type Trend = {
  title: string;
  source: string;
  keyword: string;
  url: string;
  engagement: number;
  recency_hours: number;
  viral_score: number;
};

export type SavedIdea = {
  id: number;
  title: string;
  source: string;
  keyword: string;
  url: string;
  viral_score: number;
  created_at: string;
};

export async function fetchSearch(keyword: string): Promise<Trend[]> {
  const response = await fetch(`${API_BASE_URL}/api/search?keyword=${encodeURIComponent(keyword)}`);
  if (!response.ok) throw new Error("Failed to fetch trends");
  return response.json();
}

export async function fetchDashboard(): Promise<Trend[]> {
  const response = await fetch(`${API_BASE_URL}/api/dashboard`, { cache: "no-store" });
  if (!response.ok) throw new Error("Failed to fetch dashboard");
  return response.json();
}

export async function fetchIdeas(): Promise<SavedIdea[]> {
  const response = await fetch(`${API_BASE_URL}/api/ideas`, { cache: "no-store" });
  if (!response.ok) throw new Error("Failed to fetch ideas");
  return response.json();
}

export async function saveIdea(input: Omit<SavedIdea, "id" | "created_at">): Promise<SavedIdea> {
  const response = await fetch(`${API_BASE_URL}/api/ideas`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input)
  });
  if (!response.ok) throw new Error("Failed to save idea");
  return response.json();
}

export function exportCsvUrl(): string {
  return `${API_BASE_URL}/api/export.csv`;
}
