import React from 'react';
import { interpolate, spring, useCurrentFrame } from 'remotion';
import { C, FPS, SPRING, T, bn, clamp } from './theme';
import { Stage } from './chrome';
import { Person, Mini, Bubble, PersonP } from './figures';
import * as K from './kit';
const { mouthOpen, TANVIR, SHUVO, CHACHA, FATHER, useT, sp, breathe, blinkAt, RoomNight, DeskNight, DeskTop, RoomDay, RoomLiving, Relatives, Eye, Doc, Megaphone, StepCard } = K;
type SP = K.SP;
const O = K.O;

export const S0: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const sc = sp(lf(0.8));
  return (
    <Stage dur={dur} bg="#1a2536">
      <rect width={540} height={960} fill="#1a2536" />
      <g transform={`translate(270,400) scale(${sc})`}>
        <circle r={140} fill="#3b82f6" opacity={0.3} />
        <path d="M-80 -40 L0 -120 L80 -40 Z" fill="#60a5fa" stroke={O} strokeWidth={4} />
        <rect x={-60} y={-40} width={120} height={140} rx={16} fill="#93c5fd" stroke={O} strokeWidth={4} />
        <circle cx={0} cy={20} r={24} fill={C.red} stroke={O} strokeWidth={3} />
      </g>
    </Stage>
  );
};

export const S1: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(6.01));
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <g transform={`translate(270,450) scale(${k})`}>
        <rect x={-200} y={-100} width={400} height={200} rx={24} fill="#F6EFE8" stroke={O} strokeWidth={4} />
        <text x={0} y={15} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={42} fill={C.ink}>Rayleigh</text>
      </g>
    </Stage>
  );
};

export const S2: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(9.25));
  return (
    <Stage dur={dur} bg="#fffbeb">
      <rect width={540} height={960} fill="#fffbeb" />
      <g transform={`translate(270,450) scale(${k})`}>
        {['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6'].map((col, i) => (
          <rect key={i} x={-180 + i * 75} y={-60} width={60} height={120} rx={12} fill={col} stroke={O} strokeWidth={3} />
        ))}
      </g>
    </Stage>
  );
};

export const S3: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(15.63));
  return (
    <Stage dur={dur} bg="#38bdf8">
      <rect width={540} height={960} fill="#38bdf8" />
      <g transform={`translate(270,450) scale(${k})`}>
        {Array.from({ length: 6 }).map((_, i) => (
          <circle key={i} cx={(i % 3 - 1) * 120} cy={(Math.floor(i / 3) - 0.5) * 140} r={40} fill="#e0f2fe" stroke={O} strokeWidth={4} />
        ))}
      </g>
    </Stage>
  );
};

export const S4: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(21.85));
  return (
    <Stage dur={dur} bg="#1e3a8a">
      <rect width={540} height={960} fill="#1e3a8a" />
      <g transform={`translate(270,450) scale(${k})`}>
        <path d="M-150 -150 L150 -150" stroke="#38bdf8" strokeWidth={12} strokeLinecap="round" />
        <path d="M-150 0 L150 0" stroke="#ef4444" strokeWidth={4} strokeLinecap="round" />
      </g>
    </Stage>
  );
};

export const S5: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(29.91));
  return (
    <Stage dur={dur} bg="#60a5fa">
      <rect width={540} height={960} fill="#60a5fa" />
      <g transform={`translate(270,450) scale(${k})`}>
        <circle r={180} fill="#3b82f6" stroke={O} strokeWidth={5} />
        <text x={0} y={15} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={48} fill="#fff">Blue Sky</text>
      </g>
    </Stage>
  );
};

export const S6: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(35.77));
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <text x={270} y={480} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={60} fill={C.ink}>?</text>
    </Stage>
  );
};

export const S7: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(37.96));
  return (
    <Stage dur={dur} bg="#f97316">
      <rect width={540} height={960} fill="#f97316" />
      <g transform={`translate(270,500) scale(${k})`}>
        <circle cy={0} r={90} fill="#fde047" stroke={O} strokeWidth={4} />
      </g>
    </Stage>
  );
};

export const S8: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(43.05));
  return (
    <Stage dur={dur} bg="#b91c1c">
      <rect width={540} height={960} fill="#b91c1c" />
      <g transform={`translate(270,450) scale(${k})`}>
        <rect x={-160} y={-80} width={320} height={160} rx={20} fill="#fef2f2" stroke={O} strokeWidth={4} />
        <text x={0} y={15} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={36} fill={C.red}>Red & Orange</text>
      </g>
    </Stage>
  );
};

export const S9: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(49.65));
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <g transform={`translate(270,450) scale(${k})`}>
        <circle r={120} fill={C.teal} stroke={O} strokeWidth={4} />
        <text x={0} y={15} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={40} fill="#fff">Science!</text>
      </g>
    </Stage>
  );
};

export const SCENES = [
  { s: 0.0, e: 5.8, C: S0 },
  { s: 5.8, e: 15.4, C: S1 },
  { s: 15.4, e: 21.5, C: S2 },
  { s: 21.5, e: 29.6, C: S3 },
  { s: 29.6, e: 35.6, C: S4 },
  { s: 35.6, e: 37.6, C: S5 },
  { s: 37.6, e: 42.8, C: S6 },
  { s: 42.8, e: 49.3, C: S7 },
  { s: 49.3, e: 59.11, C: S8 }
];
