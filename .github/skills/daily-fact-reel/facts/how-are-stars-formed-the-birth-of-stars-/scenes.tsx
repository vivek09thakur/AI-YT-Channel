import React from 'react';
import { interpolate, spring, useCurrentFrame } from 'remotion';
import { C, FPS, SPRING, T, clamp } from './theme';
import { Stage } from './chrome';
import { Person, Mini, Bubble } from './figures';
import * as K from './kit';

const { mouthOpen, useT, sp, breathe, blinkAt } = K;
type SP = K.SP;
const O = K.O;

const ASTRONOMER = {
  skin: '#A86D40',
  ear: '#97603A',
  shirt: '#423229',
  pants: '#242F3D',
  hair: '#14110E',
  glasses: true,
};

// S0: Hook - Stargazer looking through telescope into night space
export const S0: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  const qPop = sp(lf(1.2));
  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />
      {/* Distant Twinkling Stars */}
      {[
        [80, 180], [210, 140], [360, 200], [460, 160],
        [140, 300], [310, 290], [480, 330], [90, 420],
      ].map(([x, y], i) => (
        <circle
          key={i}
          cx={x}
          cy={y}
          r={2.5 + (i % 2)}
          fill="#FFF4D0"
          opacity={0.4 + 0.6 * Math.sin(f / 10 + i * 1.5)}
        />
      ))}

      {/* Hill silhouette */}
      <path d="M-40 680 Q180 570 580 620 L580 960 L-40 960 Z" fill="#121820" stroke={O} strokeWidth={4} />

      {/* Telescope */}
      <g transform="translate(320, 500) rotate(-32)">
        <rect x={-80} y={-14} width={160} height={28} rx={6} fill="#7A8B99" stroke={O} strokeWidth={3.5} />
        <rect x={70} y={-18} width={22} height={36} rx={4} fill="#D9A93A" stroke={O} strokeWidth={3} />
        <line x1={-10} y1={14} x2={-45} y2={130} stroke={O} strokeWidth={6} strokeLinecap="round" />
        <line x1={0} y1={14} x2={5} y2={130} stroke={O} strokeWidth={6} strokeLinecap="round" />
        <line x1={10} y1={14} x2={55} y2={130} stroke={O} strokeWidth={6} strokeLinecap="round" />
      </g>

      <Person
        x={160}
        y={540 + breathe(f)}
        s={0.82}
        pose="stand"
        {...ASTRONOMER}
        blink={blinkAt(f)}
        mouth={mouthOpen('host', t)}
        arm="raise"
        hand={[115, -130]}
        elbow={[65, -100]}
      />

      {/* Question bubble */}
      <g transform={`translate(230, 250) scale(${Math.min(1, qPop)})`} opacity={Math.min(1, qPop)}>
        <rect x={-60} y={-45} width={120} height={90} rx={24} fill={C.card} stroke={O} strokeWidth={3.5} />
        <text x={0} y={16} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={56} fill={C.red}>?</text>
      </g>
    </Stage>
  );
};

// S1: Stellar Nebula cloud of dust and gas
export const S1: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const cardScale = sp(lf(5.2));
  return (
    <Stage dur={dur} bg={C.navy}>
      <rect width={540} height={960} fill={C.navy} />
      {/* Billowing dust clouds */}
      <g opacity={0.85}>
        <ellipse cx={270} cy={420} rx={190 + Math.sin(f / 18) * 12} ry={130 + Math.cos(f / 20) * 10} fill="#6E3E68" opacity={0.65} />
        <ellipse cx={220} cy={380} rx={140} ry={110} fill="#B6533A" opacity={0.7} />
        <ellipse cx={330} cy={450} rx={130} ry={90} fill="#335C67" opacity={0.7} />
        <circle cx={270} cy={410} r={75 + Math.sin(f / 12) * 8} fill="#E09F3E" opacity={0.6} />
      </g>

      {/* Dust speckles floating */}
      {[
        [160, 360], [240, 320], [360, 380], [300, 480],
        [180, 460], [390, 430], [210, 520], [340, 330],
      ].map(([x, y], i) => (
        <circle
          key={i}
          cx={x + Math.sin(f / 15 + i) * 14}
          cy={y + Math.cos(f / 14 + i) * 14}
          r={4}
          fill="#FFF2CC"
          stroke={O}
          strokeWidth={1.5}
        />
      ))}

      {/* Label Card */}
      <g transform={`translate(270, 200) scale(${Math.min(1, cardScale)})`} opacity={Math.min(1, cardScale)}>
        <rect x={-140} y={-36} width={280} height={72} rx={22} fill={C.card} stroke={O} strokeWidth={3.5} />
        <text x={0} y={10} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={30} fill={C.ink}>
          STELLAR NEBULA
        </text>
      </g>
    </Stage>
  );
};

// S2: Hydrogen atoms - The core ingredient
export const S2: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const hPop1 = sp(lf(9.8));
  const hPop2 = sp(lf(10.5));
  const hPop3 = sp(lf(11.2));
  const cardB = sp(lf(12.5));

  const drawAtom = (x: number, y: number, scale: number, delayPhase: number) => {
    const orbitAngle = (f * 3.5 + delayPhase) * (Math.PI / 180);
    const ex = x + Math.cos(orbitAngle) * 52;
    const ey = y + Math.sin(orbitAngle) * 28;
    return (
      <g transform={`translate(${x},${y}) scale(${Math.min(1, scale)})`} opacity={Math.min(1, scale)}>
        <ellipse cx={0} cy={0} rx={54} ry={30} fill="none" stroke="#A7BED3" strokeWidth={3} strokeDasharray="6 4" transform="rotate(-20)" />
        <circle cx={0} cy={0} r={34} fill={C.red} stroke={O} strokeWidth={3.5} />
        <text x={0} y={12} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={32} fill="#FFF">H</text>
        <circle cx={ex - x} cy={ey - y} r={9} fill="#FFD166" stroke={O} strokeWidth={2.5} />
      </g>
    );
  };

  return (
    <Stage dur={dur} bg={C.beige}>
      <rect width={540} height={960} fill={C.beige} />
      {/* Top Banner */}
      <g transform={`translate(270, 210) scale(${Math.min(1, cardB)})`} opacity={Math.min(1, cardB)}>
        <rect x={-170} y={-40} width={340} height={80} rx={24} fill={C.card} stroke={O} strokeWidth={3.5} />
        <text x={0} y={12} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={32} fill={C.red}>
          90% HYDROGEN
        </text>
      </g>

      {/* Floating Hydrogen Atoms */}
      {drawAtom(150, 420, hPop1, 0)}
      {drawAtom(390, 410, hPop2, 120)}
      {drawAtom(270, 580, hPop3, 240)}
    </Stage>
  );
};

// S3: Gravity collapsing gas inward into a dense hot core
export const S3: React.FC<SP> = ({ t0, dur }) => {
  const { f, t } = useT(t0);
  const compress = interpolate(t, [15.61, 22.18], [1, 0.45], clamp);
  const coreGlow = 0.7 + 0.3 * Math.sin(f / 8);

  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />
      {/* Contracting Inward Arrows */}
      {[0, 45, 90, 135, 180, 225, 270, 315].map((ang, i) => {
        const rad = (ang * Math.PI) / 180;
        const d = 190 * compress + 35;
        const x = 270 + Math.cos(rad) * d;
        const y = 430 + Math.sin(rad) * d;
        return (
          <g key={i} transform={`translate(${x},${y}) rotate(${ang + 180})`}>
            <line x1={-30} y1={0} x2={10} y2={0} stroke={C.red} strokeWidth={5} strokeLinecap="round" />
            <polygon points="12,-8 28,0 12,8" fill={C.red} stroke={O} strokeWidth={2} />
          </g>
        );
      })}

      {/* Hot Collapsing Core */}
      <circle cx={270} cy={430} r={110 * compress + 20} fill="#E26D5C" opacity={0.35 * coreGlow} />
      <circle cx={270} cy={430} r={75 * compress + 15} fill="#D4601F" stroke={O} strokeWidth={4} />
      <circle cx={270} cy={430} r={45 * compress + 10} fill="#FFD166" />

      {/* Badge label */}
      <g transform="translate(270, 640)">
        <rect x={-120} y={-30} width={240} height={60} rx={20} fill={C.card} stroke={O} strokeWidth={3} />
        <text x={0} y={10} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={28} fill={C.ink}>
          GRAVITY PULL
        </text>
      </g>
    </Stage>
  );
};

// S4: Pressure & Temperature rising gauge
export const S4: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  const cardScale = sp(lf(22.8));
  const needleRot = interpolate(t, [22.73, 27.41], [-60, 65], clamp);

  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />
      <g transform={`translate(270, 420) scale(${Math.min(1, cardScale)})`} opacity={Math.min(1, cardScale)}>
        {/* Gauge card */}
        <rect x={-180} y={-190} width={360} height={380} rx={28} fill={C.card} stroke={O} strokeWidth={4} />
        <text x={0} y={-135} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={28} fill={C.ink}>
          CORE PRESSURE
        </text>

        {/* Gauge Arc Background */}
        <path d="M-110 50 A 130 130 0 1 1 110 50" fill="none" stroke="#D3C7B1" strokeWidth={24} strokeLinecap="round" />
        <path d="M-110 50 A 130 130 0 0 1 10 -80" fill="none" stroke={C.teal} strokeWidth={22} strokeLinecap="round" />
        <path d="M10 -80 A 130 130 0 0 1 110 50" fill="none" stroke={C.red} strokeWidth={22} strokeLinecap="round" />

        {/* Needle */}
        <g transform={`translate(0, 50) rotate(${needleRot})`}>
          <line x1={0} y1={12} x2={0} y2={-110} stroke={O} strokeWidth={7} strokeLinecap="round" />
          <polygon points="-8,-90 0,-118 8,-90" fill={C.red} stroke={O} strokeWidth={2} />
          <circle cx={0} cy={0} r={16} fill="#423229" stroke={O} strokeWidth={3} />
        </g>

        {/* Temperature Badge */}
        <rect x={-110} y={105} width={220} height={52} rx={16} fill={C.red} />
        <text x={0} y={141} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={26} fill="#FFF">
          {Math.round(interpolate(t, [22.73, 27.41], [2, 15], clamp))} MILLION Â°C
        </text>
      </g>
    </Stage>
  );
};

// S5: Nuclear Fusion Trigger
export const S5: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const flash = sp(lf(28.2), { damping: 9, stiffness: 180, mass: 0.6 });
  const pulse = Math.sin(f / 6) * 10;

  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />

      {/* Explosion glow burst */}
      <g transform="translate(270, 420)">
        <circle r={180 * Math.min(1.2, flash) + pulse} fill="#FFD166" opacity={0.25} />
        <circle r={120 * Math.min(1.2, flash)} fill="#F45B69" opacity={0.5} />
        <circle r={70 * Math.min(1.2, flash)} fill="#FFF" stroke={O} strokeWidth={4} />

        {/* Energy rays */}
        {[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330].map((deg, i) => (
          <line
            key={i}
            x1={0}
            y1={-80}
            x2={0}
            y2={-150 - (i % 2) * 30}
            stroke="#FFE6A7"
            strokeWidth={4.5}
            strokeLinecap="round"
            transform={`rotate(${deg + f * 1.2})`}
            opacity={Math.min(1, flash)}
          />
        ))}
      </g>

      {/* Headline banner */}
      <g transform={`translate(270, 210) scale(${Math.min(1, flash)})`} opacity={Math.min(1, flash)}>
        <rect x={-160} y={-36} width={320} height={72} rx={22} fill={C.card} stroke={O} strokeWidth={3.5} />
        <text x={0} y={12} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={32} fill={C.red}>
          NUCLEAR FUSION!
        </text>
      </g>
    </Stage>
  );
};

// S6: Fusion reaction: H + H = He + Energy
export const S6: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const cardA = sp(lf(33.8));
  const cardB = sp(lf(35.2));
  const cardC = sp(lf(36.8));

  return (
    <Stage dur={dur} bg={C.paper}>
      <rect width={540} height={960} fill={C.paper} />

      {/* Fusion equation display */}
      <g transform={`translate(150, 320) scale(${Math.min(1, cardA)})`} opacity={Math.min(1, cardA)}>
        <circle r={52} fill={C.red} stroke={O} strokeWidth={4} />
        <text x={0} y={15} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={40} fill="#FFF">H</text>
      </g>

      <text x={235} y={335} fontFamily="NSB" fontWeight={800} fontSize={50} fill={C.ink}>+</text>

      <g transform={`translate(320, 320) scale(${Math.min(1, cardA)})`} opacity={Math.min(1, cardA)}>
        <circle r={52} fill={C.red} stroke={O} strokeWidth={4} />
        <text x={0} y={15} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={40} fill="#FFF">H</text>
      </g>

      {/* Arrow down */}
      <g transform={`translate(270, 420) scale(${Math.min(1, cardB)})`} opacity={Math.min(1, cardB)}>
        <path d="M0 -25 L0 35 M-16 18 L0 38 L16 18" stroke={C.ink} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" />
      </g>

      {/* Result Helium atom + Light */}
      <g transform={`translate(270, 560) scale(${Math.min(1, cardC)})`} opacity={Math.min(1, cardC)}>
        <rect x={-180} y={-70} width={360} height={140} rx={26} fill={C.card} stroke={O} strokeWidth={3.5} />
        <circle cx={-85} cy={0} r={46} fill={C.teal} stroke={O} strokeWidth={3.5} />
        <text x={-85} y={14} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={34} fill="#FFF">He</text>
        <text x={35} y={-8} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={30} fill={C.ink}>HELIUM</text>
        <text x={35} y={32} textAnchor="middle" fontFamily="Hind" fontWeight={700} fontSize={24} fill={C.red}>+ Heat & Light</text>
      </g>
    </Stage>
  );
};

// S7: New star is born!
export const S7: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const birthPop = sp(lf(40.4), { damping: 9, stiffness: 220, mass: 0.6 });

  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />

      {/* Shining star rays */}
      <g transform="translate(270, 410)">
        {[0, 45, 90, 135].map((ang, i) => (
          <ellipse
            key={i}
            rx={160 * Math.min(1, birthPop)}
            ry={28 * Math.min(1, birthPop)}
            fill="#FFF1BF"
            opacity={0.7 + 0.3 * Math.sin(f / 6 + i)}
            transform={`rotate(${ang + f * 0.4})`}
          />
        ))}
        <circle r={76 * Math.min(1, birthPop)} fill="#FFD166" stroke={O} strokeWidth={4} />
        <circle r={50 * Math.min(1, birthPop)} fill="#FFF" />
      </g>

      {/* Stamp badge */}
      <g transform={`translate(270, 620) scale(${Math.min(1, birthPop)})`} opacity={Math.min(1, birthPop)}>
        <rect x={-150} y={-36} width={300} height={72} rx={22} fill={C.card} stroke={C.red} strokeWidth={4} />
        <text x={0} y={12} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={32} fill={C.red}>
          NEW STAR BORN!
        </text>
      </g>
    </Stage>
  );
};

// S8: Stellar Lifespan (Millions to Billions of years)
export const S8: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const card1 = sp(lf(43.7));
  const card2 = sp(lf(45.5));

  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />

      {/* Giant Blue/White Star - Shorter life */}
      <g transform={`translate(270, 290) scale(${Math.min(1, card1)})`} opacity={Math.min(1, card1)}>
        <rect x={-200} y={-70} width={400} height={140} rx={24} fill={C.card} stroke={O} strokeWidth={3.5} />
        <circle cx={-115} cy={0} r={44} fill="#6EA4BF" stroke={O} strokeWidth={3.5} />
        <text x={-115} y={12} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={24} fill="#FFF">MASSIVE</text>
        <text x={35} y={-6} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={28} fill={C.ink}>10 MILLION</text>
        <text x={35} y={28} textAnchor="middle" fontFamily="Hind" fontWeight={600} fontSize={22} fill="#7A6855">Years Lifespan</text>
      </g>

      {/* Yellow Dwarf (Like our Sun) - Long life */}
      <g transform={`translate(270, 480) scale(${Math.min(1, card2)})`} opacity={Math.min(1, card2)}>
        <rect x={-200} y={-70} width={400} height={140} rx={24} fill={C.card} stroke={O} strokeWidth={3.5} />
        <circle cx={-115} cy={0} r={34} fill="#E09F3E" stroke={O} strokeWidth={3.5} />
        <text x={-115} y={9} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={20} fill="#FFF">SUN</text>
        <text x={35} y={-6} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={28} fill={C.red}>10 BILLION</text>
        <text x={35} y={28} textAnchor="middle" fontFamily="Hind" fontWeight={600} fontSize={22} fill="#7A6855">Years Lifespan</text>
      </g>
    </Stage>
  );
};

// S9: Takeaway - Night sky marvel and closing wisdom
export const S9: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  const badgeScale = sp(lf(55.2));

  return (
    <Stage dur={dur} bg={C.night}>
      <rect width={540} height={960} fill={C.night} />

      {/* Sparkling Sky */}
      {[
        [80, 160], [170, 220], [290, 150], [420, 190],
        [470, 280], [110, 310], [240, 280], [380, 330],
      ].map(([x, y], i) => (
        <circle
          key={i}
          cx={x}
          cy={y}
          r={2.5 + (i % 3)}
          fill="#FFF3C4"
          opacity={0.4 + 0.6 * Math.sin(f / 8 + i)}
        />
      ))}

      {/* Stargazer looking up in awe */}
      <Person
        x={270}
        y={540 + breathe(f)}
        s={0.88}
        pose="stand"
        {...ASTRONOMER}
        blink={blinkAt(f)}
        mouth={mouthOpen('host', t)}
        arm="raise"
        hand={[120, -145]}
        elbow={[66, -110]}
      />

      {/* Final takeaway card */}
      <g transform={`translate(270, 220) scale(${Math.min(1, badgeScale)})`} opacity={Math.min(1, badgeScale)}>
        <rect x={-180} y={-45} width={360} height={90} rx={26} fill={C.card} stroke={C.red} strokeWidth={4} />
        <text x={0} y={16} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={34} fill={C.ink}>
          IT STARTS WITH <tspan fill={C.red}>GRAVITY</tspan>
        </text>
      </g>
    </Stage>
  );
};

export const SCENES = [
  { s: 0.0, e: 4.6, C: S0 },
  { s: 4.6, e: 9.3, C: S1 },
  { s: 9.3, e: 15.3, C: S2 },
  { s: 15.3, e: 22.4, C: S3 },
  { s: 22.4, e: 27.7, C: S4 },
  { s: 27.7, e: 33.3, C: S5 },
  { s: 33.3, e: 40.0, C: S6 },
  { s: 40.0, e: 43.2, C: S7 },
  { s: 43.2, e: 49.1, C: S8 },
  { s: 49.1, e: 61.62, C: S9 },
];
