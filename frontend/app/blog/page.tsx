import type { Metadata } from "next";
import Link from "next/link";
import { getPosts, getSite } from "@/lib/api";

export async function generateMetadata(): Promise<Metadata> {
  const site = await getSite();
  return {
    title: "Blog",
    description: `Daily ${site.industry} essays for ${site.audience}.`
  };
}

export default async function BlogIndexPage() {
  const posts = await getPosts();
  return (
    <main className="main">
      <section className="section" style={{ marginTop: 0 }}>
        <h2>Blog</h2>
        <div className="grid">
          {posts.map((post) => (
            <Link className="post-card" href={`/blog/${post.slug}`} key={post.id}>
              <h3>{post.title}</h3>
              <p>{post.excerpt}</p>
              <div className="tags">
                {post.tags.map((tag) => (
                  <span className="tag" key={tag}>
                    {tag}
                  </span>
                ))}
              </div>
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}

