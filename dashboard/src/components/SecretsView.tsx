"use client";

import { useMemo, useRef, useSyncExternalStore } from "react";
import { FiAlertCircle, FiCheck, FiExternalLink, FiMinus } from "react-icons/fi";
import type { Row, SecretSection } from "@/lib/secrets";
import { ago } from "@/lib/time";
import { PlatformIcon } from "./icons";

const onHash = (cb: () => void) => {
  window.addEventListener("hashchange", cb);
  return () => window.removeEventListener("hashchange", cb);
};
const readHash = () => decodeURIComponent(window.location.hash.slice(1));

export function SecretsView({ groups, settingsUrl }: { groups: SecretSection[][]; settingsUrl: string }) {
  const sections = useMemo(() => groups.flat(), [groups]);
  const hash = useSyncExternalStore(onHash, readHash, () => "");
  const panel = useRef<HTMLElement>(null);

  const select = (key: string) => {
    window.history.replaceState(null, "", `#${key}`);
    window.dispatchEvent(new Event("hashchange"));
    panel.current?.scrollTo({ top: 0 });
  };

  const sel = sections.find((s) => s.key === hash) ?? sections[0];

  return (
    <div className="flex-1 min-h-0 flex flex-col md:flex-row">
      <nav className="rail" aria-label="Sections">
        {groups.map((items, i) => (
          <ul key={i} className="rail-group">
            {items.map((it) => {
              const missing = it.rows.filter((r) => r.required && !r.present).length;
              return (
                <li key={it.key}>
                  <button type="button" className="rail-item" aria-current={it.key === sel?.key ? "true" : undefined} onClick={() => select(it.key)}>
                    {it.platform && <PlatformIcon platform={it.platform} className="rail-icon" />}
                    <span className="truncate">{it.label}</span>
                    {missing > 0 && <span className="dot dot-bad rail-dot" role="img" aria-label={`${missing} missing`} />}
                  </button>
                </li>
              );
            })}
          </ul>
        ))}
        <div className="rail-rule" role="separator" />
        <a className="rail-item" href={settingsUrl} target="_blank" rel="noreferrer">
          <FiExternalLink className="rail-icon" aria-hidden />
          <span className="truncate">GitHub settings</span>
        </a>
      </nav>

      <main ref={panel} className="flex-1 min-w-0 overflow-y-auto px-5 py-6 md:px-8">
        {sel ? (
          <section key={sel.key} className="max-w-[880px]" aria-labelledby="secrets-section">
            <h1 id="secrets-section" className="flex items-center gap-2.5 text-[20px] mb-3">
              {sel.platform && <PlatformIcon platform={sel.platform} className="text-[18px] text-ink-soft" />}
              {sel.label}
              {sel.note && <span className="text-[12px] font-normal text-slate">{sel.note}</span>}
            </h1>
            <div className="rounded-[10px] border border-line bg-card overflow-hidden">
              <table className="w-full text-[14px]">
                <tbody className="divide-y divide-line-soft">
                  {sel.rows.map((r) => (
                    <RowView key={r.name} row={r} />
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        ) : (
          <p className="text-ink-soft">No secrets or variables yet.</p>
        )}
      </main>
    </div>
  );
}

function Status({ row }: { row: Row }) {
  if (row.present) {
    const value = row.value ?? "";
    const shown = value.length > 60 ? `${value.slice(0, 57)}…` : value;
    return (
      <span className="inline-flex items-center gap-1.5">
        <FiCheck className="text-leaf shrink-0" aria-label="Set" />
        {row.type === "variable" ? (
          <span className="text-ink break-all" title={value.length > 60 ? value : undefined}>
            {shown}
          </span>
        ) : (
          <span className="text-ink-soft">{ago(row.updatedAt)}</span>
        )}
      </span>
    );
  }
  if (row.required) {
    return (
      <span className="inline-flex items-center gap-1.5 text-sindoor">
        <FiAlertCircle className="shrink-0" aria-hidden />
        Missing
      </span>
    );
  }
  return <FiMinus className="text-slate" aria-label="Not set" />;
}

function RowView({ row }: { row: Row }) {
  return (
    <tr className="align-middle">
      <td className="px-4 py-2.5">
        <div className="font-medium break-all">
          {row.name}
          {row.type === "variable" && <span className="ml-2 text-[11px] font-normal text-slate align-middle whitespace-nowrap">variable</span>}
        </div>
        <div className="text-[12px] text-slate">
          {row.hint}
          {row.link && (
            <a href={row.link} target="_blank" rel="noreferrer" className="ml-1.5 inline-flex align-middle hover:text-ink" aria-label={`Get ${row.name}`}>
              <FiExternalLink />
            </a>
          )}
        </div>
      </td>
      <td className="px-4 py-2.5 w-[32%] text-[13px]">
        <Status row={row} />
      </td>
    </tr>
  );
}
