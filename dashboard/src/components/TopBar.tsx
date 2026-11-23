import Link from "next/link";
import type { ReactNode } from "react";
import type { Session } from "@/lib/auth";
import { NavMenu, type Section } from "./NavMenu";
import { ThemeToggle } from "./ThemeToggle";

export function TopBar({ session, current, summary }: { session: Session; current: Section; summary?: ReactNode }) {
  return (
    <header className="h-[52px] shrink-0 bg-inset border-b border-line text-[14px]">
      <div className="h-full flex items-center gap-3 px-4">
        <Link href="/" className="wordmark">
          AI YT Channel
        </Link>
        {summary && <p className="hidden md:block text-slate truncate border-l border-line pl-3">{summary}</p>}
        <div className="ml-auto flex items-center gap-1">
          <ThemeToggle />
          <NavMenu session={session} current={current} />
        </div>
      </div>
    </header>
  );
}
