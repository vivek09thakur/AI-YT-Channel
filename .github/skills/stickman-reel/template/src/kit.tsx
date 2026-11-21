import React from 'react';
import { spring, useCurrentFrame } from 'remotion';
import { C, FPS, SPRING } from './theme';
import { RMS, SPEAK } from './data';

export type SP = { t0: number; dur: number };
export const O = C.outline;

/** mouth opens only while `who` is inside a speaking window AND the voice is loud at this frame */
export const mouthOpen = (who: string, t: number) => {
  const w = SPEAK[who] || [];
  if (!w.some(([a, b]) => t >= a && t <= b)) return false;
  return (RMS[Math.floor(t * 30)] ?? 0) > 0.2;
};

/** f = local frame, t = absolute second, lf(sec) = local frame at which absolute second `sec` happens */
export const useT = (t0: number) => {
  const f = useCurrentFrame();
  return { f, t: t0 + f / FPS, lf: (s: number) => f - Math.round((s - t0) * FPS) };
};
export const sp = (frame: number, cfg = SPRING) => spring({ frame, fps: FPS, config: cfg });
export const breathe = (f: number, a = 1.5, p = 22) => Math.sin(f / p) * a;
export const blinkAt = (f: number) => f % 105 < 4;
/** 0..1 ramp between two local frames */
export const ramp = (f: number, a: number, b: number) => Math.max(0, Math.min(1, (f - a) / Math.max(1, b - a)));
/** shake offset, decays after local frame `at` */
export const shake = (f: number, at: number, amp = 8) => { const d = f - at; return d < 0 || d > 18 ? 0 : Math.sin(d * 2.1) * amp * (1 - d / 18); };

// ---------- backgrounds (full 540x960, ground line at y=620 where figures stand) ----------
export const GROUND = 620;

export const Flat: React.FC<{ color?: string; dots?: boolean }> = ({ color = C.paper, dots = true }) => (
  <>
    <rect width={540} height={960} fill={color} />
    {dots && <g fill="#00000012">{Array.from({ length: 10 }).map((_, i) => Array.from({ length: 16 }).map((__, j) => <circle key={`${i}${j}`} cx={27 + i * 54} cy={30 + j * 60} r={3} />))}</g>}
  </>
);

export const Spot: React.FC<{ color?: string; spot?: string; y?: number }> = ({ color = C.yellow, spot = '#ffffff66', y = 430 }) => (
  <>
    <rect width={540} height={960} fill={color} />
    <circle cx={270} cy={y} r={300} fill={spot} />
    <circle cx={270} cy={y} r={200} fill={spot} />
  </>
);

export const Sky: React.FC<{ f: number; sky?: string; ground?: string; clouds?: boolean; sun?: boolean }> = ({ f, sky = C.sky, ground = C.green, clouds = true, sun = false }) => (
  <>
    <rect width={540} height={960} fill={sky} />
    {sun && <g transform="translate(440,190)"><circle r={46} fill={C.yellow} stroke={O} strokeWidth={4} />{Array.from({ length: 8 }).map((_, i) => <line key={i} x1={0} y1={-56} x2={0} y2={-70} transform={`rotate(${i * 45 + f * 0.3})`} stroke={C.orange} strokeWidth={6} strokeLinecap="round" />)}</g>}
    {clouds && [[80, 170, 1], [330, 240, 0.8], [200, 140, 0.6]].map(([x, y, s], i) => (
      <g key={i} transform={`translate(${((x + f * (0.25 + i * 0.1)) % 700) - 80},${y}) scale(${s})`}>
        <ellipse cx={0} cy={0} rx={60} ry={26} fill={C.white} stroke={O} strokeWidth={4} />
        <circle cx={-20} cy={-14} r={26} fill={C.white} stroke={O} strokeWidth={4} />
        <circle cx={18} cy={-18} r={30} fill={C.white} stroke={O} strokeWidth={4} />
        <ellipse cx={0} cy={2} rx={58} ry={22} fill={C.white} />
        <circle cx={-20} cy={-14} r={23} fill={C.white} /><circle cx={18} cy={-18} r={27} fill={C.white} />
      </g>
    ))}
    <rect y={GROUND} width={540} height={960 - GROUND} fill={ground} />
    <line x1={0} y1={GROUND} x2={540} y2={GROUND} stroke={O} strokeWidth={5} />
  </>
);

export const Space: React.FC<{ f: number; color?: string; stars?: number }> = ({ f, color = C.night, stars = 40 }) => (
  <>
    <rect width={540} height={960} fill={color} />
    {Array.from({ length: stars }).map((_, i) => {
      const x = (i * 157) % 540, y = 80 + ((i * 233) % 800);
      return <circle key={i} cx={x} cy={y} r={1.6 + (i % 3)} fill={C.white} opacity={0.4 + 0.6 * Math.abs(Math.sin(f / 10 + i))} />;
    })}
  </>
);

export const Room: React.FC<{ wall?: string; floor?: string; window?: boolean }> = ({ wall = C.cream, floor = C.brown, window = true }) => (
  <>
    <rect width={540} height={960} fill={wall} />
    <rect y={GROUND} width={540} height={960 - GROUND} fill={floor} />
    <line x1={0} y1={GROUND} x2={540} y2={GROUND} stroke={O} strokeWidth={5} />
    {window && <g transform="translate(90,160)"><rect width={150} height={120} rx={8} fill={C.sky} stroke={O} strokeWidth={5} /><line x1={75} y1={0} x2={75} y2={120} stroke={O} strokeWidth={4} /><line x1={0} y1={60} x2={150} y2={60} stroke={O} strokeWidth={4} /></g>}
  </>
);

export const Stage3: React.FC<{ color?: string }> = ({ color = C.purple }) => (
  <>
    <rect width={540} height={960} fill={color} />
    <path d="M270 120 L40 620 L500 620 Z" fill="#ffffff22" />
    <rect y={GROUND} width={540} height={960 - GROUND} fill={C.navy} />
    <line x1={0} y1={GROUND} x2={540} y2={GROUND} stroke={O} strokeWidth={5} />
  </>
);

export const Ground: React.FC<{ color?: string }> = ({ color = C.green }) => (
  <>
    <rect y={GROUND} width={540} height={960 - GROUND} fill={color} />
    <line x1={0} y1={GROUND} x2={540} y2={GROUND} stroke={O} strokeWidth={5} />
  </>
);

/** Simple table/desk top at y (figures sit behind it with pose="sit", y = top + 90). */
export const Desk: React.FC<{ x?: number; y?: number; w?: number; color?: string }> = ({ x = 270, y = 540, w = 260, color = C.orange }) => (
  <g>
    <rect x={x - w / 2 + 14} y={y} width={16} height={GROUND - y} fill={C.brown} stroke={O} strokeWidth={4} />
    <rect x={x + w / 2 - 30} y={y} width={16} height={GROUND - y} fill={C.brown} stroke={O} strokeWidth={4} />
    <rect x={x - w / 2} y={y - 16} width={w} height={22} rx={6} fill={color} stroke={O} strokeWidth={4} />
  </g>
);

/** Whiteboard on legs; children drawn relative to the board's top-left (w x h). */
export const Board: React.FC<{ x: number; y: number; w?: number; h?: number; color?: string; k?: number; children?: React.ReactNode }> = ({ x, y, w = 260, h = 190, color = C.white, k = 1, children }) => (
  <g transform={`translate(${x},${y}) scale(${Math.max(0, Math.min(1, k))})`} opacity={Math.max(0, Math.min(1, k))}>
    <line x1={-w / 2 + 30} y1={h / 2} x2={-w / 2 + 10} y2={h / 2 + 110} stroke={O} strokeWidth={6} strokeLinecap="round" />
    <line x1={w / 2 - 30} y1={h / 2} x2={w / 2 - 10} y2={h / 2 + 110} stroke={O} strokeWidth={6} strokeLinecap="round" />
    <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={10} fill={color} stroke={O} strokeWidth={5} />
    <g transform={`translate(${-w / 2},${-h / 2})`}>{children}</g>
  </g>
);
