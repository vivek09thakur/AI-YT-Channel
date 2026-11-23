"use client";

import { Handle, Position, type Node, type NodeProps } from "@xyflow/react";
import { PLATFORMS, type Platform } from "@/lib/model";
import type { AccountInfo, WorkflowInfo } from "@/lib/state";
import { PlatformIcon } from "./icons";
import { stateDot, stateText } from "./status";

export type WfNode = Node<{ wf: WorkflowInfo }, "workflow">;
export type AccNode = Node<{ acc: AccountInfo }, "account">;
export type GhostNode = Node<{ platform: Platform; lane: string }, "ghost">;
export type LaneNode = Node<{ word: string; hint?: string }, "lane">;
export type JunctionNode = Node<Record<string, never>, "junction">;
export type BoardNode = WfNode | AccNode | GhostNode | LaneNode | JunctionNode;

export const WF_W = 260;
export const WF_H = 76;
export const ACC_W = 260;
export const ACC_H = 76;

export function WorkflowNode({ data }: NodeProps<WfNode>) {
  const { wf } = data;
  return (
    <div className="tile tile-workflow" role="button" aria-label={`${wf.title}: ${wf.todayCount} of ${wf.target} posted today, ${stateText(wf)}`}>
      <Handle type="source" position={Position.Right} />
      <div className="flex items-center justify-between gap-2">
        <span className="font-medium leading-5 truncate">{wf.title}</span>
        <span className={stateDot(wf)} aria-hidden />
      </div>
      <div className="flex items-center justify-between gap-2 text-[12px] text-slate tabular-nums">
        <span>
          {wf.todayCount} of {wf.target} posted
        </span>
        <span className="truncate">{stateText(wf)}</span>
      </div>
    </div>
  );
}

export function AccountNode({ data }: NodeProps<AccNode>) {
  const { acc } = data;
  const planned = !acc.configured && acc.fields.every((f) => !f.present);
  const status = acc.configured ? "Ready" : planned ? "Secrets missing" : `${acc.missing.length} secrets missing`;
  return (
    <div className="tile tile-account" role="button" aria-label={`${acc.name}, ${PLATFORMS[acc.platform].label}, ${status}`} title={status}>
      <Handle type="target" position={Position.Left} />
      <div className="flex items-center justify-between gap-2">
        <span className="font-medium leading-5 truncate">{acc.name}</span>
        <span className={`dot ${acc.configured ? "dot-ok" : "dot-bad"}`} aria-hidden />
      </div>
      <div className="flex items-center justify-between gap-2 text-[12px] text-slate">
        <span className="inline-flex items-center gap-1.5 min-w-0">
          <PlatformIcon platform={acc.platform} className="text-[14px] shrink-0" />
          <span className="font-mono text-[11.5px] truncate">{acc.legacy ? "legacy secrets" : acc.key}</span>
        </span>
        {!acc.configured && <span className="text-sindoor truncate">{status}</span>}
      </div>
    </div>
  );
}

export function GhostSlotNode({ data }: NodeProps<GhostNode>) {
  const label = PLATFORMS[data.platform].label;
  return (
    <div className="tile tile-ghost" aria-label={`${data.lane}: no ${label} account yet`}>
      <Handle type="target" position={Position.Left} />
      <span className="inline-flex items-center gap-1.5 text-[13px] font-medium">
        <PlatformIcon platform={data.platform} className="shrink-0" />
        No {label} account
      </span>
    </div>
  );
}

export function LaneLabelNode({ data }: NodeProps<LaneNode>) {
  return (
    <div className="lane-word" aria-hidden="true">
      <span>{data.word}</span>
      {data.hint && <span className="lane-hint">{data.hint}</span>}
    </div>
  );
}

export function JunctionNodeView() {
  return (
    <div className="lane-junction" aria-hidden="true">
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </div>
  );
}

export const nodeTypes = { workflow: WorkflowNode, account: AccountNode, ghost: GhostSlotNode, lane: LaneLabelNode, junction: JunctionNodeView };
