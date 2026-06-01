import type { Metadata } from "next";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import { getPage, getSite } from "@/lib/api";
import { SectionRenderer } from "@/components/sections";
import { alternatesFor, normalizeLocale } from "@/lib/i18n";

type PageProps = {
  params: Promise<{ slug: string; locale: string }>;
};

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug, locale: raw } = await params;
  const locale = normalizeLocale(raw);
  const page = await getPage(slug, locale);
  if (!page) return {};
  return {
    title: page.metaTitle || page.title,
    description: page.metaDescription || undefined,
    alternates: alternatesFor(locale, `/${page.slug}`)
  };
}

export default async function ContentPage({ params }: PageProps) {
  const { slug, locale: raw } = await params;
  const locale = normalizeLocale(raw);
  const page = await getPage(slug, locale);
  if (!page) notFound();

  // Module-composed page (like the home), or a simple markdown page.
  if (page.sections && page.sections.length > 0) {
    const site = await getSite();
    return (
      <main className="main">
        <SectionRenderer sections={page.sections} site={site} />
      </main>
    );
  }

  return (
    <main className="main">
      <article className="article">
        <h1>{page.title}</h1>
        <ReactMarkdown>{page.bodyMarkdown || ""}</ReactMarkdown>
      </article>
    </main>
  );
}
