import type { Metadata } from "next";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import { getPage } from "@/lib/api";

type PageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const page = await getPage(slug);
  if (!page) return {};
  return {
    title: page.metaTitle || page.title,
    description: page.metaDescription || undefined,
    alternates: { canonical: page.canonicalUrl || `/${page.slug}` }
  };
}

export default async function ContentPage({ params }: PageProps) {
  const { slug } = await params;
  const page = await getPage(slug);
  if (!page) notFound();

  return (
    <main className="main">
      <article className="article">
        <h1>{page.title}</h1>
        <ReactMarkdown>{page.bodyMarkdown || ""}</ReactMarkdown>
      </article>
    </main>
  );
}
