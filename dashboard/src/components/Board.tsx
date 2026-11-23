"use client";

import { Background, BackgroundVariant, ReactFlow, ReactFlowProvider, useNodesInitialized, useReactFlow, type BuiltInEdge, type CoordinateExtent, type FitViewOptions } from "@xyflow/react";
import { useEffect, useMemo, useRef, useState } from "react";
import { PLATFORMS, type Platform } from "@/lib/model";
import type { AccountInfo, Overview } from "@/lib/state";
import { AccountModal } from "./AccountModal";
import { AutoRefresh } from "./AutoRefresh";
import { ACC_H, ACC_W, WF_H, nodeTypes, type BoardNode } from "./nodes";
import { WorkflowModal } from "./WorkflowModal";

const WF_X = 0;
const ACC_X = 440;
const TRUNK_X = 350;
const GAP = 16;
const LANE_PAD = 28;
/** How far past the outermost tiles the canvas may be panned. */
const EXTENT_PAD = 80;

type Selection = { kind: "workflow"; id: string } | { kind: "account"; key: string } | null;

const inert = { draggable: false, selectable: false, focusable: false, connectable: false } as const;
const FIT: FitViewOptions = { padding: "6%", maxZoom: 1 };
const solid = { style: { stroke: "var(--color-edge)" } };
const dashed = { style: { stroke: "var(--color-sindoor)", strokeDasharray: "6 5" } };

function laneHeight(slots: number) {
  return LANE_PAD * 2 + slots * ACC_H + (slots - 1) * GAP;
}

function Refit({ container }: { container: React.RefObject<HTMLDivElement | null> }) {
  const { fitView } = useReactFlow();
  const ready = useNodesInitialized();
  useEffect(() => {
    if (!ready) return;
    fitView(FIT);
    const el = container.current;
    if (!el) return;
    const ro = new ResizeObserver(() => fitView(FIT));
    ro.observe(el);
    return () => ro.disconnect();
  }, [ready, fitView, container]);
  return null;
}

export function Board(props: { overview: Overview }) {
  return (
    <ReactFlowProvider>
      <BoardInner {...props} />
    </ReactFlowProvider>
  );
}

function BoardInner({ overview }: { overview: Overview }) {
  const [sel, setSel] = useState<Selection>(null);
  const box = useRef<HTMLDivElement>(null);

  const { nodes, edges, extent } = useMemo(() => {
    const nodes: BoardNode[] = [];
    const edges: BuiltInEdge[] = [];
    let top = 0;

    const byPlatform = (list: AccountInfo[], p: Platform) => list.filter((a) => a.platform === p).sort((a, b) => a.key.localeCompare(b.key, undefined, { numeric: true }));

    overview.workflows.forEach((wf) => {
      const inLane = overview.accounts.filter((a) => a.for !== null && (a.for.length === 0 || a.for.includes(wf.id)));
      const slots: ({ acc: AccountInfo } | { ghost: Platform })[] = [];
      for (const p of Object.keys(PLATFORMS) as Platform[]) {
        const list = byPlatform(inLane, p);
        if (list.length) slots.push(...list.map((acc) => ({ acc })));
        else slots.push({ ghost: p });
      }
      const h = laneHeight(slots.length);
      const centerY = top + h / 2;
      const hasAccount = slots.some((s) => "acc" in s);
      const junction = `junction:${wf.id}`;

      nodes.push({ id: `wf:${wf.id}`, type: "workflow", position: { x: WF_X, y: centerY - WF_H / 2 }, data: { wf }, draggable: false });
      nodes.push({ id: junction, type: "junction", position: { x: TRUNK_X, y: centerY - 0.5 }, data: {}, ...inert });
      edges.push({ id: `e:${junction}`, source: `wf:${wf.id}`, target: junction, type: "straight", ...(hasAccount ? solid : dashed) });

      slots.forEach((slot, j) => {
        const y = top + LANE_PAD + j * (ACC_H + GAP);
        if ("acc" in slot) {
          const id = `acc:${slot.acc.key}@${wf.id}`;
          nodes.push({ id, type: "account", position: { x: ACC_X, y }, data: { acc: slot.acc }, draggable: false });
          edges.push({
            id: `e:${id}`,
            source: junction,
            target: id,
            type: "smoothstep",
            pathOptions: { borderRadius: 10, offset: 0, stepPosition: 0 },
            ...solid,
          });
        } else {
          const id = `ghost:${slot.ghost}@${wf.id}`;
          nodes.push({ id, type: "ghost", position: { x: ACC_X, y }, data: { platform: slot.ghost, lane: wf.lane }, ...inert });
          edges.push({
            id: `e:${id}`,
            source: junction,
            target: id,
            type: "smoothstep",
            pathOptions: { borderRadius: 10, offset: 0, stepPosition: 0 },
            ...dashed,
          });
        }
      });

      top += h;
    });

    const unlinked = overview.accounts.filter((a) => a.for === null);
    if (unlinked.length) {
      const slots = [...byPlatform(unlinked, "youtube"), ...byPlatform(unlinked, "instagram")];
      const h = laneHeight(slots.length);
      nodes.push({
        id: "lane:unlinked",
        type: "lane",
        position: { x: WF_X, y: top + h / 2 - 20 },
        data: { word: "Not linked yet", hint: "No recent run has posted here." },
        ...inert,
      });
      slots.forEach((acc, j) => {
        nodes.push({ id: `acc:${acc.key}@none`, type: "account", position: { x: ACC_X, y: top + LANE_PAD + j * (ACC_H + GAP) }, data: { acc }, draggable: false });
      });
      top += h;
    }

    const extent: CoordinateExtent = [
      [WF_X - EXTENT_PAD, -EXTENT_PAD],
      [ACC_X + ACC_W + EXTENT_PAD, top + EXTENT_PAD],
    ];

    return { nodes, edges, extent };
  }, [overview]);

  const selectedAccount = sel?.kind === "account" ? overview.accounts.find((a) => a.key === sel.key) ?? null : null;
  const selectedWorkflow = sel?.kind === "workflow" ? overview.workflows.find((w) => w.id === sel.id) ?? null : null;

  return (
    <div ref={box} className="relative flex-1 min-h-[420px]">
      <AutoRefresh />
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={FIT}
        minZoom={0.35}
        maxZoom={1.4}
        translateExtent={extent}
        nodesConnectable={false}
        elementsSelectable={false}
        edgesFocusable={false}
        panOnScroll
        proOptions={{ hideAttribution: false }}
        onNodeClick={(_, node) => {
          const [kind, rest] = node.id.split(":", 2);
          if (kind === "wf") setSel({ kind: "workflow", id: rest });
          else if (kind === "acc") setSel({ kind: "account", key: rest.split("@")[0] });
        }}
      >
        <Background variant={BackgroundVariant.Lines} gap={14} lineWidth={1} />
        <Refit container={box} />
      </ReactFlow>

      <AccountModal key={sel?.kind === "account" ? sel.key : "acc:none"} open={sel?.kind === "account"} account={selectedAccount} overview={overview} onClose={() => setSel(null)} />
      <WorkflowModal key={selectedWorkflow?.id ?? "wf:none"} open={!!selectedWorkflow} wf={selectedWorkflow} accounts={overview.accounts} onClose={() => setSel(null)} />
    </div>
  );
}
