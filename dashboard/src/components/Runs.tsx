import type { ReactNode } from "react";
import { FiAlertTriangle } from "react-icons/fi";
import { PLATFORMS } from "@/lib/model";
import type { AccountInfo, Overview, Posted, RunInfo, UploadOutcome, WorkflowInfo } from "@/lib/state";
import { fmtClock, fmtDay, fmtDayLong, fmtDayTime, fmtDuration, fmtTime } from "@/lib/time";
import { AutoRefresh } from "./AutoRefresh";
import { DaySchedule } from "./DaySchedule";
import { RunState, StateChip, runEvent } from "./status";

export function Runs({ overview }: { overview: Overview }) {
  const posted = overview.workflows.reduce((n, w) => n + w.todayCount, 0);
  const target = overview.workflows.reduce((n, w) => n + w.target, 0);

  const runsToday = overview.workflows.reduce((n, w) => n + w.runStats.today.total, 0);
  const failedToday = overview.workflows.reduce((n, w) => n + w.runStats.today.failed, 0);
  const runningNow = overview.workflows.reduce((n, w) => n + w.runStats.today.running, 0);

  const upcoming = overview.workflows
    .filter((w) => w.nextSlot)
    .sort((a, b) => a.nextSlot!.localeCompare(b.nextSlot!))[0];

  const ready = overview.accounts.filter((a) => a.configured).length;
  const weekPosted = overview.workflows.reduce((n, w) => n + w.week.reduce((m, d) => m + d.count, 0), 0);
  const weekTarget = overview.workflows.reduce((n, w) => n + w.target * w.week.length, 0);

  return (
    <main className="flex-1 px-5 py-7 max-w-[960px] w-full mx-auto text-[14px]">
      <AutoRefresh />
      <header>
        <div className="flex items-baseline justify-between gap-3">
          <h1 className="text-[24px]">Runs</h1>
          <span className="text-[13px] text-slate whitespace-nowrap">
            {fmtDayLong(`${overview.date}T12:00:00Z`)}, {fmtClock(overview.nowIST)} IST
          </span>
        </div>

        <div className="mt-6">
          <DaySchedule overview={overview} />
        </div>

        <dl className="facts mt-9">
          <div>
            <dt>Runs today</dt>
            <dd className="tabular-nums">
              {runsToday === 0 ? "None yet" : runsToday}
              {failedToday > 0 && <span className="text-sindoor">, {failedToday} failed</span>}
              {runningNow > 0 && <span className="text-sky">, {runningNow} running</span>}
            </dd>
          </div>
          <div>
            <dt>Next run</dt>
            <dd>{upcoming ? `${fmtClock(upcoming.nextSlot!)}, ${upcoming.title}` : posted >= target ? "Done for today" : "No run left today"}</dd>
          </div>
          <div>
            <dt>Accounts ready</dt>
            <dd className="tabular-nums">
              {ready} of {overview.accounts.length}
              {ready < overview.accounts.length && <span className="text-sindoor">, {overview.accounts.length - ready} missing secrets</span>}
            </dd>
          </div>
          <div>
            <dt>Last 7 days</dt>
            <dd className="tabular-nums">
              {weekPosted} of {weekTarget} videos
            </dd>
          </div>
        </dl>
      </header>

      {overview.notes.length > 0 && (
        <section className="notice mt-8 px-5 py-4 text-[13px]">
          <h2 className="flex items-center gap-2 text-[14px] mb-2">
            <FiAlertTriangle className="text-amber shrink-0" aria-hidden /> Needs a look
          </h2>
          <ul className="flex flex-col gap-2 pl-6">
            {overview.notes.map((n) => (
              <li key={n}>{n}</li>
            ))}
          </ul>
        </section>
      )}

      <div className="mt-8 flex flex-col gap-6">
        {overview.workflows.map((wf) => (
          <WorkflowCard key={wf.id} wf={wf} overview={overview} />
        ))}
      </div>
    </main>
  );
}


function WeekBars({ wf, today }: { wf: WorkflowInfo; today: string }) {
  const total = wf.week.reduce((n, d) => n + d.count, 0);
  const target = wf.target * wf.week.length;
  return (
    <span className="inline-flex items-center gap-3">
      <span className="week" role="img" aria-label={`${total} of ${target} videos in the last 7 days`}>
        {wf.week.map((d) => {
          const share = Math.min(1, d.count / wf.target);
          const cls = [d.count > 0 ? "on" : "", d.date === today ? "today" : ""].join(" ").trim();
          return <span key={d.date} className={cls || undefined} style={{ height: `${Math.max(14, share * 100)}%` }} title={`${fmtDay(`${d.date}T12:00:00Z`)}: ${d.count} of ${wf.target}`} />;
        })}
      </span>
      <span className="tabular-nums">
        {total} of {target} videos this week
      </span>
    </span>
  );
}

function uploadName(u: UploadOutcome, accounts: AccountInfo[]) {
  const acc = accounts.find((a) => a.key === u.accountKey);
  return `${PLATFORMS[u.platform].short} ${acc?.name ?? u.matrixName}${u.variant === "landscape" ? " (landscape)" : ""}`;
}

function joinNames(parts: ReactNode[]) {
  return parts.flatMap((p, i) => (i === 0 ? [p] : i === parts.length - 1 ? [" and ", p] : [", ", p]));
}

/* One sentence per video: where it went, and anything that did not make it. */
function WentTo({ post, accounts }: { post: Posted; accounts: AccountInfo[] }) {
  if (post.uploads.length === 0) return <>Not uploaded anywhere.</>;
  const link = (u: UploadOutcome, cls = "") => (
    <a key={u.jobUrl} href={u.jobUrl} target="_blank" rel="noreferrer" className={`hover:underline ${cls}`.trim()}>
      {uploadName(u, accounts)}
    </a>
  );
  const ok = post.uploads.filter((u) => u.ok === true);
  const bad = post.uploads.filter((u) => u.ok === false);
  const wait = post.uploads.filter((u) => u.ok === null);
  return (
    <>
      {ok.length > 0 && <>Posted to {joinNames(ok.map((u) => link(u)))}. </>}
      {wait.length > 0 && <span className="text-sky">Still uploading to {joinNames(wait.map((u) => link(u, "text-sky")))}. </span>}
      {bad.length > 0 && <span className="text-sindoor">Upload failed for {joinNames(bad.map((u) => link(u, "text-sindoor")))}.</span>}
    </>
  );
}

function RunOutcome({ run }: { run: RunInfo }) {
  if (run.status === "completed" && run.conclusion === "success") return <span className="state">Success</span>;
  return <RunState run={run} />;
}

function Empty({ wf }: { wf: WorkflowInfo }) {
  if (wf.state === "failed" && wf.latestRun) {
    return (
      <p className="text-ink-soft">
        Nothing posted yet today. The run at {fmtTime(wf.latestRun.createdAt)} failed;{" "}
        <a href={wf.latestRun.url} target="_blank" rel="noreferrer" className="text-ink underline">
          open the log
        </a>{" "}
        to see why.
      </p>
    );
  }
  if (wf.state === "running") return <p className="text-ink-soft">Nothing posted yet today. A run is going now.</p>;
  if (wf.nextSlot) return <p className="text-ink-soft">Nothing posted yet today. The next attempt is at {fmtClock(wf.nextSlot)}.</p>;
  return <p className="text-ink-soft">Nothing posted today, and no run is left.</p>;
}

function WorkflowCard({ wf, overview }: { wf: WorkflowInfo; overview: Overview }) {
  const { runStats } = wf;
  const runAt = (p: Posted) => wf.todayRuns.find((r) => r.number === p.run)?.createdAt ?? null;
  // Morning first, so the log reads in the same direction as the day schedule above.
  const todayLog = [...wf.today].sort((a, b) => (runAt(a) ?? "").localeCompare(runAt(b) ?? "") || a.run - b.run);
  const plural = (n: number, word: string) => `${n} ${word}${n === 1 ? "" : "s"}`;
  const summary =
    runStats.completed === 0
      ? "No finished runs yet"
      : `${plural(runStats.completed, "recent run")}, ${runStats.ok} succeeded${runStats.failed ? `, ${runStats.failed} failed` : ""}${
          runStats.typicalSec !== null ? `, usually ${fmtDuration(runStats.typicalSec)}` : ""
        }`;

  return (
    <section className="rounded-[10px] border border-line bg-card" aria-labelledby={`wf-${wf.id}`}>
      <header className="flex flex-wrap items-center gap-x-4 gap-y-2 px-6 pt-5">
        <h2 id={`wf-${wf.id}`} className="text-[18px]">
          {wf.title}
        </h2>
        <StateChip wf={wf} long />
        <div className="ml-auto flex items-center gap-1 -mr-3">
          <a className="btn btn-quiet" href={wf.actionsUrl} target="_blank" rel="noreferrer">
            Open on GitHub
          </a>
          {wf.issueUrl && (
            <a className="btn btn-quiet btn-danger" href={wf.issueUrl} target="_blank" rel="noreferrer">
              Failure issue
            </a>
          )}
        </div>
      </header>

      <div className="px-6 pt-5 pb-6">
        {wf.today.length === 0 ? (
          <Empty wf={wf} />
        ) : (
          <ol className="log">
            {todayLog.map((p) => {
              const at = runAt(p);
              return (
                <li key={p.dir}>
                  <span className="log-when">{at ? fmtTime(at) : `run #${p.run}`}</span>
                  <div className="min-w-0">
                    <a href={p.videoUrl} target="_blank" rel="noreferrer" className="block text-[15px] text-ink hover:underline">
                      {p.title}
                    </a>
                    <p className="mt-1 text-[13px] text-ink-soft">
                      <WentTo post={p} accounts={overview.accounts} />
                    </p>
                  </div>
                </li>
              );
            })}
          </ol>
        )}
      </div>

      <footer className="border-t border-line-soft px-6 py-4 text-[13px] text-ink-soft">
        <WeekBars wf={wf} today={overview.date} />
        <details className="history mt-3" open={wf.state === "failed" || undefined}>
          <summary>{summary}</summary>
          {wf.runs.length > 0 && (
            <ol className="log log-runs mt-3">
              {wf.runs.map((r) => (
                <li key={r.id}>
                  <span className="log-when">{fmtDayTime(r.createdAt)}</span>
                  <a href={r.url} target="_blank" rel="noreferrer" className="truncate text-ink hover:underline tabular-nums">
                    #{r.number} <span className="text-slate">{runEvent(r)}</span>
                  </a>
                  <span className="hidden sm:inline tabular-nums whitespace-nowrap">{fmtDuration(r.durationSec)}</span>
                  <RunOutcome run={r} />
                </li>
              ))}
            </ol>
          )}
        </details>
      </footer>
    </section>
  );
}