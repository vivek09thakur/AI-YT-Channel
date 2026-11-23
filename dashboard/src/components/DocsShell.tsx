import Link from "next/link";
import { Suspense, type ReactNode } from "react";
import { FiGithub } from "react-icons/fi";
import { getSession } from "@/lib/auth";
import { docHref, PAGES, type Heading } from "@/lib/docs";
import { NavMenu } from "./NavMenu";
import { ThemeToggle } from "./ThemeToggle";
import { Toc } from "./Toc";

const SCROLL_ID = "doc-scroll";

export function DocsShell({ slug, headings, children }: { slug: string; headings: Heading[]; children: ReactNode }) {
  const repo = process.env.GITHUB_REPO;
  return (
    <div className="h-dvh flex flex-col">
      <header className="h-[60px] shrink-0 bg-inset border-b border-line text-[15px]">
        <div className="h-full flex items-center gap-3 px-5">
          <Link href="/docs" className="wordmark">
            AI YT Channel
          </Link>
          <span className="text-slate">docs</span>
          <div className="ml-auto flex items-center gap-2">
            <ThemeToggle />
            <Suspense fallback={null}>
              <SessionMenu />
            </Suspense>
          </div>
        </div>
      </header>

      <div className="flex-1 min-h-0 flex flex-col md:flex-row">
        <nav className="rail" aria-label="Documentation">
          <ul className="rail-group">
            {PAGES.map((p) => (
              <li key={p.slug}>
                <Link href={docHref(p.slug)} className="rail-item" aria-current={p.slug === slug ? "true" : undefined}>
                  <span className="truncate">{p.title}</span>
                </Link>
              </li>
            ))}
          </ul>
          {headings.length > 0 && <Toc headings={headings} scrollId={SCROLL_ID} />}
          {repo && (
            <>
              <div className="rail-rule" role="separator" />
              <a className="rail-item" href={`https://github.com/${repo}`} target="_blank" rel="noreferrer">
                <FiGithub className="rail-icon" aria-hidden />
                <span className="truncate">Repository</span>
              </a>
            </>
          )}
        </nav>

        <main key={slug} id={SCROLL_ID} className="doc-scroll flex-1 min-w-0 overflow-y-auto px-5 py-7 md:px-10 md:py-9">
          <article className="doc">{children}</article>
        </main>
      </div>
    </div>
  );
}

async function SessionMenu() {
  const session = await getSession();
  if (!session) {
    return (
      <Link href="/login" className="btn">
        Sign in
      </Link>
    );
  }
  return <NavMenu session={session} current="docs" />;
}
