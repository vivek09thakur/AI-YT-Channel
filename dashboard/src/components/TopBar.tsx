import Link from "next/link";
import type { ReactNode } from "react";
import type { Session } from "@/lib/auth";
import { NavMenu, type Section } from "./NavMenu";
import { ThemeToggle } from "./ThemeToggle";

export function TopBar({ session, current, summary }: { session: Session; current: Section; summary?: ReactNode }) {
  return (
    <header className="h-[60px] shrink-0 bg-inset border-b border-line text-[15px]">
      <div className="h-full flex items-center gap-4 px-5">
        <Link href="/" className="wordmark">
          AI YT Channel
        </Link>
        {summary && <p className="hidden md:block text-slate truncate border-l border-line pl-4">{summary}</p>}
        <div className="ml-auto flex items-center gap-2">
          <ThemeToggle />
          <NavMenu session={session} current={current} />
        </div>
      </div>
    </header>
  );
}
