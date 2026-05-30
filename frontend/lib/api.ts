export type Site = {
  name: string;
  url: string;
  industry: string;
  audience: string;
  region: string;
  googleClientId: string;
};

export type BlogPost = {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  bodyMarkdown?: string;
  tags: string[];
  author: string;
  publishedAt: string | null;
  metaTitle: string;
  metaDescription: string;
  canonicalUrl: string;
  geoRegion: string;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

type NextRequestInit = RequestInit & { next?: { revalidate?: number } };

async function fetchJson<T>(path: string, init?: NextRequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {})
    },
    next: { revalidate: 300 }
  });
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function getSite(): Promise<Site> {
  try {
    const data = await fetchJson<{ item: Site }>("/site");
    return data.item;
  } catch {
    return {
      name: "Oracle Site",
      url: process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000",
      industry: "education",
      audience: "students and independent creators",
      region: "United States",
      googleClientId: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || ""
    };
  }
}

export async function getPosts(): Promise<BlogPost[]> {
  try {
    const data = await fetchJson<{ items: BlogPost[] }>("/blogs");
    return data.items;
  } catch {
    return [];
  }
}

export async function getPost(slug: string): Promise<BlogPost | null> {
  try {
    const data = await fetchJson<{ item: BlogPost }>(`/blogs/${slug}`);
    return data.item;
  } catch {
    return null;
  }
}

export async function postJson<T>(path: string, body: unknown): Promise<T> {
  return fetchJson<T>(path, {
    method: "POST",
    body: JSON.stringify(body),
    cache: "no-store"
  });
}
