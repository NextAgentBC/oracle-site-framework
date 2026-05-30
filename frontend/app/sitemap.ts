import type { MetadataRoute } from "next";
import { getPosts, getSite } from "@/lib/api";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const [site, posts] = await Promise.all([getSite(), getPosts()]);
  const base = process.env.NEXT_PUBLIC_SITE_URL || site.url;
  return [
    { url: base, changeFrequency: "daily", priority: 1 },
    { url: `${base}/blog`, changeFrequency: "daily", priority: 0.8 },
    ...posts.map((post) => ({
      url: `${base}/blog/${post.slug}`,
      lastModified: post.publishedAt || new Date().toISOString(),
      changeFrequency: "monthly" as const,
      priority: 0.7
    }))
  ];
}

