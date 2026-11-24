import type { RunInfo, WorkflowInfo } from "@/lib/state";
import { fmtClock, fmtTime } from "@/lib/time";

export function stateText(wf: WorkflowInfo): string {
  switch (wf.state) {
    case "done":
      return "Done for today";
    case "running":
      return "Running now";
    case "failed":
      return `Failed${wf.latestRun ? ` at ${fmtTime(wf.latestRun.createdAt)}` : ""}`;
    case "paused":
      return "Paused";
    case "partial":
    case "waiting":
      return wf.nextSlot ? `Next run ${fmtClock(wf.nextSlot)}` : "No run left today";
    default:
      return "Nothing posted yet";
  }
}

export function stateDot(wf: WorkflowInfo): string {
  switch (wf.state) {
    case "done":
      return "dot dot-ok";
    case "running":
      return "dot dot-run";
    case "failed":
      return "dot dot-bad";
    default:
      return "dot";
  }
}

function stateClass(wf: WorkflowInfo): string {
  switch (wf.state) {
    case "done":
      return "state state-ok";
    case "running":
      return "state state-run";
    case "failed":
      return "state state-bad";
    default:
      return "state";
  }
}

function stateWord(wf: WorkflowInfo): string {
  switch (wf.state) {
    case "done":
      return "Done";
    case "running":
      return "Running";
    case "failed":
      return "Failed";
    case "paused":
      return "Paused";
    case "partial":
    case "waiting":
      return "Scheduled";
    default:
      return "To do";
  }
}

export function StateChip({ wf, long = false }: { wf: WorkflowInfo; long?: boolean }) {
  return <span className={stateClass(wf)}>{long ? stateText(wf) : stateWord(wf)}</span>;
}

export function RunState({ run: r }: { run: RunInfo }) {
  if (r.status !== "completed") return <span className="state state-run">{r.status === "queued" ? "Queued" : "Running"}</span>;
  if (r.conclusion === "success") return <span className="state state-ok">Success</span>;
  if (r.conclusion === "skipped") return <span className="state">Skipped</span>;
  if (r.conclusion === "cancelled") return <span className="state">Cancelled</span>;
  return <span className="state state-bad">{r.conclusion && r.conclusion !== "failure" ? r.conclusion : "Failed"}</span>;
}

export function runEvent(r: RunInfo): string {
  return r.event === "schedule" ? "scheduled" : r.event === "workflow_dispatch" ? "manual" : r.event;
}
