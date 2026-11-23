import type { WorkflowDef } from "./model";

// Decides, for one workflow, whether the external trigger should start a run right now. Pure: the route feeds it
// what it read from GitHub. Mirrors the guard job (pipeline/published_today.py --due): a run is wanted only while a
// video that is due by now is still missing, at most `target` a day, and only inside the hours the cron used to try.

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

/** From the first slot up to 30 minutes after the last one (the last slot was a retry too). */
export function inWindow(slotsIST: string[], nowIST: string) {
  const n = toMin(nowIST);
  return n >= toMin(slotsIST[0]) && n < toMin(slotsIST[slotsIST.length - 1]) + 30;
}

export function decide(def: WorkflowDef, f: Facts): Decision {
  const target = dueCount(def.dueIST, f.nowIST, def.target);
  const base = { workflow: def.id, file: def.file, published: f.publishedToday, target };
  const skip = (reason: string): Decision => ({ ...base, action: "skip", reason });

  if (!inWindow(def.slotsIST, f.nowIST)) {
    return skip(`outside the window (${def.slotsIST[0]} to ${def.slotsIST[def.slotsIST.length - 1]} IST)`);
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
