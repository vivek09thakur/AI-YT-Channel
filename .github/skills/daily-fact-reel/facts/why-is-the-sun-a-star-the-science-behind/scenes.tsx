import React from 'react';
import { interpolate, spring, useCurrentFrame } from 'remotion';
import { C, FPS, SPRING, T, clamp } from './theme';
import { Stage } from './chrome';
import { Person, PersonP } from './figures';
import * as K from './kit';

const { mouthOpen, useT, sp, breathe, blinkAt } = K;
type SP = K.SP;
const O = K.O;

const OBSERVER: PersonP = {
  x: 160,
  y: 570,
  s: 0.82,
  skin: '#B98055',
  ear: '#A66E44',
  shirt: '#2B3856',
  pants: '#1D2233',
  hair: '#1B140F',
  glasses: true
};

export const S0_Hook: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  const sunPop = sp(lf(1.0));
  const nightStars = interpolate(t, [3.8, 5.0], [0, 1], clamp);

  return (
    <Stage dur={dur} bg="#1E2338">
      <rect width={540} height={960} fill="#181D33" />
      <circle cx={420} cy={270} r={120} fill="#E58229" opacity={0.25} />
      <circle
        cx={420}
        cy={270}
        r={75 * Math.min(1, sunPop)}
        fill="#F4A236"
        stroke={O}
        strokeWidth={4}
      />
      {[-45, 0, 45, 90, 135, 180, 225, 270].map((deg, i) => (
        <line
          key={i}
          x1={420 + Math.cos((deg * Math.PI) / 180) * 88}
          y1={270 + Math.sin((deg * Math.PI) / 180) * 88}
          x2={420 + Math.cos((deg * Math.PI) / 180) * 110}
          y2={270 + Math.sin((deg * Math.PI) / 180) * 110}
          stroke="#F4A236"
          strokeWidth={4}
          strokeLinecap="round"
        />
      ))}

      <g opacity={nightStars}>
        {[
          [80, 160, 4],
          [200, 180, 6],
          [130, 260, 5],
          [280, 220, 4],
          [90, 340, 5]
        ].map(([x, y, r], idx) => (
          <g key={idx} transform={`translate(${x},${y})`}>
            <circle cx={0} cy={0} r={r} fill="#FFF3D1" />
            <path
              d={`M0 ${-r * 2} L0 ${r * 2} M${-r * 2} 0 L${r * 2} 0`}
              stroke="#FFF3D1"
              strokeWidth={1.5}
            />
          </g>
        ))}
      </g>

      <rect y={610} width={540} height={350} fill="#141829" />
      <rect y={606} width={540} height={6} fill="#0F1220" />

      <Person
        {...OBSERVER}
        y={570 + breathe(f)}
        blink={blinkAt(f)}
        mouth={mouthOpen('astronomer', t)}
        arm="raise"
        hand={[110, -140]}
        elbow={[60, -110]}
      />
    </Stage>
  );
};

export const S1_Secret: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const zoom = sp(lf(7.5), { damping: 11, stiffness: 140, mass: 0.8 });

  return (
    <Stage dur={dur} bg={C.card}>
      <rect width={540} height={960} fill={C.card} />
      <g transform={`translate(270, 360) scale(${Math.min(1.2, zoom)})`}>
        <circle r={140} fill="#E26D24" opacity={0.18} />
        <circle r={110} fill="#F4A236" stroke={O} strokeWidth={5} />
        <circle r={85} fill="#FFD05B" />
        <path
          d="M-50 -10 Q0 -60 50 -20 Q70 40 10 60 Q-60 40 -50 -10 Z"
          fill="#FFA938"
          opacity={0.6}
        />
        <text
          y={15}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={68}
          fill={C.ink}
        >
          STAR
        </text>
      </g>
      <text
        x={270}
        y={560}
        textAnchor="middle"
        fontFamily="Hind"
        fontWeight={700}
        fontSize={32}
        fill={C.red}
      >
        A Cosmic Engine
      </text>
    </Stage>
  );
};

export const S2_GasComposition: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const cardH = sp(lf(10.0));
  const cardHe = sp(lf(12.3));

  return (
    <Stage dur={dur} bg={C.beige}>
      <rect width={540} height={960} fill={C.beige} />

      <g transform="translate(270, 270)">
        <circle
          r={105 + Math.sin(f / 12) * 4}
          fill="#E56A24"
          stroke={O}
          strokeWidth={4}
        />
        <circle r={85} fill="#F3A338" />
        <circle r={60} fill="#FDE06E" />
      </g>

      <g
        transform={`translate(70, 430) scale(${Math.min(1, cardH)})`}
        opacity={Math.min(1, cardH)}
      >
        <rect
          width={180}
          height={170}
          rx={20}
          fill={C.card}
          stroke={O}
          strokeWidth={3}
        />
        <circle cx={90} cy={55} r={32} fill="#35678F" />
        <text
          x={90}
          y={66}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={34}
          fill="#FFF"
        >
          H
        </text>
        <text
          x={90}
          y={118}
          textAnchor="middle"
          fontFamily="Hind"
          fontWeight={700}
          fontSize={22}
          fill={C.ink}
        >
          Hydrogen
        </text>
        <text
          x={90}
          y={148}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={25}
          fill={C.red}
        >
          73%
        </text>
      </g>

      <g
        transform={`translate(290, 430) scale(${Math.min(1, cardHe)})`}
        opacity={Math.min(1, cardHe)}
      >
        <rect
          width={180}
          height={170}
          rx={20}
          fill={C.card}
          stroke={O}
          strokeWidth={3}
        />
        <circle cx={90} cy={55} r={32} fill="#D9822B" />
        <text
          x={90}
          y={66}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={34}
          fill="#FFF"
        >
          He
        </text>
        <text
          x={90}
          y={118}
          textAnchor="middle"
          fontFamily="Hind"
          fontWeight={700}
          fontSize={22}
          fill={C.ink}
        >
          Helium
        </text>
        <text
          x={90}
          y={148}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={25}
          fill={C.red}
        >
          25%
        </text>
      </g>
    </Stage>
  );
};

export const S3_CoreIntro: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const coreZoom = sp(lf(16.0), { damping: 12, stiffness: 130, mass: 0.9 });
  const labelPop = sp(lf(17.5));

  return (
    <Stage dur={dur} bg="#191524">
      <rect width={540} height={960} fill="#191524" />

      <g transform={`translate(270, 350) scale(${Math.min(1.15, coreZoom)})`}>
        <circle cx={0} cy={0} r={170} fill="#8A2714" opacity={0.35 + 0.08 * Math.sin(f / 10)} />
        <circle cx={0} cy={0} r={135} fill="#B63B18" stroke={O} strokeWidth={4} />
        <circle cx={0} cy={0} r={95} fill="#E56A20" />
        <circle cx={0} cy={0} r={60} fill="#FFAA33" stroke={O} strokeWidth={3} />
        <circle cx={0} cy={0} r={36} fill="#FFF2BD" opacity={0.85 + 0.15 * Math.sin(f / 5)} />
      </g>

      <g
        transform={`translate(270, 560) scale(${Math.min(1, labelPop)})`}
        opacity={Math.min(1, labelPop)}
      >
        <rect
          x={-170}
          y={-34}
          width={340}
          height={68}
          rx={34}
          fill={C.card}
          stroke={O}
          strokeWidth={3}
        />
        <text
          x={0}
          y={10}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={26}
          fill={C.red}
        >
          NUCLEAR FUSION
        </text>
      </g>
    </Stage>
  );
};

export const S3b_FusionReaction: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  const fused = t >= 23.0;
  const heScale = sp(lf(23.0));
  const flash = interpolate(t, [22.7, 23.0, 23.5], [0, 1, 0], clamp);
  const energyWaves = sp(lf(24.5));

  return (
    <Stage dur={dur} bg="#161421">
      <rect width={540} height={960} fill="#161421" />

      <circle
        cx={270}
        cy={370}
        r={140}
        fill="#C8451E"
        stroke={O}
        strokeWidth={4}
        opacity={0.9}
      />
      <circle cx={270} cy={370} r={90} fill="#FFA733" />
      <circle
        cx={270}
        cy={370}
        r={60}
        fill="#FFF6D8"
        opacity={0.5 + 0.5 * flash}
      />

      {!fused ? (
        <g transform="translate(270, 370)">
          <g transform={`translate(${-46 + Math.sin(f / 4) * 10}, -16)`}>
            <circle cx={0} cy={0} r={24} fill="#4E84B0" stroke={O} strokeWidth={3} />
            <text y={8} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={24} fill="#FFF">H</text>
          </g>
          <g transform={`translate(${46 - Math.sin(f / 4) * 10}, 16)`}>
            <circle cx={0} cy={0} r={24} fill="#4E84B0" stroke={O} strokeWidth={3} />
            <text y={8} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={24} fill="#FFF">H</text>
          </g>
        </g>
      ) : (
        <g transform={`translate(270, 370) scale(${Math.min(1.2, heScale)})`}>
          <circle cx={0} cy={0} r={38} fill="#E29227" stroke={O} strokeWidth={3.5} />
          <text y={11} textAnchor="middle" fontFamily="NSB" fontWeight={800} fontSize={28} fill="#FFF">He</text>
        </g>
      )}

      <g opacity={Math.min(1, energyWaves)}>
        {[100, 140, 180].map((rad, i) => (
          <circle
            key={i}
            cx={270}
            cy={370}
            r={rad + ((f * 2 + i * 22) % 44)}
            fill="none"
            stroke="#FFF4A3"
            strokeWidth={3}
            opacity={0.4}
          />
        ))}
        <rect
          x={130}
          y={570}
          width={280}
          height={56}
          rx={28}
          fill={C.card}
          stroke={O}
          strokeWidth={3}
        />
        <text
          x={270}
          y={607}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={24}
          fill={C.red}
        >
          MASSIVE ENERGY
        </text>
      </g>
    </Stage>
  );
};

export const S4_WhatMakesAStar: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const seal = sp(lf(28.6), { damping: 10, stiffness: 180, mass: 0.8 });

  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />

      <g transform="translate(270, 280)">
        <circle r={110} fill="#F7B23B" stroke={O} strokeWidth={4} />
        <circle r={85} fill="#FFD76B" />
        <path
          d="M0 -70 L20 -15 L70 0 L20 20 L0 70 L-20 20 L-70 0 L-20 -15 Z"
          fill="#FFF"
          opacity={0.7}
        />
      </g>

      <g
        transform={`translate(270, 480) scale(${Math.min(1, seal)})`}
        opacity={Math.min(1, seal)}
      >
        <rect
          x={-180}
          y={-40}
          width={360}
          height={80}
          rx={24}
          fill={C.red}
          stroke={O}
          strokeWidth={3}
        />
        <text
          x={0}
          y={14}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={32}
          fill="#FFF"
        >
          SELF-POWERED
        </text>
      </g>

      <text
        x={270}
        y={590}
        textAnchor="middle"
        fontFamily="Hind"
        fontWeight={700}
        fontSize={26}
        fill={C.ink}
      >
        Creates its own radiation
      </text>
    </Stage>
  );
};

export const S5_DistantStars: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const telescopeK = sp(lf(31.8));

  return (
    <Stage dur={dur} bg="#101524">
      <rect width={540} height={960} fill="#101524" />

      {Array.from({ length: 24 }).map((_, idx) => {
        const sx = 40 + ((idx * 67) % 460);
        const sy = 140 + ((idx * 43) % 430);
        const blink = Math.sin(f / 6 + idx) > 0.3;
        return (
          <circle
            key={idx}
            cx={sx}
            cy={sy}
            r={idx % 4 === 0 ? 3.5 : 2}
            fill="#FFF5D6"
            opacity={blink ? 0.9 : 0.3}
          />
        );
      })}

      <g
        transform={`translate(270, 410) scale(${Math.min(1, telescopeK)})`}
      >
        <rect
          x={-120}
          y={-80}
          width={240}
          height={140}
          rx={20}
          fill={C.card}
          stroke={O}
          strokeWidth={3}
        />
        <text
          x={0}
          y={-20}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={25}
          fill={C.ink}
        >
          OTHER STARS
        </text>
        <circle cx={-40} cy={20} r={4} fill={C.red} />
        <circle cx={0} cy={20} r={3} fill={C.red} />
        <circle cx={40} cy={20} r={5} fill={C.red} />
        <text
          x={0}
          y={48}
          textAnchor="middle"
          fontFamily="Hind"
          fontWeight={600}
          fontSize={18}
          fill="#666"
        >
          Trillions of miles away
        </text>
      </g>
    </Stage>
  );
};

export const S6_ProximityComparison: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const sunCard = sp(lf(39.0));
  const distBar = sp(lf(41.8));

  return (
    <Stage dur={dur} bg={C.beige}>
      <rect width={540} height={960} fill={C.beige} />

      <g
        transform={`translate(160, 280) scale(${Math.min(1, sunCard)})`}
      >
        <circle r={80} fill="#F6A338" stroke={O} strokeWidth={4} />
        <circle r={60} fill="#FFD05B" />
        <text
          y={8}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={26}
          fill={C.ink}
        >
          SUN
        </text>
        <text
          y={110}
          textAnchor="middle"
          fontFamily="Hind"
          fontWeight={700}
          fontSize={22}
          fill={C.ink}
        >
          Closest Star
        </text>
      </g>

      <g transform="translate(390, 280)">
        <circle r={14} fill="#8A9CA8" stroke={O} strokeWidth={3} />
        <text
          y={40}
          textAnchor="middle"
          fontFamily="Hind"
          fontWeight={700}
          fontSize={20}
          fill={C.ink}
        >
          Earth
        </text>
      </g>

      <path
        d="M245 280 L370 280"
        stroke={C.red}
        strokeWidth={4}
        strokeDasharray="8 6"
      />

      <g
        transform={`translate(70, 470) scale(${Math.min(1, distBar)})`}
        opacity={Math.min(1, distBar)}
      >
        <rect
          width={400}
          height={110}
          rx={20}
          fill={C.card}
          stroke={O}
          strokeWidth={3}
        />
        <text
          x={200}
          y={42}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={30}
          fill={C.red}
        >
          93 MILLION MILES
        </text>
        <text
          x={200}
          y={78}
          textAnchor="middle"
          fontFamily="Hind"
          fontWeight={600}
          fontSize={21}
          fill={C.ink}
        >
          Next star: 25,000,000,000,000 mi
        </text>
      </g>
    </Stage>
  );
};

export const S7_WithoutSun: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const iceCard = sp(lf(46.2));

  return (
    <Stage dur={dur} bg="#111622">
      <rect width={540} height={960} fill="#0E121B" />

      <g transform="translate(270, 300)">
        <circle r={90} fill="#23354C" stroke={O} strokeWidth={4} />
        <path
          d="M-50 -20 Q-20 -60 10 -40 Q40 -20 60 -5 Q50 40 10 50 Q-40 40 -50 -20 Z"
          fill="#1A2535"
        />
        <path
          d="M-70 10 Q-30 0 -10 30 Q20 40 40 60 Q-20 80 -60 50 Z"
          fill="#3B577A"
          opacity={0.5}
        />
        <circle
          cx={0}
          cy={0}
          r={98}
          fill="none"
          stroke="#5C85B5"
          strokeWidth={4}
          strokeDasharray="14 10"
        />
      </g>

      <g
        transform={`translate(90, 470) scale(${Math.min(1, iceCard)})`}
        opacity={Math.min(1, iceCard)}
      >
        <rect
          width={360}
          height={140}
          rx={20}
          fill="#1C2436"
          stroke="#4D6E99"
          strokeWidth={3}
        />
        <text
          x={180}
          y={50}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={32}
          fill="#94C5FF"
        >
          DARK & FROZEN
        </text>
        <text
          x={180}
          y={95}
          textAnchor="middle"
          fontFamily="Hind"
          fontWeight={700}
          fontSize={24}
          fill="#E6EAF2"
        >
          No light â¢ No warmth â¢ No life
        </text>
      </g>
    </Stage>
  );
};

export const S8_SolarSystemHeart: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const heartPop = sp(lf(54.9));

  return (
    <Stage dur={dur} bg="#16182E">
      <rect width={540} height={960} fill="#14172B" />

      {[110, 160, 210].map((r, i) => (
        <ellipse
          key={i}
          cx={270}
          cy={360}
          rx={r * 1.15}
          ry={r * 0.55}
          fill="none"
          stroke="#444C6E"
          strokeWidth={2}
          strokeDasharray="6 6"
        />
      ))}

      <circle
        cx={270 + Math.cos(f / 20) * 126}
        cy={360 + Math.sin(f / 20) * 60}
        r={9}
        fill="#4A90E2"
      />
      <circle
        cx={270 + Math.cos(f / 28 + 2) * 184}
        cy={360 + Math.sin(f / 28 + 2) * 88}
        r={14}
        fill="#C96538"
      />

      <g transform="translate(270, 360)">
        <circle r={62} fill="#F49E33" stroke={O} strokeWidth={4} />
        <circle r={45} fill="#FFD05B" />
      </g>

      <g
        transform={`translate(270, 560) scale(${Math.min(1, heartPop)})`}
        opacity={Math.min(1, heartPop)}
      >
        <rect
          x={-180}
          y={-35}
          width={360}
          height={70}
          rx={35}
          fill={C.card}
          stroke={O}
          strokeWidth={3}
        />
        <text
          x={0}
          y={11}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={25}
          fill={C.red}
        >
          HEART OF SOLAR SYSTEM
        </text>
      </g>
    </Stage>
  );
};

export const S9_Takeaway: React.FC<SP> = ({ t0, dur }) => {
  const { f, lf } = useT(t0);
  const badge = sp(lf(58.8));

  return (
    <Stage dur={dur} bg={C.cream}>
      <rect width={540} height={960} fill={C.cream} />

      <g transform="translate(270, 280)">
        <circle
          r={120 + Math.sin(f / 10) * 5}
          fill="#F59F33"
          stroke={O}
          strokeWidth={5}
        />
        <circle r={90} fill="#FFD662" />
        <path
          d="M0 -60 L18 -15 L60 0 L18 15 L0 60 L-18 15 L-60 0 L-18 -15 Z"
          fill="#FFF"
          opacity={0.8}
        />
      </g>

      <g
        transform={`translate(270, 480) scale(${Math.min(1, badge)})`}
        opacity={Math.min(1, badge)}
      >
        <rect
          x={-170}
          y={-38}
          width={340}
          height={76}
          rx={20}
          fill={C.red}
          stroke={O}
          strokeWidth={3}
        />
        <text
          x={0}
          y={12}
          textAnchor="middle"
          fontFamily="NSB"
          fontWeight={800}
          fontSize={34}
          fill="#FFF"
        >
          OUR NEAREST STAR
        </text>
      </g>

      <text
        x={270}
        y={590}
        textAnchor="middle"
        fontFamily="Hind"
        fontWeight={700}
        fontSize={28}
        fill={C.ink}
      >
        Powered by Fusion
      </text>
    </Stage>
  );
};

export const SCENES = [
  { s: 0.0, e: 7.2, C: S0_Hook },
  { s: 7.2, e: 9.5, C: S1_Secret },
  { s: 9.5, e: 15.4, C: S2_GasComposition },
  { s: 15.4, e: 20.3, C: S3_CoreIntro },
  { s: 20.3, e: 28.2, C: S3b_FusionReaction },
  { s: 28.2, e: 31.3, C: S4_WhatMakesAStar },
  { s: 31.3, e: 38.4, C: S5_DistantStars },
  { s: 38.4, e: 45.5, C: S6_ProximityComparison },
  { s: 45.5, e: 51.1, C: S7_WithoutSun },
  { s: 51.1, e: 58.5, C: S8_SolarSystemHeart },
  { s: 58.5, e: 63.69, C: S9_Takeaway }
];
