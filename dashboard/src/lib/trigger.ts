import type { WorkflowDef } from "./model";

// Decides, for one workflow, whether the external trigger should start a run right now. Pure: the route feeds it
// what it read from GitHub. Mirrors the guard job (pipeline/published_today.py --due): a run is wanted only while a
// video that is due by now is still missing, at most `target` a day, and only inside the workflow's hours.

/** A new run is not started while the previous one began less than this many minutes ago (the cron retried every 30). */
export const RETRY_SPACING_MIN = 25;

export type Facts = {
  nowIST: string;
  publishedToday: number;
  activeRunUrl?: string;
  lastRunStartedMinAgo?: number;
};

export type Decision = {
  workflow: WorkflowDef["id"];
  file: string;
  action: "dispatch" | "skip";
  reason: string;
  published: number;
  target: number;
};

export function toMin(hhmm: string) {
  return Number(hhmm.slice(0, 2)) * 60 + Number(hhmm.slice(3, 5));
}

/** How many videos should exist by now: the due times already passed, at least 1, at most `target`. */
export function dueCount(dueIST: string[], nowIST: string, target: number) {
  const passed = dueIST.filter((d) => d <= nowIST).length;
  return Math.max(1, Math.min(target, passed));
}

/** Inside one of the workflow's [from, to) ranges (morning and afternoon). */
export function inWindow(windowsIST: [string, string][], nowIST: string) {
  const n = toMin(nowIST);
  return windowsIST.some(([from, to]) => n >= toMin(from) && n < toMin(to));
}

export function decide(def: WorkflowDef, f: Facts): Decision {
  const target = dueCount(def.dueIST, f.nowIST, def.target);
  const base = { workflow: def.id, file: def.file, published: f.publishedToday, target };
  const skip = (reason: string): Decision => ({ ...base, action: "skip", reason });

  if (def.paused) return skip("paused in dashboard/src/lib/model.ts");
  if (!inWindow(def.windowsIST, f.nowIST)) {
    return skip(`outside the hours (${def.windowsIST.map(([a, b]) => `${a} to ${b}`).join(", ")} IST)`);
  }
  if (f.publishedToday >= target) {
    if (target >= def.target) return skip("daily target reached");
    const next = def.dueIST.find((d) => d > f.nowIST);
    return skip(next ? `nothing due yet, next at ${next} IST` : "nothing due yet");
  }
  if (f.activeRunUrl) return skip(`a run is already queued or in progress: ${f.activeRunUrl}`);
  if (f.lastRunStartedMinAgo !== undefined && f.lastRunStartedMinAgo < RETRY_SPACING_MIN) {
    return skip(`last run started ${f.lastRunStartedMinAgo} min ago, next try after ${RETRY_SPACING_MIN} min`);
  }
  return { ...base, action: "dispatch", reason: `${f.publishedToday} of ${target} due by now published` };
}
