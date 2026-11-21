import React from 'react';
import { interpolate, spring, useCurrentFrame } from 'remotion';
import { C, FPS, SPRING, BOUNCY, clamp } from './theme';

const O = C.outline;
const k01 = (k: number) => Math.max(0, Math.min(1, k));
/** spring 0..1 that starts at local frame `at` (use lf(sec) from useT) */
export const pop = (f: number, at = 0, cfg = SPRING) => spring({ frame: f - at, fps: FPS, config: cfg });

// ---------- text ----------
/** Big doodle headline with a coloured shadow block. `k` = pop spring. */
export const Big: React.FC<{ x: number; y: number; text: string; k?: number; size?: number; color?: string; fill?: string; w?: number; font?: 'Baloo' | 'Hand' }> = ({ x, y, text, k = 1, size = 54, color = C.yellow, fill = C.ink, w, font = 'Baloo' }) => {
  const width = w ?? Math.max(120, text.length * size * 0.58 + 40);
  return (
    <g transform={`translate(${x},${y}) scale(${0.6 + 0.4 * k01(k)})`} opacity={k01(k)}>
      <rect x={-width / 2 + 7} y={-size * 0.72 + 7} width={width} height={size * 1.3} rx={16} fill={O} />
      <rect x={-width / 2} y={-size * 0.72} width={width} height={size * 1.3} rx={16} fill={color} stroke={O} strokeWidth={4} />
      <text x={0} y={size * 0.33} textAnchor="middle" fontFamily={font} fontWeight={800} fontSize={size} fill={fill}>{text}</text>
    </g>
  );
};

/** Handwritten label (Patrick Hand), no box. */
export const Label: React.FC<{ x: number; y: number; text: string; k?: number; size?: number; color?: string; anchor?: 'start' | 'middle' | 'end'; rot?: number }> = ({ x, y, text, k = 1, size = 28, color = C.ink, anchor = 'middle', rot = 0 }) => (
  <text x={x} y={y} textAnchor={anchor} fontFamily="Hand" fontSize={size} fill={color} opacity={k01(k)} transform={`rotate(${rot} ${x} ${y})`}>{text}</text>
);

/** Card with optional title; children are drawn relative to the card's top-left. */
export const Card: React.FC<{ x: number; y: number; w: number; h: number; k?: number; color?: string; title?: string; children?: React.ReactNode; rot?: number }> = ({ x, y, w, h, k = 1, color = C.white, title, children, rot = 0 }) => (
  <g transform={`translate(${x + w / 2},${y + h / 2}) rotate(${rot}) scale(${0.7 + 0.3 * k01(k)}) translate(${-w / 2},${-h / 2})`} opacity={k01(k)}>
    <rect x={8} y={8} width={w} height={h} rx={18} fill={O} />
    <rect width={w} height={h} rx={18} fill={color} stroke={O} strokeWidth={4} />
    {title && <text x={w / 2} y={38} textAnchor="middle" fontFamily="Baloo" fontWeight={700} fontSize={26} fill={C.ink}>{title}</text>}
    {children}
  </g>
);

/** Number that counts from..to as k goes 0..1 (use interpolate(lf, [a,b], [0,1], clamp) for k). */
export const Counter: React.FC<{ x: number; y: number; from?: number; to: number; k: number; size?: number; suffix?: string; prefix?: string; color?: string; decimals?: number }> = ({ x, y, from = 0, to, k, size = 72, suffix = '', prefix = '', color = C.ink, decimals = 0 }) => {
  const v = from + (to - from) * k01(k);
  return <text x={x} y={y} textAnchor="middle" fontFamily="Baloo" fontWeight={800} fontSize={size} fill={color}>{prefix}{v.toLocaleString('en-US', { maximumFractionDigits: decimals, minimumFractionDigits: decimals })}{suffix}</text>;
};

// ---------- speech ----------
export const Bubble: React.FC<{ x: number; y: number; text: string; k?: number; w?: number; tail?: 'l' | 'r' | 'none'; color?: string; size?: number }> = ({ x, y, text, k = 1, w, tail = 'l', color = C.white, size = 26 }) => {
  const lines = text.split('\n');
  const width = w ?? Math.max(60, Math.max(...lines.map((l) => l.length)) * size * 0.55 + 36);
  const h = lines.length * size * 1.2 + 22;
  return (
    <g transform={`translate(${x},${y}) scale(${k01(k)})`} opacity={k01(k)}>
      <rect x={-width / 2} y={-h / 2} width={width} height={h} rx={h / 2} fill={color} stroke={O} strokeWidth={4} />
      {tail !== 'none' && <path d={tail === 'l' ? `M${-width / 4} ${h / 2 - 6} L${-width / 4 - 14} ${h / 2 + 22} L${-width / 4 + 22} ${h / 2 - 4} Z` : `M${width / 4} ${h / 2 - 6} L${width / 4 + 14} ${h / 2 + 22} L${width / 4 - 22} ${h / 2 - 4} Z`} fill={color} stroke={O} strokeWidth={4} strokeLinejoin="round" />}
      {tail !== 'none' && <rect x={tail === 'l' ? -width / 4 - 4 : width / 4 - 18} y={h / 2 - 9} width={22} height={8} fill={color} />}
      {lines.map((l, i) => <text key={i} x={0} y={-h / 2 + 14 + (i + 0.85) * size * 1.2} textAnchor="middle" fontFamily="Baloo" fontWeight={700} fontSize={size} fill={C.ink}>{l}</text>)}
    </g>
  );
};

export const Thought: React.FC<{ x: number; y: number; k?: number; w?: number; h?: number; children?: React.ReactNode; tail?: 'l' | 'r' }> = ({ x, y, k = 1, w = 150, h = 100, children, tail = 'l' }) => {
  const f = useCurrentFrame();
  const tx = tail === 'l' ? -1 : 1;
  return (
    <g transform={`translate(${x},${y}) scale(${k01(k)})`} opacity={k01(k)}>
      <circle cx={tx * w * 0.35} cy={h * 0.62 + 10} r={9} fill={C.white} stroke={O} strokeWidth={3.5} />
      <circle cx={tx * w * 0.48} cy={h * 0.62 + 36} r={5.5} fill={C.white} stroke={O} strokeWidth={3.5} />
      <g transform={`translate(0,${Math.sin(f / 10) * 2})`}>
        <ellipse cx={0} cy={0} rx={w / 2} ry={h / 2} fill={C.white} stroke={O} strokeWidth={4} />
        {[-0.6, -0.2, 0.2, 0.6].map((p, i) => <circle key={i} cx={p * w / 2} cy={-h / 2 + 8 + Math.abs(p) * 8} r={h * 0.22} fill={C.white} stroke={O} strokeWidth={4} />)}
        <ellipse cx={0} cy={0} rx={w / 2 - 3} ry={h / 2 - 3} fill={C.white} />
        {[-0.6, -0.2, 0.2, 0.6].map((p, i) => <circle key={i} cx={p * w / 2} cy={-h / 2 + 8 + Math.abs(p) * 8} r={h * 0.22 - 3} fill={C.white} />)}
        {children}
      </g>
    </g>
  );
};

// ---------- symbols ----------
export const QMark: React.FC<{ x: number; y: number; k?: number; size?: number; color?: string; bounce?: boolean }> = ({ x, y, k = 1, size = 120, color = C.yellow, bounce = true }) => {
  const f = useCurrentFrame();
  const b = bounce ? Math.abs(Math.sin(f / 7)) * -10 : 0;
  return (
    <g transform={`translate(${x},${y + b}) scale(${k01(k)}) rotate(${Math.sin(f / 12) * 6})`} opacity={k01(k)}>
      <text x={5} y={size * 0.36 + 5} textAnchor="middle" fontFamily="Baloo" fontWeight={800} fontSize={size} fill={O}>?</text>
      <text x={0} y={size * 0.36} textAnchor="middle" fontFamily="Baloo" fontWeight={800} fontSize={size} fill={color} stroke={O} strokeWidth={3}>?</text>
    </g>
  );
};

export const Exclaim: React.FC<{ x: number; y: number; k?: number; size?: number; color?: string }> = ({ x, y, k = 1, size = 120, color = C.red }) => (
  <g transform={`translate(${x},${y}) scale(${k01(k)})`} opacity={k01(k)}>
    <text x={5} y={size * 0.36 + 5} textAnchor="middle" fontFamily="Baloo" fontWeight={800} fontSize={size} fill={O}>!</text>
    <text x={0} y={size * 0.36} textAnchor="middle" fontFamily="Baloo" fontWeight={800} fontSize={size} fill={color} stroke={O} strokeWidth={3}>!</text>
  </g>
);

export const Bulb: React.FC<{ x: number; y: number; on?: boolean; k?: number; s?: number }> = ({ x, y, on = true, k = 1, s = 1 }) => {
  const f = useCurrentFrame();
  return (
    <g transform={`translate(${x},${y}) scale(${s * k01(k)})`} opacity={k01(k)}>
      {on && [0, 45, 90, 135, 180, 225, 270, 315].map((a, i) => (
        <line key={i} x1={Math.cos(a * Math.PI / 180) * 52} y1={Math.sin(a * Math.PI / 180) * 52} x2={Math.cos(a * Math.PI / 180) * (66 + Math.sin(f / 4 + i) * 5)} y2={Math.sin(a * Math.PI / 180) * (66 + Math.sin(f / 4 + i) * 5)} stroke={C.yellow} strokeWidth={6} strokeLinecap="round" />
      ))}
      <circle cx={0} cy={0} r={38} fill={on ? C.yellow : C.grey} stroke={O} strokeWidth={4} />
      <path d="M-14 32 L-16 50 L16 50 L14 32 Z" fill={C.grey} stroke={O} strokeWidth={4} strokeLinejoin="round" />
      <path d="M-8 30 L-4 8 L4 8 L8 30" stroke={O} strokeWidth={3} fill="none" />
    </g>
  );
};

export const Check: React.FC<{ x: number; y: number; k?: number; s?: number }> = ({ x, y, k = 1, s = 1 }) => (
  <g transform={`translate(${x},${y}) scale(${s * (0.5 + 0.5 * k01(k))})`} opacity={k01(k)}>
    <circle r={40} fill={C.green} stroke={O} strokeWidth={4} />
    <path d="M-20 2 L-6 16 L22 -16" stroke={C.white} strokeWidth={10} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M-20 2 L-6 16 L22 -16" stroke={O} strokeWidth={3} fill="none" strokeLinecap="round" strokeLinejoin="round" opacity={0.25} />
  </g>
);

export const Cross: React.FC<{ x: number; y: number; k?: number; s?: number }> = ({ x, y, k = 1, s = 1 }) => (
  <g transform={`translate(${x},${y}) scale(${s * (0.5 + 0.5 * k01(k))})`} opacity={k01(k)}>
    <circle r={40} fill={C.red} stroke={O} strokeWidth={4} />
    <path d="M-16 -16 L16 16 M16 -16 L-16 16" stroke={C.white} strokeWidth={10} strokeLinecap="round" />
  </g>
);

export const Heart: React.FC<{ x: number; y: number; k?: number; s?: number; color?: string }> = ({ x, y, k = 1, s = 1, color = C.red }) => {
  const f = useCurrentFrame();
  const beat = 1 + Math.max(0, Math.sin(f / 5)) * 0.08;
  return (
    <g transform={`translate(${x},${y}) scale(${s * k01(k) * beat})`} opacity={k01(k)}>
      <path d="M0 28 C-40 0 -40 -30 -20 -34 C-8 -36 0 -26 0 -20 C0 -26 8 -36 20 -34 C40 -30 40 0 0 28 Z" fill={color} stroke={O} strokeWidth={4} strokeLinejoin="round" />
    </g>
  );
};

export const Star: React.FC<{ x: number; y: number; s?: number; color?: string; twinkle?: boolean; seed?: number }> = ({ x, y, s = 1, color = C.yellow, twinkle = true, seed = 0 }) => {
  const f = useCurrentFrame();
  const t = twinkle ? 0.7 + 0.3 * Math.sin(f / 6 + seed) : 1;
  return <path transform={`translate(${x},${y}) scale(${s * t}) rotate(${twinkle ? Math.sin(f / 15 + seed) * 8 : 0})`} d="M0 -22 L6 -7 L22 -7 L9 3 L14 19 L0 9 L-14 19 L-9 3 L-22 -7 L-6 -7 Z" fill={color} stroke={O} strokeWidth={3.5} strokeLinejoin="round" />;
};

/** Arrow that draws itself as k goes 0..1. */
export const Arrow: React.FC<{ from: [number, number]; to: [number, number]; k?: number; color?: string; width?: number; curve?: number }> = ({ from, to, k = 1, color = C.ink, width = 7, curve = 0 }) => {
  const mx = (from[0] + to[0]) / 2, my = (from[1] + to[1]) / 2;
  const dx = to[0] - from[0], dy = to[1] - from[1], n = Math.hypot(dx, dy) || 1;
  const cx = mx - (dy / n) * curve, cy = my + (dx / n) * curve;
  const d = `M${from[0]} ${from[1]} Q${cx} ${cy} ${to[0]} ${to[1]}`;
  const len = n * 1.2 + Math.abs(curve);
  const ang = (Math.atan2(to[1] - cy, to[0] - cx) * 180) / Math.PI;
  return (
    <g>
      <path d={d} stroke={color} strokeWidth={width} fill="none" strokeLinecap="round" strokeDasharray={len} strokeDashoffset={len * (1 - k01(k))} />
      {k01(k) > 0.95 && <path transform={`translate(${to[0]},${to[1]}) rotate(${ang})`} d="M0 0 L-22 -13 L-16 0 L-22 13 Z" fill={color} stroke={color} strokeWidth={3} strokeLinejoin="round" />}
    </g>
  );
};

/** Any path, drawn on as k goes 0..1 (set `len` to about the path length). */
export const Draw: React.FC<{ d: string; k?: number; len?: number; color?: string; width?: number; fill?: string }> = ({ d, k = 1, len = 1200, color = C.ink, width = 5, fill = 'none' }) => (
  <path d={d} stroke={color} strokeWidth={width} fill={k01(k) > 0.98 ? fill : 'none'} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={len} strokeDashoffset={len * (1 - k01(k))} />
);

// ---------- things ----------
export const Sun: React.FC<{ x: number; y: number; s?: number; k?: number }> = ({ x, y, s = 1, k = 1 }) => {
  const f = useCurrentFrame();
  return (
    <g transform={`translate(${x},${y}) scale(${s * k01(k)}) rotate(${f * 0.4})`} opacity={k01(k)}>
      {Array.from({ length: 12 }).map((_, i) => <line key={i} x1={0} y1={-50} x2={0} y2={-66} transform={`rotate(${i * 30})`} stroke={C.orange} strokeWidth={7} strokeLinecap="round" />)}
      <circle r={42} fill={C.yellow} stroke={O} strokeWidth={4} />
    </g>
  );
};

export const Planet: React.FC<{ x: number; y: number; r?: number; color?: string; ring?: boolean; k?: number; spin?: number; stripes?: boolean; face?: boolean }> = ({ x, y, r = 60, color = C.orange, ring, k = 1, spin = 0, stripes, face }) => {
  const f = useCurrentFrame();
  const rot = f * spin;
  return (
    <g transform={`translate(${x},${y}) scale(${k01(k)})`} opacity={k01(k)}>
      {ring && <ellipse rx={r * 1.7} ry={r * 0.45} fill="none" stroke={O} strokeWidth={10} transform="rotate(-15)" />}
      {ring && <ellipse rx={r * 1.7} ry={r * 0.45} fill="none" stroke={C.yellow} strokeWidth={5} transform="rotate(-15)" />}
      <circle r={r} fill={color} stroke={O} strokeWidth={4} />
      {stripes && [-0.5, -0.1, 0.35].map((p, i) => <ellipse key={i} cx={Math.sin(rot / 40 + i) * r * 0.25} cy={p * r} rx={r * Math.sqrt(1 - p * p) * 0.92} ry={r * 0.11} fill="#00000022" />)}
      {spin !== 0 && <circle cx={Math.cos(rot / 30) * r * 0.5} cy={-r * 0.25} r={r * 0.12} fill="#ffffff66" />}
      {face && <g><circle cx={-r * 0.25} cy={-r * 0.1} r={4} fill={O} /><circle cx={r * 0.25} cy={-r * 0.1} r={4} fill={O} /><path d={`M${-r * 0.2} ${r * 0.2} Q0 ${r * 0.4} ${r * 0.2} ${r * 0.2}`} stroke={O} strokeWidth={4} fill="none" strokeLinecap="round" /></g>}
    </g>
  );
};

export const Earth: React.FC<{ x: number; y: number; r?: number; k?: number; spin?: number }> = ({ x, y, r = 60, k = 1, spin = 0.6 }) => {
  const f = useCurrentFrame();
  const o = (f * spin) % 360;
  return (
    <g transform={`translate(${x},${y}) scale(${k01(k)})`} opacity={k01(k)}>
      <circle r={r} fill={C.blue} stroke={O} strokeWidth={4} />
      <g transform={`rotate(${o})`}>
        <ellipse cx={-r * 0.3} cy={-r * 0.3} rx={r * 0.3} ry={r * 0.22} fill={C.green} />
        <ellipse cx={r * 0.35} cy={r * 0.25} rx={r * 0.25} ry={r * 0.3} fill={C.green} />
        <ellipse cx={0} cy={r * 0.6} rx={r * 0.35} ry={r * 0.12} fill={C.green} />
      </g>
      <circle r={r} fill="none" stroke={O} strokeWidth={4} />
    </g>
  );
};

export const Moon: React.FC<{ x: number; y: number; r?: number; k?: number }> = ({ x, y, r = 30, k = 1 }) => (
  <g transform={`translate(${x},${y}) scale(${k01(k)})`} opacity={k01(k)}>
    <path d={`M0 ${-r} A${r} ${r} 0 1 0 0 ${r} A${r * 0.75} ${r * 0.75} 0 1 1 0 ${-r} Z`} fill={C.cream} stroke={O} strokeWidth={4} strokeLinejoin="round" />
  </g>
);

export const Clock: React.FC<{ x: number; y: number; r?: number; k?: number; speed?: number; color?: string }> = ({ x, y, r = 60, k = 1, speed = 6, color = C.white }) => {
  const f = useCurrentFrame();
  return (
    <g transform={`translate(${x},${y}) scale(${k01(k)})`} opacity={k01(k)}>
      <circle r={r} fill={color} stroke={O} strokeWidth={5} />
      {Array.from({ length: 12 }).map((_, i) => <line key={i} x1={0} y1={-r + 8} x2={0} y2={-r + (i % 3 ? 14 : 20)} transform={`rotate(${i * 30})`} stroke={O} strokeWidth={3} strokeLinecap="round" />)}
      <line x1={0} y1={0} x2={0} y2={-r * 0.5} transform={`rotate(${f * speed / 12})`} stroke={O} strokeWidth={6} strokeLinecap="round" />
      <line x1={0} y1={0} x2={0} y2={-r * 0.75} transform={`rotate(${f * speed})`} stroke={C.red} strokeWidth={4} strokeLinecap="round" />
      <circle r={5} fill={O} />
    </g>
  );
};

export const Bars: React.FC<{ x: number; y: number; values: number[]; labels?: string[]; k?: number; w?: number; h?: number; colors?: string[]; gap?: number }> = ({ x, y, values, labels, k = 1, w = 56, h = 200, colors, gap = 24 }) => {
  const max = Math.max(...values) || 1;
  const total = values.length * w + (values.length - 1) * gap;
  return (
    <g transform={`translate(${x - total / 2},${y})`}>
      <line x1={-10} y1={0} x2={total + 10} y2={0} stroke={O} strokeWidth={4} strokeLinecap="round" />
      {values.map((v, i) => {
        const bh = (v / max) * h * k01(k);
        return (
          <g key={i}>
            <rect x={i * (w + gap)} y={-bh} width={w} height={bh} rx={8} fill={(colors ?? [C.blue, C.orange, C.green, C.pink, C.purple])[i % 5]} stroke={O} strokeWidth={4} />
            {labels && <text x={i * (w + gap) + w / 2} y={30} textAnchor="middle" fontFamily="Hand" fontSize={24} fill={C.ink}>{labels[i]}</text>}
            <text x={i * (w + gap) + w / 2} y={-bh - 10} textAnchor="middle" fontFamily="Baloo" fontWeight={700} fontSize={22} fill={C.ink} opacity={k01(k)}>{Math.round(v * k01(k))}</text>
          </g>
        );
      })}
    </g>
  );
};

export const Sign: React.FC<{ text: string; w?: number; color?: string; size?: number }> = ({ text, w = 120, color = C.yellow, size = 26 }) => (
  <g>
    <rect x={-4} y={-6} width={8} height={70} fill={C.brown} stroke={O} strokeWidth={3} />
    <rect x={-w / 2} y={-70} width={w} height={64} rx={10} fill={color} stroke={O} strokeWidth={4} />
    <text x={0} y={-30} textAnchor="middle" fontFamily="Baloo" fontWeight={800} fontSize={size} fill={C.ink}>{text}</text>
  </g>
);

export const Confetti: React.FC<{ k?: number; n?: number; seed?: number; cx?: number; cy?: number }> = ({ k = 1, n = 36, seed = 1, cx = 270, cy = 420 }) => {
  const f = useCurrentFrame();
  const pieces = Array.from({ length: n }).map((_, i) => {
    const a = (i * 137.5 + seed * 50) % 360, r = 140 + ((i * 7919 + seed * 13) % 170);
    const x = cx + Math.cos(a * Math.PI / 180) * r * k01(k), y = cy + Math.sin(a * Math.PI / 180) * r * k01(k) + k01(k) * k01(k) * 160 + Math.sin(f / 5 + i) * 3;
    return { x, y, c: [C.yellow, C.red, C.blue, C.green, C.pink, C.purple][i % 6], rot: f * 4 + i * 40 };
  });
  return <g opacity={Math.min(1, 3 - 3 * k01(k))}>{pieces.map((p, i) => <rect key={i} x={p.x} y={p.y} width={12} height={7} rx={2} fill={p.c} stroke={O} strokeWidth={1.5} transform={`rotate(${p.rot} ${p.x} ${p.y})`} />)}</g>;
};

/** Social CTA icons: thumbs-up and bell/plus, bouncing. */
export const LikeIcon: React.FC<{ x: number; y: number; k?: number; s?: number }> = ({ x, y, k = 1, s = 1 }) => {
  const f = useCurrentFrame();
  return (
    <g transform={`translate(${x},${y + Math.sin(f / 6) * 4}) scale(${s * (0.5 + 0.5 * k01(k))})`} opacity={k01(k)}>
      <circle r={46} fill={C.blue} stroke={O} strokeWidth={4} />
      <path d="M-22 4 H-10 V26 H-22 Z M-10 4 L2 -20 Q6 -28 10 -20 L8 2 H22 Q28 2 26 10 L20 24 Q18 28 12 28 H-10" fill={C.white} stroke={O} strokeWidth={3.5} strokeLinejoin="round" />
    </g>
  );
};
export const FollowIcon: React.FC<{ x: number; y: number; k?: number; s?: number }> = ({ x, y, k = 1, s = 1 }) => {
  const f = useCurrentFrame();
  return (
    <g transform={`translate(${x},${y + Math.sin(f / 6 + 1.5) * 4}) scale(${s * (0.5 + 0.5 * k01(k))})`} opacity={k01(k)}>
      <circle r={46} fill={C.pink} stroke={O} strokeWidth={4} />
      <circle cx={-6} cy={-10} r={11} fill={C.white} stroke={O} strokeWidth={3.5} />
      <path d="M-26 22 Q-6 -2 14 22 Z" fill={C.white} stroke={O} strokeWidth={3.5} strokeLinejoin="round" />
      <path d="M18 -16 V0 M10 -8 H26" stroke={O} strokeWidth={5} strokeLinecap="round" />
    </g>
  );
};
export const CommentIcon: React.FC<{ x: number; y: number; k?: number; s?: number }> = ({ x, y, k = 1, s = 1 }) => {
  const f = useCurrentFrame();
  return (
    <g transform={`translate(${x},${y + Math.sin(f / 6 + 3) * 4}) scale(${s * (0.5 + 0.5 * k01(k))})`} opacity={k01(k)}>
      <circle r={46} fill={C.green} stroke={O} strokeWidth={4} />
      <path d="M-24 -14 H24 Q30 -14 30 -8 V10 Q30 16 24 16 H-4 L-16 28 V16 H-24 Q-30 16 -30 10 V-8 Q-30 -14 -24 -14 Z" fill={C.white} stroke={O} strokeWidth={3.5} strokeLinejoin="round" />
      <circle cx={-12} cy={1} r={3} fill={O} /><circle cx={0} cy={1} r={3} fill={O} /><circle cx={12} cy={1} r={3} fill={O} />
    </g>
  );
};

// ---------- quiz ----------
/** Countdown ring from s0 to s1 (absolute seconds); `t` = absolute second. Shows the remaining whole seconds. */
export const Countdown: React.FC<{ x: number; y: number; s0: number; s1: number; t: number; r?: number; color?: string }> = ({ x, y, s0, s1, t, r = 70, color = C.orange }) => {
  const k = k01((t - s0) / Math.max(0.01, s1 - s0));
  const left = Math.max(0, Math.ceil(s1 - t));
  const circ = 2 * Math.PI * (r - 8);
  const inK = k01((t - s0 + 0.3) / 0.3);
  return (
    <g transform={`translate(${x},${y}) scale(${inK})`} opacity={inK}>
      <circle r={r} fill={C.white} stroke={O} strokeWidth={5} />
      <circle r={r - 8} fill="none" stroke={color} strokeWidth={12} strokeDasharray={circ} strokeDashoffset={circ * k} transform="rotate(-90)" strokeLinecap="round" />
      <text x={0} y={r * 0.33} textAnchor="middle" fontFamily="Baloo" fontWeight={800} fontSize={r * 0.95} fill={C.ink}>{left}</text>
    </g>
  );
};

/** Answer options (2-4). `k` pops them in one after another; `reveal` (index) highlights the right one when `rk` > 0. */
export const Choices: React.FC<{ x: number; y: number; items: string[]; f: number; at?: number; reveal?: number; rk?: number; w?: number; colors?: string[] }> = ({ x, y, items, f, at = 0, reveal = -1, rk = 0, w = 300, colors }) => {
  const letters = 'ABCD';
  return (
    <g>
      {items.map((it, i) => {
        const k = pop(f, at + i * 5, BOUNCY);
        const win = reveal === i && rk > 0, lose = reveal >= 0 && reveal !== i && rk > 0;
        const yy = y + i * 74;
        const col = (colors ?? [C.yellow, C.sky, C.pink, C.lime])[i % 4];
        return (
          <g key={i} transform={`translate(${x},${yy}) scale(${0.7 + 0.3 * k01(k)}) ${win ? `scale(${1 + 0.08 * k01(rk)})` : ''}`} opacity={k01(k) * (lose ? 1 - 0.55 * k01(rk) : 1)}>
            <rect x={-w / 2 + 6} y={-26 + 6} width={w} height={56} rx={28} fill={O} />
            <rect x={-w / 2} y={-26} width={w} height={56} rx={28} fill={win ? C.green : col} stroke={O} strokeWidth={4} />
            <circle cx={-w / 2 + 30} cy={2} r={20} fill={C.white} stroke={O} strokeWidth={3.5} />
            <text x={-w / 2 + 30} y={10} textAnchor="middle" fontFamily="Baloo" fontWeight={800} fontSize={24} fill={C.ink}>{letters[i]}</text>
            <text x={16} y={11} textAnchor="middle" fontFamily="Baloo" fontWeight={700} fontSize={27} fill={C.ink}>{it}</text>
            {win && <g transform={`translate(${w / 2 - 6},2) scale(${k01(rk) * 0.55})`}><circle r={40} fill={C.green} stroke={O} strokeWidth={5} /><path d="M-20 2 L-6 16 L22 -16" stroke={C.white} strokeWidth={11} fill="none" strokeLinecap="round" strokeLinejoin="round" /></g>}
          </g>
        );
      })}
    </g>
  );
};

/** "ANSWER" style stamp that slams in. */
export const Stamp: React.FC<{ x: number; y: number; text: string; k?: number; color?: string; rot?: number }> = ({ x, y, text, k = 1, color = C.red, rot = -8 }) => {
  const kk = k01(k);
  const w = text.length * 30 + 50;
  return (
    <g transform={`translate(${x},${y}) rotate(${rot}) scale(${2 - kk})`} opacity={kk}>
      <rect x={-w / 2} y={-34} width={w} height={68} rx={12} fill="none" stroke={color} strokeWidth={7} />
      <text x={0} y={16} textAnchor="middle" fontFamily="Baloo" fontWeight={800} fontSize={46} fill={color}>{text}</text>
    </g>
  );
};
