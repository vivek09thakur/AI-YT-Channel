import type { Overview } from "@/lib/state";
import { daySchedule, pct, type WindowSlot } from "@/lib/schedule";
import { fmtClock } from "@/lib/time";

function slotText(s: WindowSlot): string {
  const when = `${fmtClock(s.from)} to ${fmtClock(s.to)}`;
  switch (s.state) {
    case "posted":
      return `${when}: posted${s.at ? ` at ${fmtClock(s.at)}` : ""}${s.post ? `, ${s.post.title}` : ""}`;
    case "failed":
      return `${when}: ${s.attempts} ${s.attempts === 1 ? "attempt" : "attempts"} failed, nothing posted`;
    case "running":
      return `${when}: running now${s.at ? `, started ${fmtClock(s.at)}` : ""}`;
    case "open":
      return s.attempts ? `${when}: ${s.attempts} ${s.attempts === 1 ? "attempt" : "attempts"} failed so far, retrying` : `${when}: waiting for the first attempt`;
    case "ahead":
      return `${when}: later today`;
    default:
      return `${when}: no run happened`;
  }
}

export function DaySchedule({ overview, only }: { overview: Overview; only?: string }) {
  const sched = daySchedule(overview.workflows, overview.date, overview.nowIST);
  const rows = only ? sched.rows.filter((r) => r.wf.id === only) : sched.rows;
  const x = (hhmm: string) => `${pct(hhmm, sched.start, sched.end)}%`;

  return (
    <div className="sched" role="group" aria-label={only ? "Today's publishing windows" : "Today's publishing windows for every workflow"}>
      <div className="sched-row sched-axis" aria-hidden>
        <span />
        <div className="sched-track">
          {sched.hours.map((h) => (
            <span key={h} className="sched-hour" style={{ left: x(h) }} data-edge={h === sched.start ? "start" : h === sched.end ? "end" : undefined}>
              {fmtClock(h).replace(":00", "")}
            </span>
          ))}
        </div>
      </div>

      {rows.map(({ wf, windows }) => (
        <div key={wf.id} className="sched-row">
          {only ? (
            <span className="sched-name text-ink-soft">Today</span>
          ) : (
            <a href={`#${wf.id}`} className="sched-name">
              {wf.title}
            </a>
          )}
          <div className="sched-track" role="img" aria-label={`${wf.title}. ${windows.map(slotText).join(". ")}.`}>
            {sched.hours.map((h) => (
              <i key={h} className="sched-line" style={{ left: x(h) }} />
            ))}
            {windows.map((s) => {
              const href = s.post?.videoUrl ?? s.run?.url;
              const style = { left: x(s.from), width: `${pct(s.to, sched.start, sched.end) - pct(s.from, sched.start, sched.end)}%` };
              const dot = s.at && <b className="sched-dot" style={{ left: `${pct(s.at, s.from, s.to)}%` }} />;
              const cls = `sched-win is-${s.state}`;
              return href ? (
                <a key={s.from} className={cls} style={style} href={href} target="_blank" rel="noreferrer" title={slotText(s)}>
                  {dot}
                </a>
              ) : (
                <span key={s.from} className={cls} style={style} title={slotText(s)}>
                  {dot}
                </span>
              );
            })}
            {sched.now && <i className="sched-now" style={{ left: x(sched.now) }} />}
          </div>
        </div>
      ))}
    </div>
  );
}
