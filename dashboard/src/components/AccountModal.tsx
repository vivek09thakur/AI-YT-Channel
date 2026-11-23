"use client";

import { ACCOUNT_FIELDS, LEGACY, WORKFLOWS, type FieldDef } from "@/lib/model";
import type { AccountInfo, Overview } from "@/lib/state";
import { ago } from "@/lib/time";
import { Modal } from "./Modal";

export function AccountModal({ open, account, overview, onClose }: { open: boolean; account: AccountInfo | null; overview: Overview; onClose: () => void }) {
  if (!account) return null;
  const { platform, legacy, key } = account;
  const fields: FieldDef[] = legacy ? LEGACY[platform].fields : ACCOUNT_FIELDS[platform];
  const present = new Map(account.fields.map((f) => [f.suffix, f]));
  const secretName = (suffix: string) => present.get(suffix)?.secretName ?? (legacy ? suffix : `${key}_${suffix}`);
  const groups = account.for === null ? null : account.for.length === 0 ? WORKFLOWS : WORKFLOWS.filter((w) => account.for!.includes(w.id));

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={account.name}
      footer={
        <>
          <a className="btn" href={`https://github.com/${overview.repo}/settings/secrets/actions`} target="_blank" rel="noreferrer">
            Open on GitHub
          </a>
          <button className="btn btn-quiet" onClick={onClose}>
            Close
          </button>
        </>
      }
    >
      <div className="flex flex-col gap-5 text-[14px]">
        <p className="text-[13px] text-ink-soft">
          {legacy ? (
            <>Old single-account secrets. The pipeline calls this account <strong>default</strong>.</>
          ) : (
            <>
              Secrets <strong>{key}_*</strong>. The pipeline calls it <strong>{account.matrixName}</strong>.
            </>
          )}
          {account.owner && <> Run by {account.owner}.</>}
          {platform === "youtube" && !legacy && (
            <>
              {" "}
              {overview.sharedYt ? "Shared OAuth client is set." : <span className="text-sindoor">Shared YT_CLIENT_ID / YT_CLIENT_SECRET are missing.</span>}
            </>
          )}
        </p>

        <section>
          <h3 className="text-[15px] mb-2">Posts videos from</h3>
          {groups === null ? (
            <p className="text-ink-soft">Not recorded yet. No recent run has posted here, and the {secretName("FOR")} value cannot be read back from GitHub.</p>
          ) : (
            <ul className="flex flex-wrap gap-1.5">
              {groups.map((w) => (
                <li key={w.id} className="chip">
                  {w.title}
                </li>
              ))}
            </ul>
          )}
          {account.forSource === "observed" && <p className="text-[13px] text-ink-soft mt-2">Taken from the upload jobs of recent runs.</p>}
          {platform === "youtube" && !legacy && <p className="text-[13px] text-ink-soft mt-2">Upload privacy: {account.privacy || "workflow default (public)"}.</p>}
        </section>

        <section>
          <h3 className="text-[15px] mb-2">Secrets</h3>
          <ul className="divide-y divide-line-soft">
            {fields
              .filter((f) => f.kind === "secret")
              .map((f) => {
                const state = present.get(f.suffix);
                const isSet = !!state?.present;
                const sharedOk = f.sharedFallback && overview.sharedYt;
                return (
                  <li key={f.suffix} className="flex items-center gap-3 py-2">
                    <span className="flex-1 min-w-0">
                      <span className="block truncate">{f.label}</span>
                      <span className="block text-[12px] text-slate truncate">{secretName(f.suffix)}</span>
                    </span>
                    {isSet ? (
                      <span className="state state-ok">Set, {ago(state?.updatedAt)}</span>
                    ) : sharedOk ? (
                      <span className="state">Uses shared {f.sharedFallback}</span>
                    ) : f.required ? (
                      <span className="state state-bad">Not set</span>
                    ) : (
                      <span className="state">Not set</span>
                    )}
                  </li>
                );
              })}
          </ul>
        </section>
      </div>
    </Modal>
  );
}
