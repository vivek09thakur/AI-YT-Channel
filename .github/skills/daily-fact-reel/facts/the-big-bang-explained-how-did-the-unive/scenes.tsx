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
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={400} r={120} fill="#ffd98a" opacity={0.2 + 0.1 * Math.sin(f / 10)} />
      {[ [100, 200], [400, 150], [200, 700], [450, 650] ].map(([x, y], i) => (
        <circle key={i} cx={x} cy={y} r={3} fill="#fff" opacity={0.4 + 0.6 * Math.sin(f / 8 + i)} />
      ))}
    </Stage>
  );
};

export const S1: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      {[ [120, 250], [380, 280], [270, 400], [150, 550], [390, 520] ].map(([x, y], i) => (
        <g key={i} transform={`translate(${x},${y})`}>
          <circle r={25 + i * 4} fill="#ffd98a" opacity={0.3} />
          <path d="M0 -20 L5 -5 L20 0 L5 5 L0 20 L-5 5 L-20 0 L-5 -5 Z" fill="#fff" />
        </g>
      ))}
    </Stage>
  );
};

export const S2: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const sc = sp(lf(10.53));
  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />
      <g transform={`translate(270,480) scale(${sc})`}>
        <circle r={180} fill={C.red} opacity={0.8} />
        <text y={10} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={44} fill="#fff">13.8B</text>
      </g>
    </Stage>
  );
};

export const S3: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <path d="M100 500 Q270 300 440 500" stroke={C.red} strokeWidth={8} fill="none" strokeDasharray="12 12" />
    </Stage>
  );
};

export const S4: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const sc = sp(lf(22.05));
  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />
      <circle cx={270} cy={480} r={100 * sc} fill="#ffd98a" opacity={0.9} />
    </Stage>
  );
};

export const S5: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />
      {Array.from({ length: 30 }).map((_, i) => (
        <circle key={i} cx={(i * 37) % 540} cy={(i * 53 + Math.sin(f / 5 + i) * 15) % 960} r={4 + (i % 5)} fill={i % 2 === 0 ? C.red : '#ffd98a'} />
      ))}
    </Stage>
  );
};

export const S6: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={480} r={140} fill="#3b4466" stroke="#ffd98a" strokeWidth={6} />
    </Stage>
  );
};

export const S7: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const sc = sp(lf(38.03));
  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />
      <g transform={`translate(270,480) scale(${sc})`}>
        <circle r={90} fill={C.teal} stroke={O} strokeWidth={4} />
        <text y={15} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={40} fill="#fff">H</text>
      </g>
    </Stage>
  );
};

export const S8: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      {[ [150, 300], [380, 500], [270, 600] ].map(([x, y], i) => (
        <ellipse key={i} cx={x} cy={y} rx={90} ry={40} fill="#ffd98a" opacity={0.25} transform={i === 1 ? 'rotate(30)' : 'rotate(-20)'} />
      ))}
    </Stage>
  );
};

export const S9: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const sc = sp(lf(50.73));
  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />
      <g transform={`translate(270,480) scale(${sc})`}>
        <circle r={110} fill={C.red} stroke={O} strokeWidth={4} />
        <text y={15} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={44} fill="#fff">FUSION</text>
      </g>
    </Stage>
  );
};

export const S10: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const sc = sp(lf(55.10));
  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />
      <g transform={`translate(270,480) scale(${sc})`}>
        <circle r={130} fill="#ffd98a" stroke={O} strokeWidth={4} />
        <path d="M-60 0 L60 0 M0 -60 L0 60" stroke={C.red} strokeWidth={12} strokeLinecap="round" />
      </g>
    </Stage>
  );
};

export const S11: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      {Array.from({ length: 12 }).map((_, i) => (
        <circle key={i} cx={270 + Math.sin(i + f / 10) * 180} cy={480 + Math.cos(i + f / 10) * 180} r={16} fill={C.red} stroke={O} strokeWidth={3} />
      ))}
    </Stage>
  );
};

export const S12: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const sc = sp(lf(68.47));
  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />
      <g transform={`translate(270,480) scale(${sc})`}>
        <circle r={90} fill={C.teal} stroke={O} strokeWidth={4} />
        <circle cx={40} cy={-40} r={25} fill="#ffd98a" stroke={O} strokeWidth={3} />
      </g>
    </Stage>
  );
};

export const S13: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <circle cx={270} cy={480} r={150} fill={C.teal} stroke={O} strokeWidth={4} />
      <path d="M150 480 Q270 360 390 480 Z" fill="#ffd98a" />
    </Stage>
  );
};

export const S14: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <path d="M200 550 Q270 450 340 550 Z" fill={C.teal} stroke={O} strokeWidth={4} />
    </Stage>
  );
};

export const S15: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <path d="M170 520 Q270 380 370 520 Z" fill={C.red} stroke={O} strokeWidth={4} />
    </Stage>
  );
};

export const S16: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <circle cx={270} cy={480} r={120} fill={C.teal} stroke={O} strokeWidth={4} />
    </Stage>
  );
};

export const S17: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <Person x={270} y={560 + breathe(f)} s={1.2} {...TANVIR} blink={blinkAt(f)} />
    </Stage>
  );
};

export const S18: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const sc = sp(lf(92.36));
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <g transform={`translate(270,480) scale(${sc})`}>
        <rect x={-110} y={-110} width={220} height={220} rx={30} fill={C.red} stroke={O} strokeWidth={4} />
        <text y={15} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={40} fill="#fff">BODY</text>
      </g>
    </Stage>
  );
};

export const S19: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={480} r={130} fill="#ffd98a" opacity={0.6} />
    </Stage>
  );
};

export const S20: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const sc = sp(lf(102.95));
  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />
      <g transform={`translate(270,480) scale(${sc})`}>
        <text y={15} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={50} fill="#ffd98a">STARDUST</text>
      </g>
    </Stage>
  );
};

export const S21: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
    </Stage>
  );
};

export const S22: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <circle cx={270} cy={480} r={130} fill={C.teal} stroke={O} strokeWidth={4} />
    </Stage>
  );
};

export const S23: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <Person x={270} y={560 + breathe(f)} s={1.2} {...TANVIR} blink={blinkAt(f)} />
    </Stage>
  );
};

export const SCENES = [
  { s: 0.0, e: 4.06, C: S0 },
  { s: 4.06, e: 10.53, C: S1 },
  { s: 10.53, e: 16.98, C: S2 },
  { s: 16.98, e: 22.05, C: S3 },
  { s: 22.05, e: 27.30, C: S4 },
  { s: 27.30, e: 34.25, C: S5 },
  { s: 34.25, e: 38.03, C: S6 },
  { s: 38.03, e: 43.53, C: S7 },
  { s: 43.53, e: 50.73, C: S8 },
  { s: 50.73, e: 55.10, C: S9 },
  { s: 55.10, e: 61.17, C: S10 },
  { s: 61.17, e: 68.47, C: S11 },
  { s: 68.47, e: 73.25, C: S12 },
  { s: 73.25, e: 77.52, C: S13 },
  { s: 77.52, e: 80.84, C: S14 },
  { s: 80.84, e: 85.65, C: S15 },
  { s: 85.65, e: 90.44, C: S16 },
  { s: 90.44, e: 92.36, C: S17 },
  { s: 92.36, e: 96.01, C: S18 },
  { s: 96.01, e: 102.95, C: S19 },
  { s: 102.95, e: 106.64, C: S20 },
  { s: 106.64, e: 112.90, C: S21 },
  { s: 112.90, e: 115.55, C: S22 },
  { s: 115.55, e: 121.63, C: S23 }
];
