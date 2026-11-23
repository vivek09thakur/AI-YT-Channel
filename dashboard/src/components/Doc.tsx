import Link from "next/link";
import type { ComponentProps } from "react";
import ReactMarkdown, { type Components } from "react-markdown";
import rehypeSlug from "rehype-slug";
import remarkGfm from "remark-gfm";
import { publicImageSize } from "@/lib/docs";

function DocLink({ href = "", children }: ComponentProps<"a">) {
  if (href.startsWith("#")) return <a href={href}>{children}</a>;
  if (href.startsWith("/")) return <Link href={href}>{children}</Link>;
  return (
    <a href={href} target="_blank" rel="noreferrer">
      {children}
    </a>
  );
}

function DocImage({ src, alt }: ComponentProps<"img">) {
  const url = typeof src === "string" ? src : undefined;
  const size = url ? publicImageSize(url) : null;
  // Guide screenshots are plain files under public/guide, served as-is; the size comes from the file so the layout does not shift.
  // eslint-disable-next-line @next/next/no-img-element
  return <img src={url} alt={alt ?? ""} width={size?.width} height={size?.height} loading="lazy" />;
}

function DocTable({ children }: ComponentProps<"table">) {
  return (
    <div className="doc-table">
      <table>{children}</table>
    </div>
  );
}

const components: Components = { a: DocLink, img: DocImage, table: DocTable };

export function Doc({ markdown }: { markdown: string }) {
  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSlug]} components={components}>
      {markdown}
    </ReactMarkdown>
  );
}
