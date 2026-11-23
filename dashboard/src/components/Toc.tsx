"use client";

import { useEffect, useState } from "react";
import type { Heading } from "@/lib/docs";

/** Section links for the current page; the one at the top of the scroll box is marked. */
export function Toc({ headings, scrollId }: { headings: Heading[]; scrollId: string }) {
  const [active, setActive] = useState(headings[0]?.id ?? "");

  useEffect(() => {
    const box = document.getElementById(scrollId);
    if (!box) return;
    const els = headings.map((h) => document.getElementById(h.id)).filter((e): e is HTMLElement => e !== null);
    let frame = 0;
    const update = () => {
      frame = 0;
      const top = box.getBoundingClientRect().top + 32;
      let cur = els[0]?.id ?? "";
      for (const el of els) {
        if (el.getBoundingClientRect().top <= top) cur = el.id;
        else break;
      }
      if (els.length && box.scrollTop + box.clientHeight >= box.scrollHeight - 2) cur = els[els.length - 1].id;
      setActive(cur);
    };
    const onScroll = () => {
      if (!frame) frame = requestAnimationFrame(update);
    };
    onScroll();
    box.addEventListener("scroll", onScroll, { passive: true });
    return () => {
      box.removeEventListener("scroll", onScroll);
      if (frame) cancelAnimationFrame(frame);
    };
  }, [headings, scrollId]);

  return (
    <ul className="rail-group rail-toc" aria-label="On this page">
      <li className="rail-label" aria-hidden>
        On this page
      </li>
      {headings.map((h) => (
        <li key={h.id}>
          <a className="rail-item" href={`#${h.id}`} aria-current={h.id === active ? "true" : undefined}>
            <span className="truncate">{h.text}</span>
          </a>
        </li>
      ))}
    </ul>
  );
}
