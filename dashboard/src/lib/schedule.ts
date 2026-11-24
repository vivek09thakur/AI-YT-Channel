import type { Posted, RunInfo, WorkflowInfo } from "./state";

export type WindowState = "posted" | "failed" | "running" | "open" | "ahead" | "missed" | "paused";

export type WindowSlot = {
  from: string;
  to: string;
  state: WindowState;
  /** IST clock of the run that decided the state, clamped into the window for drawing. */
  at: string | null;
  post: Posted | null;
  run: RunInfo | null;
  attempts: number;
};

export type DaySchedule = {
  start: string;
  end: string;
  hours: string[];
  now: string | null;
  rows: { wf: WorkflowInfo; windows: WindowSlot[] }[];
};

const IST_OFFSET_MIN = 330;
const GRACE_MIN = 30;

export function toMin(hhmm: string): number {
  return Number(hhmm.slice(0, 2)) * 60 + Number(hhmm.slice(3, 5));
}

export function toClock(min: number): string {
  const m = ((min % 1440) + 1440) % 1440;
  return `${String(Math.floor(m / 60)).padStart(2, "0")}:${String(m % 60).padStart(2, "0")}`;
}

export function istClock(iso: string): string {
  const t = new Date(Date.parse(iso) + IST_OFFSET_MIN * 60_000);
  return toClock(t.getUTCHours() * 60 + t.getUTCMinutes());
}

/** Position of a clock inside [start, end] as a 0..100 percentage. */
export function pct(hhmm: string, start: string, end: string): number {
  const span = toMin(end) - toMin(start);
  return Math.min(100, Math.max(0, ((toMin(hhmm) - toMin(start)) / span) * 100));
}

function clamp(hhmm: string, from: string, to: string): string {
  const m = Math.min(toMin(to), Math.max(toMin(from), toMin(hhmm)));
  return toClock(m);
}

function inWindow(hhmm: string, from: string, to: string, grace = GRACE_MIN): boolean {
  const m = toMin(hhmm);
  return m >= toMin(from) && m < toMin(to) + grace;
}

function isFailure(r: RunInfo): boolean {
  return r.status === "completed" && r.conclusion !== "success" && r.conclusion !== "skipped" && r.conclusion !== "cancelled";
}

export function windowSlots(wf: WorkflowInfo, today: string, now: string): WindowSlot[] {
  const runs = wf.todayRuns.filter((r) => r.createdAt.slice(0, 10) === today);
  const byNumber = new Map(runs.map((r) => [r.number, r]));
  const slots: WindowSlot[] = wf.windows.map(([from, to]) => ({ from, to, state: "ahead", at: null, post: null, run: null, attempts: 0 }));

  const posts = [...wf.today].sort((a, b) => a.run - b.run);
  const unplaced: Posted[] = [];
  for (const p of posts) {
    const run = byNumber.get(p.run) ?? null;
    const at = run ? istClock(run.createdAt) : null;
    const slot = (at && slots.find((s) => !s.post && inWindow(at, s.from, s.to, 60))) ?? null;
    if (slot) {
      slot.state = "posted";
      slot.post = p;
      slot.run = run;
      slot.at = clamp(at!, slot.from, slot.to);
    } else unplaced.push(p);
  }
  for (const p of unplaced) {
    const slot = slots.find((s) => !s.post);
    if (!slot) break;
    const run = byNumber.get(p.run) ?? null;
    slot.state = "posted";
    slot.post = p;
    slot.run = run;
    slot.at = run ? clamp(istClock(run.createdAt), slot.from, slot.to) : slot.from;
  }

  for (const s of slots) {
    const inside = runs.filter((r) => inWindow(istClock(r.createdAt), s.from, s.to));
    s.attempts = inside.length;
    if (s.post) continue;
    const live = inside.find((r) => r.status !== "completed");
    const failed = inside.filter(isFailure);
    const last = failed.at(0) ?? null;
    if (live) {
      s.state = "running";
      s.run = live;
      s.at = clamp(istClock(live.createdAt), s.from, s.to);
    } else if (toMin(now) < toMin(s.from)) {
      s.state = "ahead";
    } else if (toMin(now) < toMin(s.to)) {
      s.state = "open";
      if (last) {
        s.run = last;
        s.at = clamp(istClock(last.createdAt), s.from, s.to);
      }
    } else if (last) {
      s.state = "failed";
      s.run = last;
      s.at = clamp(istClock(last.createdAt), s.from, s.to);
    } else {
      s.state = "missed";
    }
    // A paused workflow has no attempts to wait for or miss; only what a manual run produced is shown.
    if (wf.paused && (s.state === "ahead" || s.state === "open" || s.state === "missed")) s.state = "paused";
  }
  return slots;
}

export function daySchedule(workflows: WorkflowInfo[], today: string, now: string): DaySchedule {
  const froms = workflows.flatMap((w) => w.windows.map(([f]) => toMin(f)));
  const tos = workflows.flatMap((w) => w.windows.map(([, t]) => toMin(t)));
  const startMin = Math.floor((Math.min(...froms) - 60) / 60) * 60;
  const endMin = Math.ceil((Math.max(...tos) + 60) / 60) * 60;
  const start = toClock(startMin);
  const end = toClock(endMin);
  const hours: string[] = [];
  for (let m = startMin; m <= endMin; m += 180) hours.push(toClock(m));
  const nowMin = toMin(now);
  return {
    start,
    end,
    hours,
    now: nowMin >= startMin && nowMin <= endMin ? now : null,
    rows: workflows.map((wf) => ({ wf, windows: windowSlots(wf, today, now) })),
  };
}
