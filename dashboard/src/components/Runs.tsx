import { FiAlertTriangle } from "react-icons/fi";
import type { Overview, WorkflowInfo } from "@/lib/state";
import { fmtClock, fmtDay, fmtDayLong, fmtDuration, fmtTime } from "@/lib/time";
import { AutoRefresh } from "./AutoRefresh";
import { RunState, StateChip, runEvent } from "./status";
import { UploadChips } from "./WorkflowModal";

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
        <div className="mt-4 segments" role="img" aria-label={`${posted} of ${target} videos posted today`}>
          {Array.from({ length: target }, (_, i) => (
            <span key={i} className={i < posted ? "on" : ""} />
          ))}
        </div>
        <p className="mt-2 text-[13px] text-slate tabular-nums">
          {posted} of {target} videos posted today
        </p>

        <dl className="facts mt-8">
          <div>
            <dt>Runs today</dt>
            <dd className="tabular-nums">
              {runsToday === 0 ? "None yet" : runsToday}
              {failedToday > 0 && <span className="text-sindoor">, {failedToday} failed</span>}
              {runningNow > 0 && <span className="text-leaf">, {runningNow} running</span>}
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
        <section className="mt-8 rounded-[10px] border border-line px-5 py-4 text-[13px]">
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
  return (
    <span className="inline-flex items-center gap-3">
      <span className="week" role="img" aria-label={`${total} of ${wf.target * wf.week.length} videos in the last 7 days`}>
        {wf.week.map((d) => {
          const share = Math.min(1, d.count / wf.target);
          const cls = [d.count > 0 ? "on" : "", d.date === today ? "today" : ""].join(" ").trim();
          return <span key={d.date} className={cls || undefined} style={{ height: `${Math.max(14, share * 100)}%` }} title={`${fmtDay(`${d.date}T12:00:00Z`)}: ${d.count} of ${wf.target}`} />;
        })}
      </span>
      <span className="tabular-nums">
        {total} of {wf.target * wf.week.length}
      </span>
    </span>
  );
}

function WorkflowCard({ wf, overview }: { wf: WorkflowInfo; overview: Overview }) {
  const { runStats } = wf;
  return (
    <section className="rounded-[10px] border border-line bg-card" aria-labelledby={`wf-${wf.id}`}>
      <header className="flex flex-wrap items-center gap-x-4 gap-y-2 px-6 py-4 border-b border-line-soft">
        <h2 id={`wf-${wf.id}`} className="text-[17px]">
          {wf.title}
        </h2>
        <StateChip wf={wf} long />
        <span className="text-[13px] text-slate tabular-nums">
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

      <dl className="facts px-6 py-5 border-b border-line-soft">
        <div>
          <dt>Due</dt>
          <dd>{wf.due.map(fmtClock).join(" and ")}</dd>
        </div>
        <div>
          <dt>Recent runs</dt>
          <dd className="tabular-nums">
            {runStats.completed === 0 ? (
              "No finished runs yet"
            ) : (
              <>
                {runStats.ok} of {runStats.completed} succeeded
                {runStats.failed > 0 && <span className="text-sindoor">, {runStats.failed} failed</span>}
              </>
            )}
          </dd>
        </div>
        <div>
          <dt>Typical run</dt>
          <dd>{runStats.typicalSec === null ? "Unknown" : fmtDuration(runStats.typicalSec)}</dd>
        </div>
        <div>
          <dt>Last 7 days</dt>
          <dd>
            <WeekBars wf={wf} today={overview.date} />
          </dd>
        </div>
      </dl>

      <div className="grid md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-line-soft">
        <div className="px-6 py-5 min-w-0">
          <h3 className="text-[13px] text-slate mb-4">Today&rsquo;s videos</h3>
          {wf.today.length === 0 ? (
            <p className="text-ink-soft">Nothing posted yet today.</p>
          ) : (
            <ul className="flex flex-col gap-5">
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
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    <UploadChips post={p} accounts={overview.accounts} />
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="px-6 py-5 min-w-0">
          <h3 className="text-[13px] text-slate mb-3">Recent runs</h3>
          {wf.runs.length === 0 ? (
            <p className="text-ink-soft">No runs yet.</p>
          ) : (
            <ul className="divide-y divide-line-soft">
              {wf.runs.slice(0, 5).map((r) => (
                <li key={r.id} className="flex flex-wrap items-center gap-x-3 gap-y-1 py-2.5">
                  <span className="sm:w-[140px] shrink-0 font-mono text-[11.5px] text-ink-soft whitespace-nowrap">
                    {fmtDay(r.createdAt)} {fmtTime(r.createdAt)}
                  </span>
                  <a
                    href={r.url}
                    target="_blank"
                    rel="noreferrer"
                    className="order-last basis-full sm:order-none sm:basis-0 sm:flex-1 truncate hover:underline tabular-nums"
                  >
                    #{r.number} <span className="text-slate">{runEvent(r)}</span>
                  </a>
                  {r.durationSec !== null && (
                    <span className="ml-auto sm:ml-0 text-[12px] text-slate whitespace-nowrap tabular-nums">{fmtDuration(r.durationSec)}</span>
                  )}
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
