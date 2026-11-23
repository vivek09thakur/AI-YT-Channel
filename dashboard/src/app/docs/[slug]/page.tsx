import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Doc } from "@/components/Doc";
import { DocsShell } from "@/components/DocsShell";
import { findPage, PAGES, readDoc } from "@/lib/docs";

// The overview is served at /docs itself; the other pages are prerendered here and anything else is a 404.
export function generateStaticParams() {
  return PAGES.filter((p) => p.slug !== "overview").map((p) => ({ slug: p.slug }));
}

// The whole shell (rail highlight, table of contents) depends on the slug, so there is no URL-independent
// app shell to share between links. Each page is still a prerendered static file.
export const instant = false;

export async function generateMetadata({ params }: PageProps<"/docs/[slug]">): Promise<Metadata> {
  const { slug } = await params;
  const page = findPage(slug);
  return page ? { title: page.title, description: page.blurb } : {};
}

export default async function Page({ params }: PageProps<"/docs/[slug]">) {
  const { slug } = await params;
  const doc = slug === "overview" ? null : readDoc(slug);
  if (!doc) notFound();
  return (
    <DocsShell slug={slug} headings={doc.headings}>
      <Doc markdown={doc.markdown} />
    </DocsShell>
  );
}
