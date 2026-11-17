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
  const dream = sp(lf(2.45));
  return (
    <Stage dur={dur}>
      <RoomNight f={f} />
      <DeskNight />
      <Person x={150} y={560 + breathe(f)} s={0.8} {...TANVIR} blink={blinkAt(f)} hand={[150, -62]} elbow={[70, -90]} />
      <DeskTop />
      <g transform={`translate(292,218) scale(${dream})`} opacity={Math.min(1, dream)}>
        <circle cx={0} cy={0} r={10} fill="#F6EFE8" transform="translate(-70,92)" />
        <circle cx={0} cy={0} r={16} fill="#F6EFE8" transform="translate(-48,64)" />
        <rect x={-62} y={-44} width={170} height={74} rx={36} fill="#F6EFE8" stroke={O} strokeWidth={3} />
        <rect x={-34} y={-28} width={114} height={42} rx={14} fill={C.red} />
        <text x={23} y={2} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={26} fill="#fff">বিসিএস</text>
      </g>
    </Stage>
  );
};

export const S1: React.FC<SP> = ({ t0, dur }) => {
  const { f, t } = useT(t0);
  const steam = (x: number, k: number) => (
    <path d={`M${x} 438 q-6 -12 0 -22 q6 -10 0 -22`} stroke="#ffffff" strokeWidth={3} fill="none" opacity={0.35 + 0.3 * Math.sin(f / 9 + k)} transform={`translate(0,${-((f + k * 9) % 26) * 0.5})`} />
  );
  return (
    <Stage dur={dur}>
      <rect width={540} height={960} fill="#DDCFB7" />
      <rect x={0} y={0} width={150} height={110} fill="#aebfc4" stroke="#8d7a5c" strokeWidth={6} />
      <rect x={62} y={0} width={6} height={110} fill="#8d7a5c" />
      <rect y={610} width={540} height={350} fill="#D3C7B1" />
      <rect y={606} width={540} height={6} fill="#c2b499" />
      <path d="M0 120 Q135 150 270 120 T540 120" stroke="#6b4a32" strokeWidth={3} fill="none" />
      {[40, 130, 220, 310, 400, 490].map((x, i) => (
        <circle key={i} cx={x} cy={128 + (i % 2 ? 6 : 14)} r={8} fill="#ffd98a" opacity={0.7 + 0.3 * Math.sin(f / 10 + i)} />
      ))}
      <rect x={30} y={470} width={170} height={190} rx={34} fill="#96A5AB" />
      <rect x={340} y={470} width={170} height={190} rx={34} fill="#a9a08a" />
      <Person x={112} y={520 + breathe(f)} s={0.82} {...TANVIR} blink={blinkAt(f)} mouth={mouthOpen('tanvir', t)} />
      <Person x={428} y={520 + breathe(f + 20)} s={0.82} flip {...SHUVO} blink={blinkAt(f + 40)} mouth={mouthOpen('shuvo', t)} smile={t > 10.48 && t < 12.0} />
      <rect x={196} y={500} width={150} height={14} rx={5} fill="#6B4A32" stroke={O} strokeWidth={3} />
      <rect x={256} y={514} width={30} height={190} fill="#5a3d28" />
      {[222, 298].map((x, i) => (
        <g key={i} transform={`translate(${x},446)`}>
          <rect width={34} height={50} rx={5} fill="#fbf6ee" stroke={O} strokeWidth={3} />
          <rect y={12} width={34} height={9} fill="#D4601F" />
          {i === 0 && <path d="M34 12 q18 4 0 24" fill="none" stroke="#fbf6ee" strokeWidth={7} />}
        </g>
      ))}
      {steam(239, 0)}{steam(315, 3)}
    </Stage>
  );
};

export const S2: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  return (
    <Stage dur={dur}>
      <rect width={540} height={960} fill="#cfd8dc" />
      <rect x={-20} y={300} width={170} height={330} fill="#bfa98a" />
      <rect x={400} y={260} width={180} height={370} fill="#a89478" />
      {[0, 1, 2].map((r) => [0, 1].map((c) => (
        <rect key={`${r}${c}`} x={10 + c * 60} y={330 + r * 90} width={36} height={50} fill="#e9dcb8" opacity={0.85} />
      )))}
      {[0, 1, 2].map((r) => [0, 1].map((c) => (
        <rect key={`b${r}${c}`} x={430 + c * 56} y={290 + r * 95} width={36} height={52} fill="#d7c9a6" opacity={0.85} />
      )))}
      <rect x={0} y={610} width={540} height={350} fill="#b8a88a" />
      <rect x={0} y={606} width={540} height={8} fill="#a39475" />
      <rect x={262} y={250} width={10} height={360} fill="#4a3a2e" />
      <rect x={236} y={250} width={62} height={8} fill="#4a3a2e" />
      <Person x={120} y={520 + breathe(f)} s={0.8} pose="stand" {...(CHACHA as PersonP)} blink={blinkAt(f)} mouth={mouthOpen('chacha', t)} />
      <Person x={415} y={520 + breathe(f + 15)} s={0.8} pose="stand" flip {...TANVIR} blink={blinkAt(f + 30)} sad={t > 17.8} />
      {t > 17.3 && <Bubble x={200} y={238} text="?" w={54} delay={lf(17.36)} />}
    </Stage>
  );
};

export const S3: React.FC<SP> = (p) => <Relatives {...p} colors={['#B5543A', '#8f98a0', '#7a5c8f']} bubble="…" w={60} />;
export const S3b: React.FC<SP> = (p) => <Relatives {...p} colors={['#D9A93A', '#5f9d7a', '#c97f4a']} bubble="হা হা" w={92} laugh />;

export const S4: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  const look: [number, number] = [155, 340];
  const eyes: [number, number][] = [[330, 190], [470, 270], [250, 160], [60, 300], [480, 380], [370, 330]];
  const fill = interpolate(t, [30.24, 31.2], [0, 0.92], clamp);
  return (
    <Stage dur={dur}>
      <RoomNight f={f} />
      <DeskNight />
      <Person x={150} y={560 + breathe(f)} s={0.8} {...TANVIR} blink={blinkAt(f)} sad hand={[150, -62]} elbow={[70, -90]} />
      <DeskTop />
      {eyes.map(([x, y], i) => <Eye key={i} x={x} y={y} d={T(26.7 - t0) + i * 14} look={look} f={f} />)}
      {t > 30.2 && (
        <g transform="translate(486,250)" opacity={Math.min(1, lf(30.24) / 6)}>
          <rect x={-18} y={0} width={36} height={220} rx={18} fill="#F6EFE8" stroke={O} strokeWidth={3} />
          <rect x={-12} y={214 - 208 * fill} width={24} height={208 * fill} rx={12} fill={C.red} />
          <text y={-10} textAnchor="middle" fontFamily="Hind" fontWeight={700} fontSize={20} fill="#F6EFE8">চাপ</text>
        </g>
      )}
    </Stage>
  );
};

export const S5: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  const a = interpolate(t, [31.58, 32.6], [100, 25], clamp);
  const cardA = sp(lf(31.35));
  const outA = interpolate(t, [32.8, 33.1], [0, 1], clamp);
  const cardB = sp(lf(33.05), { damping: 11, stiffness: 120, mass: 0.9 });
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <g transform={`translate(80,${250 - outA * 400}) scale(${Math.min(1, cardA)})`} opacity={1 - outA}>
        <rect width={380} height={170} rx={20} fill="#F6EFE8" stroke={O} strokeWidth={3} />
        <text x={30} y={50} fontFamily="Hind" fontWeight={700} fontSize={26} fill={C.ink}>মনোযোগ</text>
        <text x={350} y={50} textAnchor="end" fontFamily="NSB" fontWeight={800} fontSize={32} fill={C.red}>{bn(Math.round(a))}%</text>
        <rect x={30} y={90} width={320} height={26} rx={13} fill="#d9cbb2" />
        <rect x={30} y={90} width={(320 * a) / 100} height={26} rx={13} fill={C.teal} />
      </g>
      <g opacity={Math.min(1, cardB)} transform={`translate(0,${(1 - Math.min(1, cardB)) * -300})`}>
        <Doc x={130} y={180} />
        <text x={270} y={450} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={120} fill={C.red} opacity={0.5 + 0.5 * Math.sin(f / 6)}>?</text>
      </g>
    </Stage>
  );
};

export const S6: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  const stampK = sp(lf(35.0), { damping: 9, stiffness: 220, mass: 0.7 });
  const docOut = interpolate(t, [36.1, 36.4], [1, 0], clamp);
  const showPeople = t > 36.2;
  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />
      <g opacity={docOut}>
        <Doc x={130} y={190} />
        <g transform={`translate(270,400) rotate(-14) scale(${2.6 - 1.6 * Math.min(1, stampK)})`} opacity={Math.min(1, stampK)}>
          <circle r={86} fill="none" stroke={C.red} strokeWidth={14} />
          <path d="M-46 -46 L46 46 M46 -46 L-46 46" stroke={C.red} strokeWidth={22} strokeLinecap="round" />
        </g>
      </g>
      {showPeople && (
        <g>
          {['#B5543A', '#8f98a0', '#D9A93A', '#5f9d7a', '#7a5c8f'].map((c, i) => (
            <g key={i} opacity={sp(lf(36.25) - i * 3)} transform={`translate(0,${(1 - sp(lf(36.25) - i * 3)) * 30})`}>
              <Mini x={70 + i * 100} y={560} s={1.7} color={c} bob={0} />
              <Bubble x={75 + i * 100} y={300 + (i % 2) * 30} text={t > 37.5 ? '!' : '…'} w={56} delay={T(0.2) + i * 4 + T(36.25 - t0)} dark />
            </g>
          ))}
        </g>
      )}
    </Stage>
  );
};

export const S7: React.FC<SP> = ({ t0, dur }) => {
  const { f, t } = useT(t0);
  const filled = Math.max(0, Math.min(12, Math.floor((t - 39.3) / 0.34)));
  const done = sp(f - T(43.4 - t0));
  return (
    <Stage dur={dur}>
      <RoomDay />
      <rect x={215} y={500} width={330} height={14} rx={5} fill="#6B4A32" stroke={O} strokeWidth={3} />
      <rect x={222} y={514} width={14} height={140} fill="#5a3d28" />
      <rect x={510} y={514} width={14} height={140} fill="#5a3d28" />
      <Person x={150} y={560 + breathe(f)} s={0.8} {...TANVIR} blink={blinkAt(f)} smile={t > 41.0} hand={[150, -62]} elbow={[70, -90]} />
      <DeskTop lamp={false} />
      <g transform="translate(36,162)">
        {Array.from({ length: 12 }).map((_, i) => {
          const on = i < filled;
          const k = on ? sp(f - T(39.3 + i * 0.34 - t0), { damping: 10, stiffness: 200, mass: 0.6 }) : 0;
          return <rect key={i} x={(i % 6) * 78} y={Math.floor(i / 6) * 66} width={64} height={54} rx={12} fill={on ? C.teal : '#d3c7b1'} stroke={O} strokeWidth={2.5} transform={`translate(0,${(1 - Math.min(1, k)) * -8})`} />;
        })}
        {Array.from({ length: 12 }).map((_, i) => (
          <text key={i} x={(i % 6) * 78 + 32} y={Math.floor(i / 6) * 66 + 36} textAnchor="middle" fontFamily="Hind" fontWeight={700} fontSize={24} fill={i < filled ? '#fff' : '#9c8e76'}>{bn(i + 1)}</text>
        ))}
        <text x={234} y={-22} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={30} fill={C.red} opacity={Math.min(1, done)}>১ বছর</text>
      </g>
    </Stage>
  );
};

export const S8: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  const badge = sp(lf(46.4), { damping: 10, stiffness: 160, mass: 0.8 });
  return (
    <Stage dur={dur}>
      <RoomLiving />
      <rect x={290} y={440} width={190} height={210} rx={34} fill="#8c6a4f" />
      <Person x={410} y={540 + breathe(f)} s={0.8} flip {...FATHER} blink={blinkAt(f)} smile={t > 46.9} />
      <Person x={100} y={520 + breathe(f + 12)} s={0.8} pose="stand" {...TANVIR} blink={blinkAt(f + 30)} smile={t > 46.9} arm="raise" hand={[130, -150]} elbow={[64, -112]} />
      <g transform="translate(214,386) rotate(-8)">
        <rect width={52} height={66} rx={5} fill="#F6EFE8" stroke={O} strokeWidth={3} />
        <rect x={8} y={12} width={36} height={6} rx={3} fill="#cdbfa8" /><rect x={8} y={28} width={26} height={6} rx={3} fill="#cdbfa8" />
        <path d="M14 48 l8 8 l16 -18" stroke={C.teal} strokeWidth={5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </g>
      <g transform={`translate(270,190) scale(${Math.min(1, badge)})`} opacity={Math.min(1, badge)}>
        <rect x={-110} y={-30} width={220} height={60} rx={30} fill={C.teal} stroke={O} strokeWidth={3} />
        <text y={12} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={32} fill="#fff">উত্তীর্ণ ✔</text>
      </g>
    </Stage>
  );
};

export const S9: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const h = sp(lf(48.2));
  const m = sp(lf(49.8));
  const x = sp(lf(51.1), { damping: 9, stiffness: 220, mass: 0.7 });
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <text x={270} y={190} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={54} fill={C.ink} opacity={Math.min(1, h)} transform={`translate(0,${(1 - Math.min(1, h)) * 20})`}>
        শিক্ষাটা <tspan fill={C.teal}>সহজ</tspan>
      </text>
      <Megaphone k={Math.min(1, m) * (1 + 0.02 * Math.sin(f / 8))} xk={x} />
    </Stage>
  );
};

export const S10: React.FC<SP> = ({ t0, dur }) => {
  const { lf } = useT(t0);
  const a = sp(lf(53.2)), ar = interpolate(lf(54.0), [0, 12], [0, 1], clamp), b = sp(lf(54.55));
  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <StepCard y={290} n="১" text="কাজ" k={a} />
      <g opacity={ar} transform={`translate(0,${(1 - ar) * -10})`}>
        <path d="M270 380 V470" stroke={C.ink} strokeWidth={8} strokeLinecap="round" />
        <path d="M244 450 L270 480 L296 450" stroke={C.ink} strokeWidth={8} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </g>
      <StepCard y={580} n="২" text="ঘোষণা" k={b} />
    </Stage>
  );
};

// List the scenes in time order. s/e are seconds on the final timeline; cut inside voice pauses.
// The last scene should end at TOTAL (see data.ts).
export const SCENES = [
  { s: 0.0, e: 4.3, C: S0 }, { s: 4.3, e: 14.1, C: S1 }, { s: 14.1, e: 20.0, C: S2 },
  { s: 20.0, e: 23.2, C: S3 }, { s: 23.2, e: 26.1, C: S3b }, { s: 26.1, e: 31.3, C: S4 },
  { s: 31.3, e: 34.7, C: S5 }, { s: 34.7, e: 38.9, C: S6 }, { s: 38.9, e: 44.1, C: S7 },
  { s: 44.1, e: 48.0, C: S8 }, { s: 48.0, e: 52.9, C: S9 }, { s: 52.9, e: 59.0, C: S10 },
];
