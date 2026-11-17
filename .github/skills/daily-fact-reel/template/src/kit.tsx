import React from 'react';
import { interpolate, spring, useCurrentFrame } from 'remotion';
import { C, FPS, SPRING, T, bn, clamp } from './theme';
import { Stage } from './chrome';
import { Person, Mini, Bubble, PersonP } from './figures';
import { RMS, SPEAK } from './data';

/** mouth opens only while `who` is inside a speaking window AND the voice is loud at this frame */
export const mouthOpen = (who: string, t: number) => {
  const w = SPEAK[who] || [];
  if (!w.some(([a, b]) => t >= a && t <= b)) return false;
  return (RMS[Math.floor(t * 30)] ?? 0) > 0.2;
};

export type SP = { t0: number; dur: number };
export const O = C.outline;

export const TANVIR = { skin: '#9A6238', ear: '#8A5530', shirt: '#6E96BB', pants: '#2A3550', hair: '#15110e' };
export const SHUVO = { skin: '#A86D40', ear: '#97603A', shirt: '#D9A93A', pants: '#3a4660', hair: '#1b140f' };
export const CHACHA: Partial<PersonP> = { skin: '#8E5B34', ear: '#7d4d2b', shirt: '#EFE3C8', pants: '#444', hair: '#8d8d8d', lungi: '#8f98a0', glasses: true, mustache: '#8d8d8d', long: true };
export const FATHER = { skin: '#946037', ear: '#84552f', shirt: '#9DBBD6', pants: '#2b2f3f', hair: '#9a9a9a', glasses: true };

export const useT = (t0: number) => {
  const f = useCurrentFrame();
  return { f, t: t0 + f / FPS, lf: (s: number) => f - T(s - t0) };
};
export const sp = (frame: number, cfg = SPRING) => spring({ frame, fps: FPS, config: cfg });
export const breathe = (f: number, a = 1.5, p = 22) => Math.sin(f / p) * a;
export const blinkAt = (f: number) => f % 105 < 4;

// ---------- backgrounds ----------
export const RoomNight: React.FC<{ f: number }> = ({ f }) => (
  <>
    <defs>
      <radialGradient id="glow"><stop offset="0" stopColor="#ffd98a" stopOpacity="0.55" /><stop offset="1" stopColor="#ffd98a" stopOpacity="0" /></radialGradient>
    </defs>
    <rect width={540} height={960} fill="#3b4466" />
    <rect y={606} width={540} height={354} fill="#2b3150" />
    <rect y={602} width={540} height={6} fill="#222741" />
    <rect x={40} y={130} width={150} height={120} fill="#141a33" />
    {[[70, 160], [110, 195], [150, 150], [165, 220], [85, 230]].map(([x, y], i) => (
      <circle key={i} cx={x} cy={y} r={2.2} fill="#fff" opacity={0.5 + 0.5 * Math.sin(f / 12 + i)} />
    ))}
    <path d="M140 165 a18 18 0 1 0 14 28 a14 14 0 1 1 -14 -28Z" fill="#f3e7c0" />
    <rect x={40} y={130} width={150} height={120} fill="none" stroke="#8d7a5c" strokeWidth={6} />
    <rect x={112} y={130} width={6} height={120} fill="#8d7a5c" />
    <circle cx={436} cy={430} r={230} fill="url(#glow)" opacity={0.85 + 0.1 * Math.sin(f / 15)} />
  </>
);
export const DeskNight: React.FC = () => (
  <>
    <rect x={215} y={500} width={330} height={14} rx={5} fill="#6B4A32" stroke={O} strokeWidth={3} />
    <rect x={222} y={514} width={14} height={140} fill="#5a3d28" />
    <rect x={510} y={514} width={14} height={140} fill="#5a3d28" />
  </>
);
export const DeskTop: React.FC<{ lamp?: boolean }> = ({ lamp = true }) => (
  <>
    {([['#C8451E', 330], ['#2C483B', 318], ['#D9A93A', 306]] as [string, number][]).map(([c, y], i) => (
      <rect key={i} x={300 + i * 4} y={Number(y) + 130} width={90} height={14} rx={3} fill={c} stroke={O} strokeWidth={2.5} />
    ))}
    {lamp && (
      <g transform="translate(-34,0)">
        <rect x={470} y={488} width={46} height={12} rx={5} fill="#3b2a20" />
        <path d="M493 488 L480 420 L520 392" stroke="#3b2a20" strokeWidth={7} fill="none" strokeLinecap="round" />
        <path d="M505 384 L545 392 L530 418 Z" fill="#E8B84A" stroke={O} strokeWidth={3} />
      </g>
    )}
  </>
);
export const RoomDay: React.FC = () => (
  <>
    <rect width={540} height={960} fill="#E2D6BE" />
    <rect y={606} width={540} height={354} fill="#D3C7B1" />
    <rect y={602} width={540} height={6} fill="#c2b499" />
  </>
);
export const RoomLiving: React.FC = () => (
  <>
    <rect width={540} height={960} fill="#D9CBB1" />
    <rect y={606} width={540} height={354} fill="#C9BB9F" />
    <rect y={602} width={540} height={6} fill="#b6a789" />
    <rect x={190} y={140} width={160} height={110} rx={6} fill="#efe6d3" stroke="#6B4A32" strokeWidth={8} />
    <path d="M205 230 L255 185 L290 215 L320 190 L340 230Z" fill="#9db4a0" />
    <circle cx={300} cy={170} r={12} fill="#e3b04b" />
    <rect x={60} y={640} width={420} height={36} rx={18} fill="#b5543a" opacity={0.35} />
  </>
);

// ---------- scenes ----------

// ---------- reusable scene pieces ----------
export const Relatives: React.FC<{ t0: number; dur: number; colors: string[]; bubble: string; w?: number; laugh?: boolean }> = ({ t0, dur, colors, bubble, w = 70, laugh }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur}>
      <RoomLiving />
      {colors.map((c, i) => (
        <Mini key={i} x={90 + i * 95} y={560} s={1.9} color={c} skin={['#9A6238', '#A86D40', '#8A5530'][i]} bob={laugh ? Math.abs(Math.sin(f / 5 + i * 1.7)) * -9 : 0} />
      ))}
      {colors.map((_, i) => (
        <Bubble key={i} x={95 + i * 95} y={300 + (i % 2) * 30} text={bubble} w={w} delay={6 + i * 5} />
      ))}
      <Mini x={440} y={560} s={1.9} color="#6E96BB" flip bob={breathe(f, 1.5)} />
    </Stage>
  );
};
export const Eye: React.FC<{ x: number; y: number; d: number; look: [number, number]; f: number }> = ({ x, y, d, look, f }) => {
  const k = sp(f - d, { damping: 12, stiffness: 120, mass: 0.7 });
  const dx = look[0] - x, dy = look[1] - y, n = Math.hypot(dx, dy) || 1;
  return (
    <g transform={`translate(${x},${y}) scale(${k},${k})`} opacity={Math.min(1, k)}>
      <ellipse rx={24} ry={15} fill="#F6EFE8" stroke={O} strokeWidth={3} />
      <circle cx={(dx / n) * 8} cy={(dy / n) * 5} r={7} fill={O} />
    </g>
  );
};
export const Doc: React.FC<{ x: number; y: number; k?: number }> = ({ x, y, k = 1 }) => (
  <g transform={`translate(${x},${y}) scale(${k})`}>
    <rect width={280} height={360} rx={14} fill="#F6EFE8" stroke={O} strokeWidth={3} />
    <rect width={280} height={60} rx={14} fill={C.teal} />
    <rect y={30} width={280} height={30} fill={C.teal} />
    <text x={140} y={42} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={26} fill="#fff">ফলাফল</text>
    {[0, 1, 2, 3].map((i) => <rect key={i} x={30} y={96 + i * 36} width={i % 2 ? 150 : 220} height={12} rx={6} fill="#cdbfa8" />)}
  </g>
);
export const Megaphone: React.FC<{ k: number; xk: number }> = ({ k, xk }) => (
  <g transform={`translate(270,430) scale(${k})`}>
    <path d="M-120 -40 L40 -120 L40 120 L-120 40Z" fill="#8c6a4f" stroke={O} strokeWidth={5} strokeLinejoin="round" />
    <rect x={-170} y={-46} width={64} height={92} rx={16} fill="#6B4A32" stroke={O} strokeWidth={5} />
    <rect x={-100} y={40} width={34} height={80} rx={12} fill="#6B4A32" stroke={O} strokeWidth={5} />
    {[0, 1, 2].map((i) => <path key={i} d={`M${70 + i * 34} ${-40 - i * 10} Q${100 + i * 34} 0 ${70 + i * 34} ${40 + i * 10}`} stroke={C.ink} strokeWidth={6} fill="none" strokeLinecap="round" />)}
    <g transform={`translate(80,70) scale(${xk})`} opacity={Math.min(1, xk)}>
      <circle r={62} fill={C.red} stroke={O} strokeWidth={5} />
      <path d="M-28 -28 L28 28 M28 -28 L-28 28" stroke="#fff" strokeWidth={14} strokeLinecap="round" />
    </g>
  </g>
);
export const StepCard: React.FC<{ y: number; n: string; text: string; k: number }> = ({ y, n, text, k }) => (
  <g transform={`translate(270,${y + (1 - Math.min(1, k)) * 40}) scale(${0.9 + 0.1 * Math.min(1, k)})`} opacity={Math.min(1, k)}>
    <rect x={-190} y={-70} width={380} height={140} rx={24} fill="#F6EFE8" stroke={O} strokeWidth={3} />
    <circle cx={-120} cy={0} r={34} fill={C.red} />
    <text x={-120} y={14} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={40} fill="#fff">{n}</text>
    <text x={-50} y={16} fontFamily="NSB" fontWeight={800} fontSize={50} fill={C.ink}>{text}</text>
  </g>
);
