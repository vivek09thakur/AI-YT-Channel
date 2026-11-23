import { FiAlertTriangle } from "react-icons/fi";
import type { Overview, WorkflowInfo } from "@/lib/state";
import { fmtClock, fmtDay, fmtDayLong, fmtTime } from "@/lib/time";
import { AutoRefresh } from "./AutoRefresh";
import { RunState, StateChip, runEvent } from "./status";
import { UploadChips } from "./WorkflowModal";

export function Runs({ overview }: { overview: Overview }) {
  const posted = overview.workflows.reduce((n, w) => n + w.todayCount, 0);
  const target = overview.workflows.reduce((n, w) => n + w.target, 0);

  return (
    <main className="flex-1 px-5 py-6 max-w-[960px] w-full mx-auto text-[14px]">
      <AutoRefresh />
      <header>
        <div className="flex items-baseline justify-between gap-3">
          <h1 className="text-[22px]">Runs</h1>
          <span className="text-[12px] text-slate whitespace-nowrap">
            {fmtDayLong(`${overview.date}T12:00:00Z`)}, {fmtClock(overview.nowIST)} IST
          </span>
        </div>
        <div className="mt-4 segments" role="img" aria-label={`${posted} of ${target} videos posted today`}>
          {Array.from({ length: target }, (_, i) => (
            <span key={i} className={i < posted ? "on" : ""} />
          ))}
        </div>
        <p className="mt-2 text-[12px] text-slate tabular-nums">
          {posted} of {target} videos posted today
        </p>
      </header>

      {overview.notes.length > 0 && (
        <section className="mt-5 rounded-[10px] border border-line p-3 text-[13px]">
          <h2 className="flex items-center gap-2 text-[14px] mb-1.5">
            <FiAlertTriangle className="text-amber shrink-0" aria-hidden /> Needs a look
          </h2>
          <ul className="flex flex-col gap-1.5 pl-6">
            {overview.notes.map((n) => (
              <li key={n}>{n}</li>
            ))}
          </ul>
        </section>
      )}

      <div className="mt-6 flex flex-col gap-4">
        {overview.workflows.map((wf) => (
          <WorkflowCard key={wf.id} wf={wf} overview={overview} />
        ))}
      </div>
    </main>
  );
}

function WorkflowCard({ wf, overview }: { wf: WorkflowInfo; overview: Overview }) {
  return (
    <section className="rounded-[10px] border border-line bg-card" aria-labelledby={`wf-${wf.id}`}>
      <header className="flex flex-wrap items-center gap-x-3 gap-y-2 px-4 py-3 border-b border-line-soft">
        <h2 id={`wf-${wf.id}`} className="text-[16px]">
          {wf.title}
        </h2>
        <StateChip wf={wf} long />
        <span className="text-[12px] text-slate tabular-nums">
          {wf.todayCount} of {wf.target} posted
        </span>
        <div className="ml-auto flex items-center gap-2">
          <a className="btn" href={wf.actionsUrl} target="_blank" rel="noreferrer">
            Open on GitHub
          </a>
          {wf.issueUrl && (
            <a className="btn btn-danger" href={wf.issueUrl} target="_blank" rel="noreferrer">
              Failure issue
            </a>
          )}
        </div>
      </header>

      <div className="grid md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-line-soft">
        <div className="px-4 py-4 min-w-0">
          <h3 className="text-[13px] text-slate mb-3">Today&rsquo;s videos</h3>
          {wf.today.length === 0 ? (
            <p className="text-ink-soft">Nothing posted yet today.</p>
          ) : (
            <ul className="flex flex-col gap-3">
              {wf.today.map((p) => (
                <li key={p.dir}>
                  <div className="flex items-center gap-2">
                    <a href={p.videoUrl} target="_blank" rel="noreferrer" className="truncate hover:underline">
                      {p.title}
                    </a>
                    <a href={p.runUrl} target="_blank" rel="noreferrer" className="ml-auto shrink-0 text-[12px] text-slate hover:text-ink hover:underline tabular-nums">
                      run #{p.run}
                    </a>
                  </div>
                  <div className="flex flex-wrap gap-1 mt-1">
                    <UploadChips post={p} accounts={overview.accounts} />
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="px-4 py-4 min-w-0">
          <h3 className="text-[13px] text-slate mb-3">Recent runs</h3>
          {wf.runs.length === 0 ? (
            <p className="text-ink-soft">No runs yet.</p>
          ) : (
            <ul className="divide-y divide-line-soft">
              {wf.runs.map((r) => (
                <li key={r.id} className="flex items-center gap-3 py-2">
                  <span className="w-[140px] shrink-0 font-mono text-[11.5px] text-ink-soft whitespace-nowrap">
                    {fmtDay(r.createdAt)} {fmtTime(r.createdAt)}
                  </span>
                  <a href={r.url} target="_blank" rel="noreferrer" className="flex-1 truncate hover:underline tabular-nums">
                    #{r.number} <span className="text-slate">{runEvent(r)}</span>
                  </a>
                  <RunState run={r} />
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </section>
  );
}
