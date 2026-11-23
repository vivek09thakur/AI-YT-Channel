"use client";

import { useEffect, useRef, type ReactNode } from "react";
import { FiExternalLink } from "react-icons/fi";
import { setHash, useHash } from "./useHash";

export type RunsSection = {
  key: string;
  label: string;
  /** Red when the workflow failed today, blue while it is running; nothing otherwise. */
  dot?: "bad" | "run";
  node: ReactNode;
};

/** The Runs page frame: a rail of sections on the left, the chosen one on the right. */
export function RunsShell({ today, workflows, actionsUrl }: { today: RunsSection; workflows: RunsSection[]; actionsUrl: string }) {
  const hash = useHash();
  const panel = useRef<HTMLElement>(null);
  const sel = workflows.find((s) => s.key === hash) ?? today;

  useEffect(() => {
    panel.current?.scrollTo({ top: 0 });
  }, [sel.key]);

  const item = (s: RunsSection) => (
    <li key={s.key}>
      <button type="button" className="rail-item" aria-current={s.key === sel.key ? "true" : undefined} onClick={() => setHash(s.key)}>
        <span className="truncate">{s.label}</span>
        {s.dot === "bad" && <span className="dot dot-bad rail-dot" role="img" aria-label="Failed today" />}
        {s.dot === "run" && <span className="dot dot-run rail-dot" role="img" aria-label="Running now" />}
      </button>
    </li>
  );

  return (
    <div className="flex-1 min-h-0 flex flex-col md:flex-row">
      <nav className="rail" aria-label="Sections">
        <ul className="rail-group">{item(today)}</ul>
        <ul className="rail-group">{workflows.map(item)}</ul>
        <div className="rail-rule" role="separator" />
        <a className="rail-item" href={actionsUrl} target="_blank" rel="noreferrer">
          <FiExternalLink className="rail-icon" aria-hidden />
          <span className="truncate">Actions on GitHub</span>
        </a>
      </nav>

      <main ref={panel} className="flex-1 min-w-0 overflow-y-auto px-5 py-7 md:px-8 text-[14px]">
        <div key={sel.key} className="max-w-[880px]">
          {sel.node}
        </div>
      </main>
    </div>
  );
}
