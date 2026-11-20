import React from 'react';
import { interpolate, spring, useCurrentFrame } from 'remotion';
import { C, FPS, SPRING, T, clamp } from './theme';
import { Stage } from './chrome';
import { Person, Mini, Bubble, PersonP } from './figures';
import * as K from './kit';
const { mouthOpen, useT, sp, breathe, blinkAt, RoomNight } = K;
type SP = K.SP;
const O = K.O;

export const S0: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  const sc = sp(f);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform={`translate(270,420) scale(${sc})`}>
        <circle r={70} fill="#FFD98A" stroke={O} strokeWidth={4} />
        {[0, 45, 90, 135, 180, 225, 270, 315].map((angle, i) => (
          <line key={i} x1={Math.cos((angle * Math.PI) / 180) * 85} y1={Math.sin((angle * Math.PI) / 180) * 85} x2={Math.cos((angle * Math.PI) / 180) * 115} y2={Math.sin((angle * Math.PI) / 180) * 115} stroke="#FFD98A" strokeWidth={6} strokeLinecap="round" />
        ))}
      </g>
    </Stage>
  );
};

export const S1: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const exp = sp(lf(4.36));
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform="translate(270,420)">
        <circle r={30} fill="#E8B84A" stroke={O} strokeWidth={4} />
        <g transform={`scale(${exp})`} opacity={Math.min(1, 2 - exp)}>
          <circle r={140} fill="none" stroke={C.red} strokeWidth={12} opacity={0.8} />
          <circle r={90} fill="none" stroke="#FFD98A" strokeWidth={8} />
        </g>
      </g>
    </Stage>
  );
};

export const S2: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(9.74));
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform={`translate(270,420) scale(${k})`}>
        <circle r={120} fill="#3b4466" stroke={O} strokeWidth={4} strokeDasharray="10 10" />
        <circle r={25} fill="#C8451E" stroke={O} strokeWidth={4} />
      </g>
    </Stage>
  );
};

export const S3: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(16.0));
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform={`translate(270,420) scale(${k})`}>
        <circle r={35} fill="#2C483B" stroke={O} strokeWidth={4} />
        <circle r={12} fill="#F6EFE8" />
      </g>
    </Stage>
  );
};

export const S4: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(18.4));
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform={`translate(270,420) scale(${k})`}>
        <rect x={-110} y={-110} width={220} height={220} rx={110} fill="#22284A" stroke={O} strokeWidth={4} />
        <circle cx={80} cy={-60} r={18} fill="#E8B84A" stroke={O} strokeWidth={3} />
        <circle r={15} fill="#C8451E" stroke={O} strokeWidth={3} />
      </g>
    </Stage>
  );
};

export const S5: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(23.94));
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform={`translate(270,420) scale(${k})`}>
        <rect x={-130} y={-70} width={260} height={140} rx={24} fill="#F6EFE8" stroke={O} strokeWidth={4} />
        <text x={0} y={12} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={36} fill={C.ink}>City Size</text>
      </g>
    </Stage>
  );
};

export const S6: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(29.52));
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform={`translate(270,420) scale(${k})`}>
        <rect x={-150} y={-80} width={300} height={160} rx={24} fill="#C8451E" stroke={O} strokeWidth={4} />
        <text x={0} y={15} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={40} fill="#fff">1 Teaspoon</text>
      </g>
    </Stage>
  );
};

export const S7: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  const rot = (f * 12) % 360;
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform={`translate(270,420) rotate(${rot})`}>
        <rect x={-80} y={-15} width={160} height={30} rx={15} fill="#D9A93A" stroke={O} strokeWidth={4} />
        <circle r={20} fill="#F6EFE8" stroke={O} strokeWidth={3} />
      </g>
    </Stage>
  );
};

export const S8: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(41.6));
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform={`translate(270,420) scale(${k})`}>
        <rect x={-120} y={-60} width={240} height={120} rx={20} fill="#2C483B" stroke={O} strokeWidth={4} />
        <text x={0} y={12} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={38} fill="#fff">Pulsar</text>
      </g>
    </Stage>
  );
};

export const S9: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  const beamRot = (f * 18) % 360;
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform="translate(270,420)">
        <g transform={`rotate(${beamRot})`}>
          <polygon points="0,0 -150,-300 150,-300" fill="#FFD98A" opacity={0.3} />
          <polygon points="0,0 -150,300 150,300" fill="#FFD98A" opacity={0.3} />
        </g>
        <circle r={25} fill="#F6EFE8" stroke={O} strokeWidth={4} />
      </g>
    </Stage>
  );
};

export const S10: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(48.29));
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform={`translate(270,420) scale(${k})`}>
        <ellipse rx={140} ry={80} fill="none" stroke="#6E96BB" strokeWidth={6} strokeDasharray="12 12" />
        <circle r={35} fill="#C8451E" stroke={O} strokeWidth={4} />
      </g>
    </Stage>
  );
};

export const S11: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(54.87));
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform={`translate(270,420) scale(${k})`}>
        <rect x={-130} y={-60} width={260} height={120} rx={20} fill="#3B1B22" stroke={O} strokeWidth={4} />
        <text x={0} y={12} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={38} fill="#fff">Magnetar</text>
      </g>
    </Stage>
  );
};

export const S12: React.FC<SP> = ({ t0, dur }) => {
  const { f } = useT(t0);
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform="translate(270,420)">
        <circle r={90} fill="#22284A" stroke={O} strokeWidth={4} />
        <path d="M-40 -40 Q0 -90 40 -40" stroke="#FFD98A" strokeWidth={6} fill="none" strokeLinecap="round" />
      </g>
    </Stage>
  );
};

export const S13: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const k = sp(lf(63.05));
  return (
    <Stage dur={dur} bg={C.night}>
      <RoomNight f={f} />
      <g transform={`translate(270,420) scale(${k})`}>
        <text x={0} y={0} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={44} fill="#F6EFE8">Mysterious</text>
      </g>
    </Stage>
  );
};

export const SCENES = [
  { s: 0.0, e: 4.36, C: S0 },
  { s: 4.36, e: 9.74, C: S1 },
  { s: 9.74, e: 16.00, C: S2 },
  { s: 16.00, e: 18.40, C: S3 },
  { s: 18.40, e: 23.94, C: S4 },
  { s: 23.94, e: 29.52, C: S5 },
  { s: 29.52, e: 35.86, C: S6 },
  { s: 35.86, e: 41.60, C: S7 },
  { s: 41.60, e: 43.81, C: S8 },
  { s: 43.81, e: 48.29, C: S9 },
  { s: 48.29, e: 54.87, C: S10 },
  { s: 54.87, e: 58.23, C: S11 },
  { s: 58.23, e: 63.05, C: S12 },
  { s: 63.05, e: 69.67, C: S13 },
];
