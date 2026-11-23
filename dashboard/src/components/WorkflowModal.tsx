"use client";

import { FiCheck, FiClock, FiX } from "react-icons/fi";
import { PLATFORMS } from "@/lib/model";
import type { AccountInfo, Posted, WorkflowInfo } from "@/lib/state";
import { fmtClock, fmtDay, fmtTime } from "@/lib/time";
import { Modal } from "./Modal";
import { RunState, StateChip, runEvent } from "./status";

export function UploadChips({ post, accounts }: { post: Posted; accounts: AccountInfo[] }) {
  if (post.uploads.length === 0) return <span className="chip chip-mute">Not uploaded</span>;
  return (
    <>
      {post.uploads.map((u) => {
        const acc = accounts.find((a) => a.key === u.accountKey);
        const label = `${PLATFORMS[u.platform].short} ${acc?.name ?? u.matrixName}${u.variant === "landscape" ? ", landscape" : ""}`;
        const cls = u.ok === null ? "chip-wait" : u.ok ? "chip-ok" : "chip-bad";
        return (
          <a key={u.jobUrl} href={u.jobUrl} target="_blank" rel="noreferrer" className={`chip ${cls} hover:underline`}>
            {u.ok === null ? <FiClock aria-label="Uploading" /> : u.ok ? <FiCheck aria-label="Uploaded" /> : <FiX aria-label="Upload failed" />} {label}
          </a>
        );
      })}
    </>
  );
}

export function WorkflowModal({ open, wf, accounts, onClose }: { open: boolean; wf: WorkflowInfo | null; accounts: AccountInfo[]; onClose: () => void }) {
  if (!wf) return null;

  const receivers = accounts.filter((a) => a.for === null || a.for.length === 0 || a.for.includes(wf.id));
  const unrecorded = receivers.some((a) => a.for === null);

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={wf.title}
      footer={
        <>
          <a className="btn" href={wf.actionsUrl} target="_blank" rel="noreferrer">
            Open on GitHub
          </a>
          {wf.issueUrl && (
            <a className="btn btn-danger" href={wf.issueUrl} target="_blank" rel="noreferrer">
              Failure issue
            </a>
          )}
        </>
      }
    >
      <div className="flex flex-col gap-5">
        <div className="flex items-center justify-between gap-3">
          <span className="text-[15px] tabular-nums">
            {wf.todayCount} of {wf.target} posted today
          </span>
          <StateChip wf={wf} />
        </div>
        <p className="text-[13px] text-ink-soft -mt-3">
          Due {wf.due.map(fmtClock).join(" and ")} IST. Tried every 30 minutes until the video is published, from {fmtClock(wf.slots[0] ?? "")} to {fmtClock(wf.slots.at(-1) ?? "")}; a slot only runs while a video due by then is still missing.
        </p>

        <section>
          <h3 className="text-[15px] mb-2">Today</h3>
          {wf.today.length === 0 ? (
            <p className="text-[14px] text-ink-soft">Nothing posted yet today.</p>
          ) : (
            <ul className="flex flex-col gap-2">
              {wf.today.map((p) => (
                <PostRow key={p.dir} post={p} accounts={accounts} />
              ))}
            </ul>
          )}
        </section>

        <section>
          <h3 className="text-[15px] mb-2">Posts to</h3>
          {receivers.length === 0 ? (
            <p className="text-[14px] text-sindoor">No account receives this workflow.</p>
          ) : (
            <>
              <ul className="flex flex-wrap gap-1.5">
                {receivers.map((a) => (
                  <li key={a.key} className={`chip ${!a.configured ? "chip-bad" : a.for === null ? "chip-mute" : "chip-ok"}`}>
                    {PLATFORMS[a.platform].short} {a.name}
                    {!a.configured && " (missing secrets)"}
                  </li>
                ))}
              </ul>
              {unrecorded && <p className="text-[13px] text-ink-soft mt-2">Grey accounts are not linked to any workflow yet, so they may or may not receive this one.</p>}
            </>
          )}
        </section>

        <section>
          <h3 className="text-[15px] mb-2">Recent runs</h3>
          {wf.runs.length === 0 ? (
            <p className="text-[14px] text-ink-soft">No runs yet.</p>
          ) : (
            <ul className="text-[14px] divide-y divide-line-soft">
              {wf.runs.map((r) => (
                <li key={r.id} className="flex items-center gap-3 py-1.5">
                  <span className="w-[132px] shrink-0 text-ink-soft whitespace-nowrap tabular-nums">
                    {fmtDay(r.createdAt)} {fmtTime(r.createdAt)}
                  </span>
                  <span className="flex-1 truncate">
                    #{r.number} <span className="text-slate">{runEvent(r)}</span>
                  </span>
                  <RunState run={r} />
                  <a href={r.url} target="_blank" rel="noreferrer" className="text-ink-soft hover:text-ink underline">
                    log
                  </a>
                </li>
              ))}
            </ul>
          )}
        </section>

        {wf.recent.length > 0 && (
          <section>
            <h3 className="text-[15px] mb-2">Earlier</h3>
            <ul className="flex flex-col gap-1 text-[14px]">
              {wf.recent.map((p) => (
                <li key={p.dir} className="flex items-center gap-3">
                  <span className="w-[132px] shrink-0 text-ink-soft whitespace-nowrap tabular-nums">{fmtDay(`${p.date}T12:00:00Z`)}</span>
                  <a href={p.videoUrl} className="truncate underline" target="_blank" rel="noreferrer">
                    {p.title}
                  </a>
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>
    </Modal>
  );
}

export function PostRow({ post, accounts }: { post: Posted; accounts: AccountInfo[] }) {
  return (
    <li className="rounded-[10px] bg-sunken px-3 py-2 text-[14px]">
      <div className="flex items-center gap-2">
        <a href={post.videoUrl} target="_blank" rel="noreferrer" className="font-medium truncate underline">
          {post.title}
        </a>
        <a href={post.runUrl} target="_blank" rel="noreferrer" className="ml-auto text-ink-soft shrink-0 hover:text-ink">
          run #{post.run}
        </a>
      </div>
      <div className="flex flex-wrap gap-1 mt-1.5">
        <UploadChips post={post} accounts={accounts} />
      </div>
    </li>
  );
}
