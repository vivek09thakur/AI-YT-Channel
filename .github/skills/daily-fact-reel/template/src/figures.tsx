import React from 'react';
import { spring, useCurrentFrame } from 'remotion';
import { C, FPS, SPRING } from './theme';

const O = C.outline;

export type PersonP = {
  x: number; y: number; s?: number; flip?: boolean; pose?: 'sit' | 'stand';
  skin: string; ear: string; shirt: string; pants: string; hair: string;
  long?: boolean; lungi?: string; glasses?: boolean; mustache?: string;
  mouth?: boolean; smile?: boolean; sad?: boolean; blink?: boolean;
  hand?: [number, number]; elbow?: [number, number]; arm?: 'rest' | 'raise';
};

export const Person: React.FC<PersonP> = (p) => {
  const { x, y, s = 1, flip, pose = 'sit', skin, ear, shirt, pants, hair, long, lungi, glasses, mustache, mouth, smile, sad, blink, arm = 'rest' } = p;
  const sit = pose === 'sit';
  const hand = p.hand ?? (sit ? [128, -126] : arm === 'raise' ? [120, -150] : [18, -30]);
  const elbow = p.elbow ?? (sit ? [62, -96] : arm === 'raise' ? [64, -112] : [10, -90]);
  const armPts = `0,-160 ${elbow[0]},${elbow[1]} ${hand[0]},${hand[1]}`;
  const torsoH = long && !sit ? 300 : 200;
  return (
    <g transform={`translate(${x},${y}) scale(${flip ? -s : s},${s})`}>
      {sit ? (
        <>
          <rect x={-45} y={-30} width={190} height={60} rx={28} fill={pants} stroke={O} strokeWidth={4} />
          <rect x={98} y={-8} width={54} height={190} rx={26} fill={pants} stroke={O} strokeWidth={4} />
          <ellipse cx={132} cy={184} rx={48} ry={17} fill="#1f1a17" stroke={O} strokeWidth={3} />
        </>
      ) : (
        <>
          {lungi ? (
            <>
              <rect x={-46} y={-30} width={104} height={238} rx={22} fill={lungi} stroke={O} strokeWidth={4} />
              <path d="M-46 60 H58 M-46 130 H58 M-10 -30 V208 M24 -30 V208" stroke="#00000030" strokeWidth={3} />
              <ellipse cx={14} cy={214} rx={44} ry={13} fill="#6b4a32" stroke={O} strokeWidth={3} />
            </>
          ) : (
            <>
              <rect x={-34} y={0} width={44} height={205} rx={20} fill={pants} stroke={O} strokeWidth={4} opacity={0.92} />
              <rect x={-10} y={0} width={46} height={205} rx={20} fill={pants} stroke={O} strokeWidth={4} />
              <ellipse cx={14} cy={208} rx={46} ry={15} fill="#1f1a17" stroke={O} strokeWidth={3} />
            </>
          )}
        </>
      )}
      <rect x={-45} y={-195} width={92} height={torsoH} rx={38} fill={shirt} stroke={O} strokeWidth={4} />
      <rect x={-14} y={-228} width={30} height={40} rx={10} fill={skin} stroke={O} strokeWidth={4} />
      <circle cx={6} cy={-272} r={62} fill={skin} stroke={O} strokeWidth={4} />
      <ellipse cx={-16} cy={-262} rx={13} ry={19} fill={ear} stroke={O} strokeWidth={3} />
      <path d="M-58 -282 Q-46 -346 14 -340 Q68 -334 70 -284 Q40 -308 -12 -300 Z" fill={hair} stroke={O} strokeWidth={3} />
      {blink ? (
        <path d="M24 -278 Q36 -272 48 -278" stroke={O} strokeWidth={4} fill="none" strokeLinecap="round" />
      ) : (
        <>
          <circle cx={36} cy={-278} r={13} fill="#fff" stroke={O} strokeWidth={3} />
          <circle cx={40} cy={-278} r={6} fill={O} />
        </>
      )}
      {sad ? (
        <path d="M24 -296 L50 -306" stroke={O} strokeWidth={4} strokeLinecap="round" />
      ) : (
        <path d="M26 -300 Q38 -308 50 -300" stroke={O} strokeWidth={4} fill="none" strokeLinecap="round" />
      )}
      {glasses && (
        <>
          <circle cx={38} cy={-278} r={21} fill="#ffffff22" stroke={O} strokeWidth={3} />
          <path d="M17 -280 L-8 -286" stroke={O} strokeWidth={3} />
        </>
      )}
      {mustache && <path d="M48 -256 Q62 -266 76 -256 Q62 -250 48 -256 Z" fill={mustache} stroke={O} strokeWidth={2} />}
      {mouth ? (
        <ellipse cx={60} cy={-240} rx={8} ry={11} fill="#3b1a14" />
      ) : smile ? (
        <path d="M44 -242 Q58 -226 72 -244" stroke={O} strokeWidth={4} fill="none" strokeLinecap="round" />
      ) : sad ? (
        <path d="M48 -236 Q58 -246 68 -236" stroke={O} strokeWidth={4} fill="none" strokeLinecap="round" />
      ) : (
        <path d="M48 -242 Q58 -237 66 -243" stroke={O} strokeWidth={4} fill="none" strokeLinecap="round" />
      )}
      <polyline points={armPts} fill="none" stroke={O} strokeWidth={46} strokeLinecap="round" strokeLinejoin="round" />
      <polyline points={armPts} fill="none" stroke={shirt} strokeWidth={38} strokeLinecap="round" strokeLinejoin="round" />
      <circle cx={hand[0]} cy={hand[1]} r={23} fill={skin} stroke={O} strokeWidth={4} />
    </g>
  );
};

// simple faceless infographic person
export const Mini: React.FC<{ x: number; y: number; s?: number; color: string; skin?: string; flip?: boolean; bob?: number }> = ({ x, y, s = 1, color, skin = '#9A6238', flip, bob = 0 }) => (
  <g transform={`translate(${x},${y + bob}) scale(${flip ? -s : s},${s})`}>
    <rect x={-12} y={-12} width={10} height={50} rx={5} fill="#2A3550" />
    <rect x={2} y={-12} width={10} height={50} rx={5} fill="#2A3550" />
    <rect x={-17} y={-76} width={34} height={70} rx={17} fill={color} />
    <circle cx={0} cy={-96} r={17} fill={skin} />
    <path d="M-17 -100 Q-12 -118 4 -114 Q17 -112 17 -100 Q4 -108 -17 -100Z" fill="#17120f" />
    <circle cx={7} cy={-96} r={2.6} fill="#17120f" />
  </g>
);

export const Bubble: React.FC<{ x: number; y: number; text: string; delay?: number; w?: number; tail?: 'l' | 'r'; dark?: boolean }> = ({ x, y, text, delay = 0, w = 70, tail = 'l', dark }) => {
  const f = useCurrentFrame();
  const sc = spring({ frame: f - delay, fps: FPS, config: SPRING });
  const fill = dark ? '#2f2a27' : '#F6EFE8';
  const tx = dark ? '#F6EFE8' : C.ink;
  return (
    <g transform={`translate(${x},${y}) scale(${sc})`} opacity={Math.min(1, sc)}>
      <rect x={-w / 2} y={-26} width={w} height={42} rx={20} fill={fill} stroke={O} strokeWidth={2.5} />
      <path d={tail === 'l' ? 'M-14 14 L-24 30 L2 14Z' : 'M14 14 L24 30 L-2 14Z'} fill={fill} stroke={O} strokeWidth={2.5} strokeLinejoin="round" />
      <rect x={-w / 2 + 3} y={8} width={w - 6} height={9} fill={fill} />
      <text x={0} y={5} textAnchor="middle" fontFamily="Hind" fontWeight={700} fontSize={22} fill={tx}>{text}</text>
    </g>
  );
};
