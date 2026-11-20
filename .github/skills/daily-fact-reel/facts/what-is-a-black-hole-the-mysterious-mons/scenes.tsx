import React from 'react';
import { interpolate, spring, useCurrentFrame } from 'remotion';
import { C, FPS, SPRING, T, bn, clamp } from './theme';
import { Stage } from './chrome';
import { Person, Mini, Bubble, PersonP } from './figures';
import * as K from './kit';
const { mouthOpen, TANVIR, useT, sp, breathe, blinkAt, RoomNight, Eye, Doc, StepCard } = K;
type SP = K.SP;
const O = K.O;

export const S0: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={400} r={60} fill="#000" stroke={C.red} strokeWidth={4} />
      <path d="M210 400 Q270 300 330 400" stroke="#ffd98a" strokeWidth={3} fill="none" opacity={0.7} />
    </Stage>
  );
};

export const S1: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.navy}>
      <rect width={540} height={960} fill={C.navy} />
      <text x={270} y={400} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={60} fill="#fff">?</text>
    </Stage>
  );
};

export const S2: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={400} r={80} fill="#ffd98a" opacity={0.3} />
    </Stage>
  );
};

export const S3: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  const k = sp(f);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform={`translate(270,400) scale(${k})`}>
        <circle r={90} fill="#000" stroke={C.red} strokeWidth={6} />
        <text y={15} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={32} fill="#fff">BH</text>
      </g>
    </Stage>
  );
};

export const S4: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={400} r={100} fill="#000" stroke="#fff" strokeWidth={3} />
      <path d="M150 300 Q270 500 390 300" stroke={C.red} strokeWidth={4} fill="none" />
    </Stage>
  );
};

export const S5: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <text x={270} y={400} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={50} fill="#ffd98a">Star?</text>
    </Stage>
  );
};

export const S6: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.navy}>
      <rect width={540} height={960} fill={C.navy} />
      <circle cx={270} cy={400} r={120} fill="#ffd98a" />
    </Stage>
  );
};

export const S7: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={400} r={60} fill="#ffd98a" />
    </Stage>
  );
};

export const S8: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={400} r={40} fill="#000" stroke={C.red} strokeWidth={4} />
    </Stage>
  );
};

export const S9: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <text x={270} y={400} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={50} fill={C.ink}>Secret</text>
    </Stage>
  );
};

export const S10: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={400} r={100} fill="#000" stroke={C.teal} strokeWidth={4} />
      <circle cx={270} cy={400} r={130} fill="none" stroke={C.red} strokeWidth={3} strokeDasharray="8 8" />
    </Stage>
  );
};

export const S11: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <path d="M200 400 Q270 400 270 400" stroke="#fff" strokeWidth={4} fill="none" />
      <circle cx={270} cy={400} r={70} fill="#000" />
    </Stage>
  );
};

export const S12: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={400} r={90} fill="#000" />
    </Stage>
  );
};

export const S13: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <text x={270} y={400} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={44} fill={C.ink}>Not a Vacuum!</text>
    </Stage>
  );
};

export const S14: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={400} r={70} fill="#000" />
      <circle cx={400} cy={400} r={10} fill="#ffd98a" />
    </Stage>
  );
};

export const S15: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={400} r={50} fill="#000" />
      <ellipse cx={270} cy={400} rx={150} ry={70} fill="none" stroke="#fff" strokeWidth={2} opacity={0.5} />
      <circle cx={120} cy={400} r={12} fill="#ffd98a" />
    </Stage>
  );
};

export const S16: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={400} r={60} fill="#000" />
      <path d="M100 200 L270 400" stroke={C.red} strokeWidth={3} strokeDasharray="5 5" />
    </Stage>
  );
};

export const S17: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <circle cx={270} cy={400} r={140} fill="#000" stroke={C.red} strokeWidth={6} />
    </Stage>
  );
};

export const S18: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <text x={270} y={400} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={48} fill={C.ink}>Cosmic Mysteries</text>
    </Stage>
  );
};

export const S19: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <text x={270} y={400} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={40} fill="#fff">Time & Space</text>
    </Stage>
  );
};

export const SCENES = [
  { s: 0.00, e: 5.71, C: S0 },
  { s: 5.71, e: 7.55, C: S1 },
  { s: 7.55, e: 9.79, C: S2 },
  { s: 9.79, e: 11.68, C: S3 },
  { s: 11.68, e: 20.89, C: S4 },
  { s: 20.89, e: 22.96, C: S5 },
  { s: 22.96, e: 29.97, C: S6 },
  { s: 29.97, e: 33.11, C: S7 },
  { s: 33.11, e: 40.86, C: S8 },
  { s: 40.86, e: 43.26, C: S9 },
  { s: 43.26, e: 46.89, C: S10 },
  { s: 46.89, e: 52.21, C: S11 },
  { s: 52.21, e: 55.21, C: S12 },
  { s: 55.21, e: 59.05, C: S13 },
  { s: 59.05, e: 62.62, C: S14 },
  { s: 62.62, e: 69.80, C: S15 },
  { s: 69.80, e: 78.76, C: S16 },
  { s: 78.76, e: 86.36, C: S17 },
  { s: 86.36, e: 92.81, C: S18 },
  { s: 92.81, e: 101.90, C: S19 }
];
