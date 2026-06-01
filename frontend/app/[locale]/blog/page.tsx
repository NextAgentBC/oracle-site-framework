import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { getPosts, getSite } from "@/lib/api";
import { alternatesFor, loadMessages, normalizeLocale, t } from "@/lib/i18n";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale: raw } = await params;
  const locale = normalizeLocale(raw);
  const [site, messages] = await Promise.all([getSite(), loadMessages(locale)]);
  return {
    title: t(messages, "meta.blog"),
    description: t(messages, "blog.lede", { industry: site.industry, audience: site.audience }),
    alternates: alternatesFor(locale, "/blog")
  };
}

export default async function BlogIndexPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale: raw } = await params;
  const locale = normalizeLocale(raw);
  const [site, posts, messages] = await Promise.all([getSite(), getPosts(locale), loadMessages(locale)]);
  return (
    <main className="main">
      <header className="page-header">
        <p className="kicker">{t(messages, "blog.kicker")}</p>
        <h1>{t(messages, "blog.title")}</h1>
        <p className="lede">{t(messages, "blog.lede", { industry: site.industry, audience: site.audience })}</p>
      </header>
      {posts.length ? (
        <div className="grid">
          {posts.map((post) => (
            <Link className="post-card" href={`/${locale}/blog/${post.slug}`} key={post.id}>
              <h3>{post.title}</h3>
              <p>{post.excerpt}</p>
              {post.tags?.length ? (
                <div className="tags">
                  {post.tags.map((tag) => (
                    <span className="tag" key={tag}>
                      {tag}
                    </span>
                  ))}
                </div>
              ) : null}
              <span className="button ghost">
                {t(messages, "blog.read")} <ArrowRight size={16} />
              </span>
            </Link>
          ))}
        </div>
      ) : (
        <div className="post-card">
          <h3>{t(messages, "blog.empty")}</h3>
          <p>{t(messages, "home.noPostsBody")}</p>
        </div>
      )}
    </main>
  );
}
