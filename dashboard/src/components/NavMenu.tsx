"use client";

import Link from "next/link";
import { useEffect, useId, useRef, useState } from "react";
import { FiActivity, FiBookOpen, FiGrid, FiKey, FiLogOut, FiMenu, FiX } from "react-icons/fi";
import { logout } from "@/app/actions";
import type { Session } from "@/lib/auth";

export type Section = "board" | "runs" | "secrets" | "docs";

const SECTIONS: { id: Section; href: string; label: string; Icon: typeof FiGrid }[] = [
  { id: "board", href: "/", label: "Board", Icon: FiGrid },
  { id: "runs", href: "/runs", label: "Runs", Icon: FiActivity },
  { id: "secrets", href: "/secrets", label: "Secrets", Icon: FiKey },
  { id: "docs", href: "/docs", label: "Docs", Icon: FiBookOpen },
];

export function NavMenu({ session, current }: { session: Session; current: Section }) {
  const [open, setOpen] = useState(false);
  const root = useRef<HTMLDivElement>(null);
  const panelId = useId();

  useEffect(() => {
    if (!open) return;
    const onDown = (e: PointerEvent) => {
      if (!root.current?.contains(e.target as Node)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("pointerdown", onDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("pointerdown", onDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  return (
    <div ref={root} className="relative flex items-center">
      <button type="button" className="btn btn-quiet btn-icon" aria-label="Menu" aria-expanded={open} aria-controls={panelId} onClick={() => setOpen((v) => !v)}>
        {open ? <FiX aria-hidden /> : <FiMenu aria-hidden />}
      </button>
      {open && (
        <div id={panelId} className="menu" role="menu">
          {SECTIONS.map(({ id, href, label, Icon }) => (
            <Link key={id} href={href} role="menuitem" className="menu-item" aria-current={current === id ? "page" : undefined} onClick={() => setOpen(false)}>
              <Icon aria-hidden /> {label}
            </Link>
          ))}
          <div className="menu-rule" role="separator" />
          <p className="menu-note">{session.user}</p>
          <form action={logout}>
            <button type="submit" role="menuitem" className="menu-item w-full">
              <FiLogOut aria-hidden /> Sign out
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
