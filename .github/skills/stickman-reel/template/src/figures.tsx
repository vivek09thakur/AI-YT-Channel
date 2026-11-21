import React from 'react';
import { useCurrentFrame } from 'remotion';
import { C } from './theme';

/*
 Stick: the one character of the kit. Round head, dot eyes, tube limbs, black outline. Poses are procedural and
 animate by themselves (walk/run/jump/wave/dance loop on the current frame), so a scene only has to pick a pose.

 Origin = between the feet, on the ground. Height ~270 units at s=1 (design space is 540x960).
 Angles: 0 = straight down, positive = toward the front (+x). flip mirrors the figure (then it faces -x).
*/
export type Pose = 'stand' | 'walk' | 'run' | 'jump' | 'sit' | 'think' | 'point' | 'shrug' | 'wave' | 'cheer' | 'facepalm' | 'explain' | 'cross' | 'dance' | 'pointup' | 'lean';
export type Face = 'neutral' | 'happy' | 'laugh' | 'surprised' | 'sad' | 'think' | 'wink' | 'angry' | 'sleepy';

export type StickP = {
  x: number; y: number;
  s?: number; flip?: boolean;
  pose?: Pose; face?: Face;
  shirt?: string;              // torso fill; white = classic doodle, a colour tells characters apart
  talk?: boolean;              // open mouth (pair with mouthOpen())
  look?: [number, number];     // pupil offset, each -1..1
  blink?: boolean;             // force closed eyes this frame (auto blink happens anyway)
  seed?: number;               // phase offset so several figures do not move in unison
  tilt?: number;               // extra body lean in degrees (positive = forward)
  hold?: React.ReactNode;      // drawn at the front hand, e.g. a sign or a cup
  still?: boolean;             // no idle bob/sway
  shadow?: boolean;            // ground shadow (default true)
};

const HEAD_R = 36, HEAD_Y = -232, SH_Y = -174, HIP_Y = -92, UA = 56, FA = 54, TH = 48, SH = 46;
const rad = (d: number) => (d * Math.PI) / 180;
const end = (x: number, y: number, a: number, L: number): [number, number] => [x + L * Math.sin(rad(a)), y + L * Math.cos(rad(a))];

type Limbs = { la: [number, number]; ra: [number, number]; ll: [number, number]; rl: [number, number]; bob: number; lean: number; drop: number };

const pose = (p: Pose, f: number, seed: number): Limbs => {
  const ph = f / 4.6 + seed;
  // resting arms hang slightly outward so the back arm is not hidden behind the shirt
  const base: Limbs = { la: [-24, -12], ra: [24, 12], ll: [4, 0], rl: [-4, 0], bob: 0, lean: 0, drop: 0 };
  switch (p) {
    case 'walk': {
      const sw = Math.sin(ph) * 30, sw2 = Math.sin(ph + Math.PI) * 30;
      const k1 = Math.max(0, Math.sin(ph + 1.2)) * 50, k2 = Math.max(0, Math.sin(ph + Math.PI + 1.2)) * 50;
      return { ...base, ll: [sw, sw - k1], rl: [sw2, sw2 - k2], la: [-sw * 0.7, -sw * 0.7 + 25], ra: [-sw2 * 0.7, -sw2 * 0.7 + 25], bob: -Math.abs(Math.sin(ph)) * 4, lean: 3 };
    }
    case 'run': {
      const q = f / 3.1 + seed, sw = Math.sin(q) * 52, sw2 = Math.sin(q + Math.PI) * 52;
      const k1 = Math.max(0, Math.sin(q + 1.3)) * 75, k2 = Math.max(0, Math.sin(q + Math.PI + 1.3)) * 75;
      return { ...base, ll: [sw, sw - k1], rl: [sw2, sw2 - k2], la: [-sw * 0.8, -sw * 0.8 + 95], ra: [-sw2 * 0.8, -sw2 * 0.8 + 95], bob: -Math.abs(Math.sin(q)) * 7, lean: 14 };
    }
    case 'jump': {
      const h = Math.abs(Math.sin(f / 9 + seed));
      return { ...base, la: [-150, -168], ra: [150, 168], ll: [35 * h, 35 * h - 70 * h], rl: [-25 * h, -25 * h - 60 * h], bob: -h * 48 };
    }
    case 'sit': return { ...base, ll: [88, 2], rl: [92, -2], la: [40, 100], ra: [38, 96], drop: 44 };
    case 'think': return { ...base, ra: [150, -62], la: [-24, -12], lean: -4 };
    case 'point': return { ...base, ra: [95, 92], la: [-24, -12] };
    case 'pointup': return { ...base, ra: [165, 172], la: [-24, -12] };
    case 'shrug': return { ...base, la: [-40, -165], ra: [40, 165], bob: -5 };
    case 'wave': return { ...base, ra: [158, 160 + Math.sin(f / 2.6 + seed) * 26], la: [-24, -12] };
    case 'cheer': return { ...base, la: [-150, -165], ra: [150, 165], bob: -Math.abs(Math.sin(f / 6 + seed)) * 6 };
    case 'facepalm': return { ...base, ra: [150, -70], la: [-24, -12], lean: 6 };
    case 'explain': return { ...base, ra: [70, 20 + Math.sin(f / 5.5 + seed) * 16], la: [-24, -12] };
    case 'cross': return { ...base, la: [35, -110], ra: [-35, 110] };
    case 'lean': return { ...base, la: [-25, -40], ra: [-20, -30], lean: -12 };
    case 'dance': {
      const p1 = Math.sin(f / 5 + seed), up = Math.max(0, p1), dn = Math.max(0, -p1);
      return { la: [-20 - 125 * up, -40 - 125 * up], ra: [20 + 125 * dn, 40 + 125 * dn], ll: [-14 * p1, -14 * p1 - 20 * Math.abs(p1)], rl: [14 * p1, 14 * p1 - 20 * Math.abs(p1)], bob: -Math.abs(p1) * 6, lean: p1 * 5, drop: 0 };
    }
    default: return base;
  }
};

const Limb: React.FC<{ x: number; y: number; a: [number, number]; L1: number; L2: number; fill: string; hand?: boolean; foot?: boolean; children?: (p: [number, number]) => React.ReactNode }> = ({ x, y, a, L1, L2, fill, hand, foot, children }) => {
  const [ex, ey] = end(x, y, a[0], L1);
  const [hx, hy] = end(ex, ey, a[1], L2);
  const pts = `${x},${y} ${ex},${ey} ${hx},${hy}`;
  return (
    <g>
      <polyline points={pts} fill="none" stroke={C.outline} strokeWidth={24} strokeLinecap="round" strokeLinejoin="round" />
      <polyline points={pts} fill="none" stroke={fill} strokeWidth={13} strokeLinecap="round" strokeLinejoin="round" />
      {hand && <circle cx={hx} cy={hy} r={12} fill={fill} stroke={C.outline} strokeWidth={5} />}
      {foot && <ellipse cx={hx + 9} cy={hy - 1} rx={20} ry={8} fill={fill} stroke={C.outline} strokeWidth={5} />}
      {children && children([hx, hy])}
    </g>
  );
};

const Eyes: React.FC<{ face: Face; closed: boolean; look: [number, number] }> = ({ face, closed, look }) => {
  const dx = look[0] * 5, dy = look[1] * 4;
  const big = face === 'surprised';
  if (closed || face === 'sleepy') {
    return <g stroke={C.outline} strokeWidth={4} fill="none" strokeLinecap="round"><path d="M-21 -242 L-7 -242" /><path d="M7 -242 L21 -242" /></g>;
  }
  if (face === 'laugh') {
    return <g stroke={C.outline} strokeWidth={4} fill="none" strokeLinecap="round"><path d="M-21 -238 Q-14 -250 -7 -238" /><path d="M7 -238 Q14 -250 21 -238" /></g>;
  }
  return (
    <g>
      {face === 'wink' ? <path d="M-21 -240 Q-14 -234 -7 -240" stroke={C.outline} strokeWidth={4} fill="none" strokeLinecap="round" /> : (
        <>{big && <circle cx={-14} cy={-242} r={9} fill="#fff" stroke={C.outline} strokeWidth={3} />}<circle cx={-14 + dx} cy={-242 + dy} r={big ? 5 : 4.5} fill={C.outline} /></>
      )}
      {big && <circle cx={14} cy={-242} r={9} fill="#fff" stroke={C.outline} strokeWidth={3} />}
      <circle cx={14 + dx} cy={-242 + dy} r={big ? 5 : 4.5} fill={C.outline} />
    </g>
  );
};

const Brows: React.FC<{ face: Face }> = ({ face }) => {
  const s = { stroke: C.outline, strokeWidth: 4, fill: 'none', strokeLinecap: 'round' as const };
  if (face === 'surprised') return <g {...s}><path d="M-22 -262 Q-14 -268 -6 -262" /><path d="M6 -262 Q14 -268 22 -262" /></g>;
  if (face === 'sad') return <g {...s}><path d="M-22 -258 L-6 -263" /><path d="M6 -263 L22 -258" /></g>;
  if (face === 'angry') return <g {...s}><path d="M-22 -264 L-6 -257" /><path d="M6 -257 L22 -264" /></g>;
  if (face === 'think') return <g {...s}><path d="M-22 -257 L-6 -257" /><path d="M6 -263 Q14 -268 22 -263" /></g>;
  return null;
};

const Mouth: React.FC<{ face: Face; talk: boolean }> = ({ face, talk }) => {
  const s = { stroke: C.outline, strokeWidth: 4.5, fill: 'none', strokeLinecap: 'round' as const };
  if (talk) return <ellipse cx={0} cy={-212} rx={face === 'laugh' || face === 'happy' ? 10 : 7} ry={face === 'surprised' ? 10 : 7} fill={C.outline} />;
  switch (face) {
    case 'happy': case 'wink': return <path d="M-13 -218 Q0 -204 13 -218" {...s} />;
    case 'laugh': return <path d="M-15 -217 Q0 -194 15 -217 Z" fill={C.outline} stroke={C.outline} strokeWidth={3} strokeLinejoin="round" />;
    case 'surprised': return <ellipse cx={0} cy={-212} rx={6} ry={9} fill={C.outline} />;
    case 'sad': return <path d="M-11 -210 Q0 -221 11 -210" {...s} />;
    case 'think': return <path d="M-6 -212 L8 -215" {...s} />;
    case 'angry': return <path d="M-11 -212 L11 -212" {...s} />;
    case 'sleepy': return <circle cx={0} cy={-212} r={4} fill={C.outline} />;
    default: return <path d="M-9 -214 L9 -214" {...s} />;
  }
};

export const Stick: React.FC<StickP> = ({ x, y, s = 1, flip, pose: p = 'stand', face = 'neutral', shirt = C.white, talk = false, look = [0, 0], blink, seed = 0, tilt = 0, hold, still, shadow = true }) => {
  const f = useCurrentFrame();
  const L = pose(p, f, seed);
  const idle = still ? 0 : Math.sin(f / 14 + seed) * 1.6;
  const sway = still ? 0 : Math.sin(f / 23 + seed) * 1.2;
  const closed = blink ?? ((f + Math.round(seed * 37)) % 105 < 4);
  const hip = HIP_Y + L.drop, sh = SH_Y + L.drop, head = HEAD_Y + L.drop;
  const lean = L.lean + tilt + sway;
  const fill = C.white;
  return (
    <g transform={`translate(${x},${y}) scale(${flip ? -s : s},${s})`}>
      {shadow && <ellipse cx={0} cy={2} rx={44} ry={7} fill={C.shadow} />}
      <g transform={`translate(0,${L.bob + idle})`}>
        {/* back leg + back arm first so the torso overlaps them */}
        <Limb x={-11} y={hip} a={L.ll} L1={TH} L2={SH} fill={fill} foot />
        <g transform={`rotate(${lean} 0 ${hip})`}>
          <Limb x={-18} y={sh} a={L.la} L1={UA} L2={FA} fill={fill} hand />
          <rect x={-28} y={sh - 16} width={56} height={hip - sh + 32} rx={27} fill={shirt} stroke={C.outline} strokeWidth={5} />
          <rect x={-7} y={head + HEAD_R - 6} width={14} height={16} fill={fill} stroke={C.outline} strokeWidth={5} />
          <g transform={`translate(0,${head - HEAD_Y})`}>
            <circle cx={0} cy={HEAD_Y} r={HEAD_R} fill={fill} stroke={C.outline} strokeWidth={5} />
            <Brows face={face} />
            <Eyes face={face} closed={closed} look={look} />
            <Mouth face={face} talk={talk} />
          </g>
          <Limb x={18} y={sh} a={L.ra} L1={UA} L2={FA} fill={fill} hand>
            {hold ? ([hx, hy]) => <g transform={`translate(${hx},${hy})`}>{hold}</g> : undefined}
          </Limb>
        </g>
        <Limb x={11} y={hip} a={L.rl} L1={TH} L2={SH} fill={fill} foot />
      </g>
    </g>
  );
};

/** Walks from `from` to `to` between absolute seconds s0..s1, stands (pose `rest`) before and after. `t` = absolute second. */
export const Walker: React.FC<Omit<StickP, 'x' | 'y' | 'pose'> & { from: [number, number]; to: [number, number]; s0: number; s1: number; t: number; rest?: Pose; restAfter?: Pose }> = ({ from, to, s0, s1, t, rest = 'stand', restAfter, ...rest_ }) => {
  const k = Math.max(0, Math.min(1, (t - s0) / Math.max(0.01, s1 - s0)));
  const moving = t > s0 && t < s1;
  const x = from[0] + (to[0] - from[0]) * k, y = from[1] + (to[1] - from[1]) * k;
  const flip = rest_.flip ?? to[0] < from[0];
  return <Stick {...rest_} x={x} y={y} flip={flip} pose={moving ? 'walk' : t >= s1 ? restAfter ?? rest : rest} />;
};

/** A row of small figures (crowd / audience). */
export const Crowd: React.FC<{ x: number; y: number; n?: number; s?: number; gap?: number; pose?: Pose; face?: Face; shirts?: string[]; talk?: boolean }> = ({ x, y, n = 4, s = 0.55, gap = 70, pose = 'stand', face = 'happy', shirts, talk }) => (
  <g>
    {Array.from({ length: n }).map((_, i) => (
      <Stick key={i} x={x + (i - (n - 1) / 2) * gap} y={y} s={s} pose={pose} face={face} seed={i * 1.7} shirt={shirts ? shirts[i % shirts.length] : C.white} talk={talk} shadow={false} />
    ))}
  </g>
);
